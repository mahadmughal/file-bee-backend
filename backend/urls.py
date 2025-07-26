from django.urls import path

from backend.views.help_request import SubmitHelpRequestView
from backend.views.ocr import OCRView

from .views import *

urlpatterns = [
    path('user/register/', UserRegistration.as_view(),
         name='user_registration'),
    path('user/login/', UserLogin.as_view(), name='user_login'),
    path('user/request_reset_password/', RequestPasswordReset.as_view(),
         name='request_reset_password'),
    path('user/reset_password/',
         ResetPassword.as_view(), name='reset_password'),
    path('user/',
         GetUserDetails.as_view(), name='user_details'),
    path('user/profile',
         UpdateUserProfile.as_view(), name='user_profile'),
    path('user/delete_account',
         DeleteUserAccount.as_view(), name='delete_account'),
    path('convert/', UploadAndCreateDocumentView.as_view(),
         name='upload_and_create_document'),
    path('target_conversions/', TargetConversionsView.as_view(),
         name='target_conversions'),
    path('send_help_request/', SubmitHelpRequestView.as_view(),
         name='send_help_request'),
    path('ocr/', OCRView.as_view(), name='ocr_view'),
]
