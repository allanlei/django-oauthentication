from oauthentication.oauth2.backends import AuthenticationBackend as OAuth2AuthenticationBackend

import requests
import simplejson as json
import logging
logger = logging.getLogger(__name__)


class BaseGoogleAuthenticationBackend(OAuth2AuthenticationBackend):
    endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'

    def get_credentials(self, access_token):
        response = requests.get(self.endpoint, headers={
            'Authorization': 'Bearer {access_token}'.format(access_token=access_token)
        })
        
        data = None
        if response.status_code != requests.codes.ok:
            logger.info(response.text)
        else:
            data = json.loads(response.text)
        return data

    def find_user(self, **credentials):
        logger.info(credentials)
        return super(BaseGoogleAuthenticationBackend, self).find_user(**credentials)

class EmailAuthenticationBackend(BaseGoogleAuthenticationBackend):
    verified_emails_only = True
    
    def find_user(self, **credentials):
        if self.verified_emails_only and credentials.get('verified_email', False):
            return None

        email = credentials.get('email', None)
        if email is None:
            return None

        return super(EmailAuthenticationBackend, self).find_user(**{
            'email': email,
        })

class GPlusAuthenticationBackend(BaseGoogleAuthenticationBackend):
    def find_user(self, **credentials):
        link = credentials.get('link', None)
        if link is None:
            return None
            
        return super(GPlusAuthenticationBackend, self).find_user(**{
            'link': link,
        })
