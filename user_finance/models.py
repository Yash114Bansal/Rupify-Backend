from django.db import models
from CashAPI.models import RupifyUser

class PurposeModel(models.Model):
    user = models.ForeignKey(RupifyUser, on_delete=models.CASCADE)
    purpose = models.IntegerField()

class UserNotesModel(models.Model):
    user = models.ForeignKey(RupifyUser, on_delete=models.CASCADE)
    note = models.CharField(max_length=200,unique=True)