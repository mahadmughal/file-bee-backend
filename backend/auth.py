from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import CustomToken
import pdb


class CustomTokenAuthentication(TokenAuthentication):
    model = CustomToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if token.is_expired():
            raise AuthenticationFailed('Token has expired')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        return (token.user, token)
