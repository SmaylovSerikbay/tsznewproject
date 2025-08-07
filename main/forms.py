from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order, Review, Portfolio, Tariff

class UserRegistrationForm(UserCreationForm):
    city = forms.CharField(max_length=100, required=True, label='Город')
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'user_type', 'profile_photo', 'city')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'bio', 'profile_photo', 'city')

class OrderForm(forms.ModelForm):
    city = forms.ChoiceField(choices=[], required=True, label='Город')
    
    class Meta:
        model = Order
        fields = ['title', 'event_type', 'event_date', 'venue', 'guest_count', 
                 'description', 'budget']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'budget': forms.NumberInput(attrs={'min': '0', 'step': '10000'}),
            'guest_count': forms.NumberInput(attrs={'min': '1'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле description необязательным
        self.fields['description'].required = False
        
        # Получаем города из базы данных
        from .models import City
        cities = City.objects.filter(is_active=True).order_by('name')
        self.fields['city'].choices = [('', 'Выберите город')] + [(city.name, city.name) for city in cities]
        
        # Если это редактирование, устанавливаем текущий город
        if kwargs.get('instance'):
            instance = kwargs['instance']
            if instance.city:
                self.fields['city'].initial = instance.city

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'image', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название работы'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание работы'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        
        # Проверяем, что загружен хотя бы один файл
        if not image and not video:
            raise forms.ValidationError('Необходимо загрузить изображение или видео')
        
        # Проверяем, что не загружены оба файла одновременно
        if image and video:
            raise forms.ValidationError('Можно загрузить только изображение ИЛИ видео')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Определяем тип медиа
        if instance.video:
            instance.media_type = 'video'
        elif instance.image:
            instance.media_type = 'image'
        
        if commit:
            instance.save()
        return instance

class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'price', 'description'] 