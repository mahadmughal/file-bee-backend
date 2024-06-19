from django.contrib.auth import authenticate
from backend.serializers import UserSerializer
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from backend.models import PasswordReset
from backend.emailers.password_reset_emailer import PasswordResetEmailer


class UserRegistration(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

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
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
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
