from django.urls import path
from . import views

urlpatterns = [
    path("deposite/",views.DepositedMoneyView.as_view()),
    path("get-money/",views.GetMoneyView.as_view()),
    path("transfer/",views.TransferNoteView.as_view()),
    path("get_pending_notes/",views.GetPendingNoteView.as_view()),
    
]

