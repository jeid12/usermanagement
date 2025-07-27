from django.db import models

from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    SELLER = 'seller', 'Seller'
    CUSTOMER = 'customer', 'Customer'

class User(AbstractUser):

    
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/profile/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

