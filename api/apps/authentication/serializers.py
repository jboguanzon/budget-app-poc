from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DJRestAuthRegisterSerializer,
)
from dj_rest_auth.serializers import LoginSerializer as DJRestAuthLoginSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class LoginSerializer(DJRestAuthLoginSerializer):
    username = None


class RegisterSerializer(DJRestAuthRegisterSerializer):
    username = None

    def validate_email(self, email):
        """
        Check if the email already exists in the database and if the user is verified.
        """
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and (
                User.objects.filter(email=email).exists()
                or EmailAddress.objects.filter(email=email).exists()
            ):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."),
                )
        return email
