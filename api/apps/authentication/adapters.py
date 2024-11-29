from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the frontend email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        return f"{settings.WEB_APP_BASE_URL}/{settings.WEB_APP_VERIFY_EMAIL_PATH}?key={emailconfirmation.key}"
