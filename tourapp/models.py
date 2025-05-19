# from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name

class Package(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    image = models.ImageField(upload_to='packages/')
    expiry_date = models.DateTimeField()
    location = models.CharField(max_length=100, default='Unknown')
    is_approved = models.BooleanField(default=False)
    is_top_package = models.BooleanField(default=False)
    is_budget_friendly = models.BooleanField(default=False)


    def is_expired(self):
        return self.expiry_date < timezone.now()

    def __str__(self):
        return self.title

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    persons = models.PositiveIntegerField(default=1)
    booking_date = models.DateTimeField(default=timezone.now, editable=True)
    status = models.CharField(max_length=20, default='Pending')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.title}"
