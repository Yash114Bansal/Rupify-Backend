from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager

class RupifyUser(AbstractUser):
    username = None
    aadhar_number = models.CharField(max_length=12, unique=True, primary_key=True)
    phone = models.CharField(max_length=10, unique=True)
    user_Picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    objects = UserManager()

    # Using 'aadhar_number' as the primary identifier for authentication
    USERNAME_FIELD = 'aadhar_number'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.first_name

class CashValueModel(models.Model):
    note_number = models.CharField(max_length=200)
    note_amount = models.IntegerField()
    