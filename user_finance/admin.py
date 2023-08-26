from django.contrib import admin
from .models import PurposeModel,UserNotesModel

@admin.register(PurposeModel)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ["user","purpose"]

@admin.register(UserNotesModel)
class UserNptes(admin.ModelAdmin):
    list_display = ["user","note"]


# Register your models here.
