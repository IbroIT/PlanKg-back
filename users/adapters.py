from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new User instance using information provided in the signup form.
        """
        user = super().save_user(request, user, form, False)
        user.role = 'provider'  # Everyone is a provider by default
        if commit:
            user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        Populates user information from social provider data.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Generate unique username if it already exists
        email = data.get('email', '')
        base_username = email.split('@')[0] if email else 'user'
        
        # Check if username exists and make it unique
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user.username = username
        
        # Extract additional info from Google
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            user.first_name = extra_data.get('given_name', '')
            user.last_name = extra_data.get('family_name', '')
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a new User instance using information from social login.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Set default role for social login users
        if not hasattr(user, 'role') or not user.role:
            user.role = 'provider'  # Everyone is a provider
            user.save()
        
        return user
