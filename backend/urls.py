from django.urls import path

from .views import *

urlpatterns = [
    path('api/user/register/', UserRegistration.as_view(),
         name='user_registration'),
    path('api/user/login/', UserLogin.as_view(), name='user_login'),
    path('', file_conversion.upload_and_create_document,
         name='upload_and_create_document'),
    path('target_conversions/', file_conversion.target_conversions,
         name='target_conversions'),
    path('documents/', file_conversion.index, name='index')
]
