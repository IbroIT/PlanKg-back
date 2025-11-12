from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


class GoogleLogin(SocialLoginView):
    """
    Google OAuth login endpoint using dj-rest-auth
    """
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:5173'
    client_class = OAuth2Client
    
    def post(self, request, *args, **kwargs):
        # dj-rest-auth expects 'id_token' or 'access_token'
        if 'id_token' not in request.data and 'access_token' in request.data:
            request.data._mutable = True
            request.data['id_token'] = request.data.get('access_token')
            request.data._mutable = False
        
        return super().post(request, *args, **kwargs)
