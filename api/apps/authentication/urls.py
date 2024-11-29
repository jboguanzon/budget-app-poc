from dj_rest_auth.app_settings import api_settings
from django.urls import include, path

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("register/", include("dj_rest_auth.registration.urls")),
]

if api_settings.USE_JWT:
    from dj_rest_auth.jwt_auth import get_refresh_view
    from rest_framework_simplejwt.views import TokenVerifyView

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    ]
