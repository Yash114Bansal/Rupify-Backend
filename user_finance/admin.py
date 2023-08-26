from django.contrib import admin
from .models import PurposeModel,UserNotesModel,HistoryModel

@admin.register(PurposeModel)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ["user","purpose"]

@admin.register(UserNotesModel)
class UserNotes(admin.ModelAdmin):
    list_display = ["user","note"]

@admin.register(HistoryModel)
class UserNptes(admin.ModelAdmin):
    list_display = ["user","second_user","amount","time"]

