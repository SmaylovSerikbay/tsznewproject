from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('auth/', views.auth, name='auth'),
    path('auth-page/', views.auth_page, name='auth_page'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('profile/update-photo/', views.update_profile_photo, name='update_profile_photo'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('profile/subscription/process/', views.process_subscription, name='process_subscription'),
    path('create-order/', views.create_order_request, name='create_order_request'),
    path('create-order/<int:performer_id>/', views.create_order_booking, name='create_order_booking'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/edit/', views.edit_order, name='edit_order'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
    path('order/<int:order_id>/review/', views.create_review, name='create_review'),
    path('order/<int:order_id>/performer-cancel/', views.performer_cancel_order, name='performer_cancel_order'),
    
    # Portfolio management
    path('portfolio/add/', views.add_portfolio, name='add_portfolio'),
    path('portfolio/<int:photo_id>/delete/', views.delete_portfolio_photo, name='delete_portfolio_photo'),
    path('portfolio/<int:item_id>/view/', views.view_portfolio_item, name='view_portfolio_item'),
    
    # Tariff management
    path('tariff/manage/', views.manage_tariff, name='manage_tariff'),
    path('tariff/<int:tariff_id>/delete/', views.delete_tariff, name='delete_tariff'),
    path('tariff/<int:tariff_id>/edit/', views.edit_tariff, name='edit_tariff'),
    
    # Calendar management
    path('calendar/manage/', views.manage_calendar, name='manage_calendar'),
    

    
    # Booking proposal URLs
    path('proposal/<int:proposal_id>/accept/', views.accept_proposal, name='accept_proposal'),
    path('proposal/<int:proposal_id>/reject/', views.reject_proposal, name='reject_proposal'),
    
    # API endpoints
    path('api/orders/', views.get_user_orders, name='get_user_orders'),
    path('api/user/orders/', views.get_user_orders_api, name='get_user_orders_api'),
    path('api/orders/<int:order_id>/attach/<int:performer_id>/', views.attach_performer_to_order, name='attach_performer'),
    path('api/performer/<int:performer_id>/busy-dates/', views.get_performer_busy_dates, name='get_performer_busy_dates'),
    path('api/performer/<int:performer_id>/tariffs/', views.get_performer_tariffs, name='get_performer_tariffs'),
    
    # Order detail API
    path('order/<int:order_id>/detail/', views.order_detail_api, name='order_detail_api'),
    path('order/<int:order_id>/respond/', views.order_respond_api, name='order_respond_api'),
    
    # Response management
    path('order/response/<int:response_id>/accept/', views.accept_response, name='accept_response'),
    path('order/response/<int:response_id>/reject/', views.reject_response, name='reject_response'),
    path('order/response/<int:response_id>/cancel/', views.cancel_response, name='cancel_response'),
    
    # Order management API
    path('order/<int:order_id>/cancel-api/', views.cancel_order_api, name='cancel_order_api'),
    path('order/<int:order_id>/complete-api/', views.complete_order_api, name='complete_order_api'),
    path('order/<int:order_id>/review-api/', views.create_review_api, name='create_review_api'),
    path('order/<int:order_id>/performer-cancel-booking-api/', views.performer_cancel_booking_api, name='performer_cancel_booking_api'),
    path('order/<int:order_id>/customer-cancel-booking-api/', views.customer_cancel_booking_api, name='customer_cancel_booking_api'),
    path('order/<int:order_id>/delete-api/', views.delete_order_api, name='delete_order_api'),
    path('order/<int:order_id>/accept-booking-api/', views.accept_booking_api, name='accept_booking_api'),
    path('order/<int:order_id>/reject-booking-api/', views.reject_booking_api, name='reject_booking_api'),
    
    # Test page for mobile menu
    path('test-mobile/', views.test_mobile, name='test_mobile'),
] 