from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.backends import ModelBackend

from models import OAuth2User as User

import requests
import simplejson as json
import logging
logger = logging.getLogger(__name__)


class AuthenticationBackend(ModelBackend):
    supports_inactive_user = False
    endpoint = None

    def __init__(self, *args, **kwargs):
        if self.endpoint is None:
            raise ImproperlyConfigured('OAuth 2.0 backend {backend} is missing the user data endpoint'.format(backend=__name__))
        return super(AuthenticationBackend, self).__init__(*args, **kwargs)
    
    def authenticate(self, access_token=None, endpoint=None):
        if access_token is None:
            return None

        if endpoint != self.endpoint:
            return None
        
        credentials = self.get_credentials(access_token)
        user = None
        try:
            user = self.find_user(**credentials)
        except User.DoesNotExist:
            pass
        
        if user is None:
            if hasattr(self, 'create_user'):
                user = self.create_user(**credentials)
        return user
    
    def get_credentials(self, access_token):
        response = requests.get(self.get_endpoint(), data={
            'access_token': access_token,
        })
        
        data = None
        if response.status_code != requests.codes.ok:
            logger.info(response.text)
        else:
            data = json.loads(response.text)
        return data

    def find_user(self, **credentials):
        return User.objects.get(**credentials)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
