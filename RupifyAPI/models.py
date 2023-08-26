from django.db import models
from CashAPI.models import RupifyUser

class DepositeUserModel(models.Model):
    user = models.ForeignKey(RupifyUser, on_delete=models.CASCADE)
    note_number = models.CharField(max_length=200)
    note_purpose = models.IntegerField()

class PendingNoteModel(models.Model):
    user = models.ForeignKey(RupifyUser, on_delete=models.CASCADE)
    note_number = models.CharField(max_length=200)
