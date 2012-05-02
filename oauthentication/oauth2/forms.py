from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
from django.contrib.auth import forms as auth

#import base
#import requests
#import simplejson as json
import logging
logger = logging.getLogger(__name__)



class LoginForm(base.LoginForm):
    pass

class AuthenticationForm(auth.AuthenticationForm):
    error_messages = {
        'invalid_login': _('No account could be found with that OAuth account'),
        'inactive': _('This account is inactive.'),
        'token_error': _('Token could not be retrieved from OAuth provider'),
    }
    oauth2_token_endpoint = None
    oauth2_redirect_uri = None

    code = forms.CharField()

    def __init__(self, *args, **kwargs):
        if not self.oauth2_redirect_uri:
            self.oauth2_redirect_uri = kwargs.pop('oauth2_redirect_uri', None)
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        
        if not self.oauth2_token_endpoint:
            raise ImproperlyConfigured('OAuth endpoint required.')

    def authenticate(self):
        data = self.cleaned_data
        data.update({
            'grant_type': 'authorization_code',
            'client_id': self.get_oauth2_client_id(),
            'client_secret': self.get_oauth2_client_secret(),
            'redirect_uri': self.get_oauth2_redirect_uri(),
        })
        logger.info(self.get_oauth2_token_endpoint())
        logger.info(data)
        response = requests.post(self.get_oauth2_token_endpoint(), data=data)
        
        if response.status_code != requests.codes.ok:
            errors = json.loads(response.text)
            logger.info(errors)
            raise forms.ValidationError(self.error_messages['token_error'])
            
        tokens = json.loads(response.text)
        logger.info(tokens)
        self.access_token = tokens.get('access_token', None)
        self.token_type = tokens.get('token_type', None)
        self.expires_in = tokens.get('expires_in', 0)
        self.id_token = tokens.get('id_token', None)
        return authenticate(access_token=self.access_token)

    def get_oauth2_token_endpoint(self):
        return str(self.oauth2_token_endpoint)
        
    def get_oauth2_client_id(self):
        return settings.OAUTH2_GOOGLEAPPS_CLIENT_ID

    def get_oauth2_client_secret(self):
        return settings.OAUTH2_GOOGLEAPPS_CLIENT_SECRET

    def get_oauth2_redirect_uri(self):
        return self.oauth2_redirect_uri
#        return str(settings.OAUTH2_GOOGLEAPPS_REDIRECT_URI)
