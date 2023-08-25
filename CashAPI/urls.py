from django.urls import path
from . import views
urlpatterns = [
    path("notevalue/",views.NoteValue.as_view()),
    path("get-otp/",views.SendOTP.as_view()),
    path("verify-otp/",views.VerifyOTP.as_view()),
]
