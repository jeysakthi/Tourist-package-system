from django.contrib import admin
from .models import Vendor, Package, Booking

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor', 'price', 'expiry_date', 'is_approved']
    list_filter = ['is_approved']
    actions = ['approve_packages']

    def approve_packages(self, request, queryset):
        queryset.update(is_approved=True)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'persons', 'status', 'razorpay_order_id', 'booking_date')
    fields = ('user', 'package', 'persons', 'status', 'razorpay_order_id', 'booking_date')  

admin.site.register(Vendor)
# admin.site.register(Booking)
