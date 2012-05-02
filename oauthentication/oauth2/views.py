from django.core.exceptions import ImproperlyConfigured

import oauthentication as djauth

import simplejson as json
import urllib
import requests
import logging
logger = logging.getLogger(__name__)



class OAuth2ClientIdMixin(object):
    oauth2_client_id = None
    
    def get_oauth2_client_id(self):
        if self.oauth2_client_id:
            return self.oauth2_client_id
        raise ImproperlyConfigured('Provide oauth2_client_id')

class OAuth2ClientSecretMixin(object):
    oauth2_client_secret = None
    
    def get_oauth2_client_secret(self):
        if self.oauth2_client_secret:
            return self.oauth2_client_secret
        raise ImproperlyConfigured('Provide oauth2_client_secret')

class OAuth2RedirectUriMixin(object):
    oauth2_redirect_uri = None
    
    def get_oauth2_redirect_uri(self):
        if self.oauth2_redirect_uri:
            uri = self.oauth2_redirect_uri
        else:
            raise ImproperlyConfigured('Provide oauth2_redirect_uri. Must be an absolute URI.')
        return self.request.build_absolute_uri(str(uri))





class LoginView(OAuth2RedirectUriMixin, OAuth2ClientIdMixin, djauth.views.LoginView):
    oauth2_authorization_endpoint = None
    oauth2_scopes = None
    oauth2_scopes_empty = True
    oauth2_response_type = 'code'
    oauth2_state = None

    def get_oauth2_scopes(self):
        scopes = []
        if isinstance(self.oauth2_scopes, list) or isinstance(self.oauth2_scopes, tuple):
            scopes = list(self.oauth2_scopes)
        elif isinstance(self.oauth2_scopes, str):
            scopes = self.oauth2_scopes.split()

        if not self.oauth2_scopes_empty and not scopes:
            raise djauth.exceptions.OAuth2EmptyScopesError()
        return scopes
        
    def get_oauth2_authorization_endpoint(self):
        if self.oauth2_authorization_endpoint:
            return self.oauth2_authorization_endpoint
        raise ImproperlyConfigured('Provide oauth2_authorization_endpoint')

    def get_oauth2_respone_type(self):
        if self.oauth2_response_type:
            return self.oauth2_response_type
        raise ImproperlyConfigured('Provide oauth_response_type. "code" recommended.')

    def get_oauth2_state(self):
        if self.oauth2_state:
            state = self.oauth2_state
        else:
            state = None
        return state

    def get_oauth2_redirect_uri(self):
        return self.request.build_absolute_uri(self.get_authentication_callback_url())

    def get_oauth2_authorization_parameters(self):
        params = {
            'client_id': self.get_oauth2_client_id(),
            'response_type': self.get_oauth2_respone_type(),
            'scope': ' '.join(self.get_oauth2_scopes()),        #Add only if not empty
            'redirect_uri': self.request.build_absolute_uri(self.get_authentication_callback_url()),
            'state': self.get_oauth2_state() or '',
        }
        return params
        
    def get_authentication_url(self):
        return '{endpoint}?{params}'.format(
            endpoint=self.get_oauth2_authorization_endpoint(), 
            params=urllib.urlencode(
                self.get_oauth2_authorization_parameters(),
            )
        )

class AuthenticationView(OAuth2RedirectUriMixin, OAuth2ClientIdMixin, OAuth2ClientSecretMixin, djauth.views.AuthenticationView):
    oauth2_code_field = 'code'
    oauth2_access_endpoint = None
    
    def get_oauth2_code_field(self):
        if self.oauth2_code_field:
            field = self.oauth2_code_field
        else:
            raise ImproperlyConfigured('Provide oauth2_code_field')
        return field
    
    def get_oauth2_access_endpoint(self):
        if self.oauth2_access_endpoint:
            endpoint = self.oauth2_access_endpoint
        else:
            raise ImproperlyConfigured('Provide oauth2_access_endpoint')
        return endpoint
        
    def get_form_kwargs(self):
        kwargs = super(AuthenticationView, self).get_form_kwargs()
        kwargs.update({
            'oauth2_redirect_uri': self.get_oauth2_redirect_uri(),
        })
        return kwargs
