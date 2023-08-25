from django.urls import path
from . import views
urlpatterns = [
    path("notevalue/",views.NoteValue.as_view()),
]
