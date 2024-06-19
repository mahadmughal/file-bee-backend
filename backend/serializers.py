from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = "__all__"

    def validate_email(self, value):
        # Check for unique email
        UserModel = get_user_model()
        if UserModel.objects.filter(email=value).exists():
            raise ValidationError("This email address is already registered.")
        return value
