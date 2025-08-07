from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, City, ServiceType, Order, Review, Portfolio, Tariff, BusyDate, Message, OrderResponse, OTP, BookingProposal

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Дополнительная информация', {'fields': ('user_type', 'phone_number', 'bio', 'profile_photo', 'rating')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'event_type', 'event_date', 'city', 'status')
    list_filter = ('status', 'event_type', 'city')
    search_fields = ('title', 'description', 'customer__username', 'city')
    date_hierarchy = 'event_date'

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'icon', 'is_active', 'sort_order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    ordering = ('sort_order', 'name')
    list_editable = ('sort_order', 'is_active')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('order', 'from_user', 'to_user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('comment', 'from_user__username', 'to_user__username')

class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__username', 'description')
    ordering = ('-created_at',)

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)

class BusyDateAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    list_filter = ('date',)
    search_fields = ('user__username',)
    date_hierarchy = 'date'

class MessageAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'order', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('content', 'from_user__username', 'to_user__username')
    date_hierarchy = 'created_at'

class OrderResponseAdmin(admin.ModelAdmin):
    list_display = ('performer', 'order', 'price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('performer__username', 'order__title', 'message')
    date_hierarchy = 'created_at'

class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'is_verified', 'attempts', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('phone_number',)
    date_hierarchy = 'created_at'

class BookingProposalAdmin(admin.ModelAdmin):
    list_display = ('performer', 'order', 'tariff', 'date', 'status', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('performer__username', 'order__title')
    date_hierarchy = 'created_at'

admin.site.register(User, CustomUserAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(BusyDate, BusyDateAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(OrderResponse, OrderResponseAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(BookingProposal, BookingProposalAdmin)
