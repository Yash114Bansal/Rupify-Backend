from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .forms import RupifyUserCreationForm, RupifyUserChangeForm
from .models import RupifyUser,CashValueModel

class RupifyUserAdmin(UserAdmin):
    add_form = RupifyUserCreationForm
    form = RupifyUserChangeForm
    model = RupifyUser

    list_display = ['aadhar_number', 'phone', 'first_name', 'last_name', 'user_Picture']
    list_filter = ["aadhar_number", "is_staff", "is_active"]
    fieldsets = (
        (None, {"fields": ("aadhar_number",'password', "phone", "first_name", "last_name", "user_Picture")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ('aadhar_number','password1','password2', 'phone', 'first_name', 'last_name', 'user_Picture', "is_staff", "is_active"),
        }),
    )
    search_fields = ("aadhar_number",)
    ordering = ("aadhar_number",)


admin.site.register(RupifyUser, RupifyUserAdmin)

@admin.register(CashValueModel)
class CashValueAdmin(admin.ModelAdmin):
    list_display = ["note_number","note_amount"]
