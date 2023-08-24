from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import RupifyUser

class RupifyUserCreationForm(UserCreationForm):
    class Meta:
        model = RupifyUser
        fields = ['aadhar_number', 'phone', 'first_name', 'last_name', 'user_Picture']
class RupifyUserChangeForm(UserChangeForm):
    class Meta:
        model = RupifyUser
        fields = ['phone', 'first_name', 'last_name', 'user_Picture']
