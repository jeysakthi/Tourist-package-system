from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register_view, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('packages/', views.package_list, name='package_list'),
    path('package/<int:id>/', views.package_detail, name='package_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-package/', views.add_package, name='add_package'),
    path('vendor/register/', views.vendor_register, name='vendor_register'),
    path('package/book/<int:id>/', views.book_package, name='book_package'),
    path('pay/<int:id>/', views.initiate_payment, name='initiate_payment'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('packages/', views.package_list, name='package_list'),
    path('packages/<int:id>/', views.package_detail, name='package_detail'),
    path('admin/packages/', views.admin_package_approval, name='admin_package_approval'),
    path('register/user/', views.user_register_view, name='user_register'),
    path('register/vendor/', views.vendor_register_view, name='vendor_register'),
    path('vendor/package/edit/<int:package_id>/', views.edit_package, name='edit_package'),
    path('vendor/package/delete/<int:package_id>/', views.delete_package, name='delete_package'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('book/<int:package_id>/', views.create_booking, name='create_booking'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('approve-booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject-booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),


]
LOGIN_URL = '/login/'