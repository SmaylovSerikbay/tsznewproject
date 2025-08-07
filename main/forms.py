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
        fields = ['image']

class TariffForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = ['name', 'price', 'description'] 