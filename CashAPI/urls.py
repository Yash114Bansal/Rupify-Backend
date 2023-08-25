from django.urls import path
from . import views
urlpatterns = [
    path("notevalue/",views.NoteValueView.as_view()),
    path("get-otp/",views.SendOTPView.as_view()),
    path("verify-otp/",views.VerifyOTPView.as_view()),
]
