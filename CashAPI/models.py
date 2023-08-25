from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager
from django.utils import timezone

class RupifyUser(AbstractUser):
    username = None
    aadhar_number = models.CharField(max_length=12, unique=True, primary_key=True)
    phone = models.CharField(max_length=10, unique=True)
    user_Picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = 'aadhar_number'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.aadhar_number

class CashValueModel(models.Model):
    note_number = models.CharField(max_length=200)
    note_amount = models.IntegerField()

class OTP(models.Model):
    user = models.ForeignKey(RupifyUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()

    def has_expired(self):
        return self.expiry_time < timezone.now()

    def __str__(self):
        return f"OTP for {self.user.username}"