from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Custom serializer for the User model."""

    class Meta:
        model = User
        fields = ["id", "email"]
