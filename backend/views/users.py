from django.contrib.auth import authenticate
from backend.serializers import UserSerializer, CustomTokenSerializer
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from backend.auth import CustomTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from backend.models.user import PasswordReset, CustomToken
from backend.emailers.password_reset_emailer import PasswordResetEmailer
from django.utils import timezone
from datetime import timedelta
import pdb


class UserRegistration(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):
        # Hash the password before saving the user
        user = serializer.save()
        user.set_password(serializer.validated_data["password"])
        user.save()


class UserLogin(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        # Validate required fields
        if not all((username, password)):
            return Response({'error': 'Missing required fields: username or password'}, status=400)

        user = authenticate(
            request,
            username=request.data["username"],
            password=request.data["password"],
        )

        if user:
            try:
                token = CustomToken.objects.get(user=user)

                if token.is_expired():
                    token.delete()
                    expiration_time = timezone.now() + timedelta(hours=2)
                    token = CustomToken.objects.create(
                        user=user, expires_at=expiration_time)
                    message = "New token created"
                else:
                    message = "Existing token returned"

            except CustomToken.DoesNotExist:
                expiration_time = timezone.now() + timedelta(hours=2)
                token = CustomToken.objects.create(
                    user=user, expires_at=expiration_time)
                message = "New token created"

            # Use the serializer to convert the token object to JSON
            serializer = CustomTokenSerializer(token)

            return Response({
                "token": serializer.data,
                "message": message
            }, status=200)

        else:
            # Authentication failed - provide specific error messages
            error_messages = {
                'nonexistent_user': 'Username does not exist.',
                'inactive_user': 'User account is inactive.',
                'wrong_password': 'Incorrect password.',
            }

            # Identify the specific authentication error (if possible)
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    error_code = 'inactive_user'
                else:
                    error_code = 'wrong_password'
            except User.DoesNotExist:
                error_code = 'nonexistent_user'
            except Exception as e:  # Catch any unexpected exceptions
                error_code = 'internal_error'

            return Response({'error': error_messages[error_code]}, status=401)


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data['email']

        if not email:
            return Response({'error': 'Email is required.'}, status=400)

        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            password_reset = PasswordReset(
                email=email, token=token, user_id=user.pk)
            password_reset.save()

            # Sending reset link via email
            PasswordResetEmailer(password_reset.token, user).send_email()

            return Response({'success': 'We have sent you a link to reset your password'}, status=200)
        else:
            return Response({"error": "Email is invalid"}, status=400)


class ResetPassword(APIView):
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated users

    def post(self, request):
        token = request.data['token']
        new_password = request.data['password']
        confirm_password = request.data['confirm_password']

        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=400)

        password_reset = PasswordReset.objects.get(token=token)

        if not password_reset:
            return Response({'error': 'Password reset token is invalid. Please try again!'}, status=400)

        user = password_reset.user
        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully.'}, status=200)


class GetUserDetails(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the token from the request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return Response({'error': 'Invalid or missing token'}, status=401)

        token_key = auth_header.split(' ')[1]

        try:
            # Find the CustomToken
            custom_token = CustomToken.objects.get(key=token_key)

            # Check if the token is expired
            if custom_token.is_expired():
                return Response({'error': 'Token has expired'}, status=401)

            # Get the user associated with the token
            user = custom_token.user

            # Serialize the user data
            serializer = UserSerializer(user)

            return Response(serializer.data, status=200)

        except CustomToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=401)
