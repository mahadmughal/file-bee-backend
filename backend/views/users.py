from django.contrib.auth import authenticate
from backend.serializers import UserSerializer, CustomTokenSerializer
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from backend.auth import CustomTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from backend.models.user import PasswordReset, CustomToken
from backend.mailers.password_reset_emailer import PasswordResetEmailer
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from django.db import transaction
from backend.models.file_conversion import DocumentConversion


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
            return JsonResponse({'error': 'Missing required fields: username or password'}, status=400)

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

            return JsonResponse({
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

            return JsonResponse({'error': error_messages[error_code]}, status=status.HTTP_401_UNAUTHORIZED)


class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data['email']

        if not email:
            return JsonResponse({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            password_reset = PasswordReset(
                email=email, token=token, user_id=user.pk)
            password_reset.save()

            # Sending reset link via email
            PasswordResetEmailer(password_reset.token, user).send_email()

            return JsonResponse({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Email is invalid"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated users

    def post(self, request):
        token = request.data['token']
        new_password = request.data['password']
        confirm_password = request.data['confirm_password']

        if new_password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        password_reset = PasswordReset.objects.get(token=token)

        if not password_reset:
            return JsonResponse({'error': 'Password reset token is invalid. Please try again!'}, status=status.HTTP_400_BAD_REQUEST)

        user = password_reset.user
        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)


class GetUserDetails(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the token from the request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'error': 'Invalid or missing token'}, status=status.HTTP_401_UNAUTHORIZED)

        token_key = auth_header.split(' ')[1]

        try:
            # Find the CustomToken
            custom_token = CustomToken.objects.get(key=token_key)

            # Check if the token is expired
            if custom_token.is_expired():
                return JsonResponse({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)

            # Get the user associated with the token
            user = custom_token.user

            # Serialize the user data
            serializer = UserSerializer(user)

            return JsonResponse(serializer.data, status=200)

        except CustomToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateUserProfile(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the token from the request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'error': 'Invalid or missing token'}, status=status.HTTP_401_UNAUTHORIZED)

        token_key = auth_header.split(' ')[1]

        try:
            # Find the CustomToken
            custom_token = CustomToken.objects.get(key=token_key)

            # Check if the token is expired
            if custom_token.is_expired():
                return JsonResponse({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)

            # Get the user associated with the token
            user = custom_token.user

            # Get the data from the request
            email = request.data.get('email')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')

            # Update the user fields if provided
            if email:
                user.email = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name

            try:
                user.full_clean()  # Validate the model
                user.save()
                serializer = UserSerializer(user)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except CustomToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class DeleteUserAccount(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request):
        # Get the token from the request headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Token '):
            return JsonResponse({'error': 'Invalid or missing token'}, status=status.HTTP_401_UNAUTHORIZED)

        token_key = auth_header.split(' ')[1]

        try:
            # Find the CustomToken
            custom_token = CustomToken.objects.get(key=token_key)

            # Check if the token is expired
            if custom_token.is_expired():
                return JsonResponse({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)

            # Get the user associated with the token
            user = custom_token.user

            # Delete associated records
            DocumentConversion.objects.filter(user=user).delete()
            CustomToken.objects.filter(user=user).delete()

            # Delete the user
            user.delete()

            return JsonResponse({'message': 'User account and all associated data have been permanently deleted.'}, status=status.HTTP_200_OK)

        except CustomToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
