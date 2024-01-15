from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload_and_create_document, name='upload_and_create_document'),
    path('target_conversions/', views.target_conversions, name='target_conversions'),
    path('documents/', views.index, name='index')
]