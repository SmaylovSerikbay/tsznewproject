from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from PIL import Image
import os
from io import BytesIO
from django.core.files import File
import subprocess
import tempfile
from pathlib import Path

class City(models.Model):
    """Модель городов"""
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']

class ServiceType(models.Model):
    """Модель типов услуг"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS класс иконки (например: ri-camera-line)")
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'
        ordering = ['sort_order', 'name']

class User(AbstractUser):
    """Модель пользователей"""
    USER_TYPES = (
        ('customer', 'Заказчик'),
        ('performer', 'Исполнитель'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Город')
    rating = models.FloatField(default=0)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    
    # Поля для исполнителей
    company_name = models.CharField(max_length=100, blank=True, null=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип услуги')
    bio = models.TextField(blank=True)
    services = models.JSONField(default=list, blank=True, null=True, help_text="Список предоставляемых услуг")
    
    # Настройки уведомлений
    email_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def compress_image(self, image_field, max_size=(800, 800), quality=85):
        """Сжимает изображение до указанного размера и качества"""
        if not image_field:
            return
        
        try:
            # Открываем изображение
            img = Image.open(image_field)
            
            # Конвертируем в RGB если нужно
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Изменяем размер если изображение больше max_size
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Сохраняем сжатое изображение
            output = BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            # Создаем новое имя файла
            filename = os.path.basename(image_field.name)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_compressed.jpg"
            
            # Заменяем файл
            image_field.save(new_filename, File(output), save=False)
            
        except Exception as e:
            print(f"Ошибка при сжатии изображения: {e}")

    @property
    def completed_orders_count(self):
        """Количество завершенных заказов"""
        return self.orders_received.filter(status='completed').count()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Portfolio(models.Model):
    """Модель портфолио (фото и видео)"""
    MEDIA_TYPES = (
        ('image', 'Фото'),
        ('video', 'Видео'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    image = models.ImageField(upload_to='portfolio/', null=True, blank=True)
    video = models.FileField(upload_to='portfolio/videos/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='portfolio/thumbnails/', null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Длительность видео в секундах")
    file_size = models.BigIntegerField(null=True, blank=True, help_text="Размер файла в байтах")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Определяем тип медиа
        if self.video and not hasattr(self, '_processing_video'):
            self.media_type = 'video'
            self._processing_video = True
            self.compress_video()
            delattr(self, '_processing_video')
        elif self.image and not hasattr(self, '_processing_image'):
            self.media_type = 'image'
            self._processing_image = True
            self.compress_image()
            delattr(self, '_processing_image')
        
        super().save(*args, **kwargs)

    def compress_image(self, max_width=1920, max_height=1080, quality=85):
        """Сжимает изображение портфолио"""
        if not self.image:
            return
        
        try:
            from PIL import Image, ImageOps
            import io
            
            # Открываем изображение
            img = Image.open(self.image.path)
            
            # Автоматически поворачиваем изображение согласно EXIF
            img = ImageOps.exif_transpose(img)
            
            # Конвертируем в RGB если нужно
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Получаем размеры
            width, height = img.size
            
            # Изменяем размер если нужно
            if width > max_width or height > max_height:
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Сохраняем сжатое изображение
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            # Получаем размер файла
            self.file_size = len(output.getvalue())
            
            # Сохраняем сжатое изображение
            from django.core.files import File
            filename = os.path.basename(self.image.name)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_compressed.jpg"
            self.image.save(new_filename, File(output), save=False)
            
        except Exception as e:
            print(f"Ошибка при сжатии изображения портфолио: {e}")

    def compress_video(self, max_width=1280, max_height=720, max_bitrate='2M'):
        """Сжимает видео портфолио"""
        if not self.video:
            return
        
        try:
            # Получаем информацию о видео
            video_path = self.video.path
            if not os.path.exists(video_path):
                return
            
            # Получаем размер файла
            self.file_size = os.path.getsize(video_path)
            
            # Создаем простое превью (иконка видео)
            # В будущем можно добавить создание превью через ffmpeg
            self.save()
            
        except Exception as e:
            print(f"Ошибка при обработке видео портфолио: {e}")

    def get_duration_display(self):
        """Возвращает длительность видео в формате MM:SS"""
        if not self.duration:
            return ""
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_file_size_display(self):
        """Возвращает размер файла в читаемом формате"""
        if not self.file_size:
            return ""
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.1f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.1f} TB"

    def __str__(self):
        media_type_display = self.get_media_type_display()
        return f"{media_type_display} портфолио {self.user.username}"

    class Meta:
        verbose_name = 'Портфолио'
        verbose_name_plural = 'Портфолио'
        ordering = ['-created_at']

class PortfolioPhoto(models.Model):
    image = models.ImageField(upload_to='portfolio/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio photo {self.id}"

class Tariff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tariffs')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ['price']

class BusyDate(models.Model):
    """Модель занятых дат"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    
    class Meta:
        unique_together = ['user', 'date']

class Category(models.Model):   
    """Модель категорий"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Order(models.Model):
    """Модель заказов"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен')
    ]

    EVENT_TYPES = [
        ('wedding', 'Свадьба'),
        ('birthday', 'День рождения'),
        ('corporate', 'Корпоратив'),
        ('other', 'Другое')
    ]

    ORDER_TYPES = [
        ('request', 'Заявка'),  # Заявка от заказчика
        ('booking', 'Бронирование')  # Бронирование у исполнителя
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_created')
    performer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_received')
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_date = models.DateField()
    city = models.CharField(verbose_name='Город', max_length=100)
    venue = models.CharField(max_length=200, blank=True)
    guest_count = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Бюджет', default=0)
    services = models.JSONField()  # Хранит список выбранных услуг
    selected_performers = models.JSONField(default=dict, blank=True, help_text="Выбранные исполнители по услугам: {service_type: performer_id}")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, related_name='orders')
    details = models.TextField(blank=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES, default='request')

    def __str__(self):
        return f"{self.title} - {self.customer.get_full_name()}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(validators=[MinValueValidator(1)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.from_user.get_full_name()} for {self.to_user.get_full_name()}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class Message(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='messages')
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    performer = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='chat_messages_performer')
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f'Message from {self.from_user} to {self.to_user} in order {self.order.id}'

class OrderResponse(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонен'),
        ('cancelled', 'Отменен')
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='responses')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_responses')
    message = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отклик на заказ'
        verbose_name_plural = 'Отклики на заказы'
        ordering = ['-created_at']
        unique_together = ['order', 'performer']  # Один исполнитель - один отклик на заказ
        
    def __str__(self):
        return f'Response from {self.performer.get_full_name()} to order {self.order.id}'

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    def is_valid(self):
        # OTP is valid for 5 minutes and max 3 attempts
        return (
            not self.is_verified and
            self.attempts < 3 and
            (timezone.now() - self.created_at).total_seconds() < 300
        )

class BookingProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает ответа'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='booking_proposals')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_proposals')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['order', 'performer', 'date']
