from django.urls import path

from . import views

urlpatterns = [
    path('api/', views.TxnView.as_view()),
]