from django.urls import path 
from . import views

urlpatterns = [
    path('receipts/process', views.process, name='process'),
    path('receipts/<str:id>/points/', views.getPoints, name='getPoints'),
]
