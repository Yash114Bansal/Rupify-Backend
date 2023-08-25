from django.contrib import admin
from .models import DepositeUserModel,PendingNoteModel
# Register your models here.

@admin.register(DepositeUserModel)
class OTPAdmin(admin.ModelAdmin):
    list_display = ["user","note_number","note_purpose"]

@admin.register(PendingNoteModel)
class PendingNoteAdmin(admin.ModelAdmin):
    list_display = ["user","note_number"]