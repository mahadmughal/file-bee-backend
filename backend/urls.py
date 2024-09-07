from django.urls import path

from backend.views.help_request import SubmitHelpRequestView

from .views import *

urlpatterns = [
    path('api/user/register/', UserRegistration.as_view(),
         name='user_registration'),
    path('api/user/login/', UserLogin.as_view(), name='user_login'),
    path('api/user/request_reset_password/', RequestPasswordReset.as_view(),
         name='request_reset_password'),
    path('api/user/reset_password/',
         ResetPassword.as_view(), name='reset_password'),
    path('api/user/',
         GetUserDetails.as_view(), name='user_details'),
    path('api/user/profile',
         UpdateUserProfile.as_view(), name='user_profile'),
    path('api/user/delete_account',
         DeleteUserAccount.as_view(), name='delete_account'),
    path('', UploadAndCreateDocumentView.as_view(),
         name='upload_and_create_document'),
    path('target_conversions/', TargetConversionsView.as_view(),
         name='target_conversions'),
    path('send_help_request/', SubmitHelpRequestView.as_view(),
         name='send_help_request'),
]
