from django.urls import path
from . import views
urlpatterns = [
    path("",views.UserDetailsView.as_view()),
    path("history/",views.HistoryView.as_view()),
    path("get-name/",views.GetNameView.as_view()),
]
