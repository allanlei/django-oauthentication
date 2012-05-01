from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
import simplejson as json

import urllib2, urllib
from urlparse import urlparse


class OAuth2Mixin(object):
    oauth2_client_id = None
    oauth2_redirect_uri = None
    oauth2_redirect_uri_lazy = None

    def get_oauth2_client_id(self):
        if self.oauth2_client_id:
            return self.oauth2_client_id
        raise ImproperlyConfigured('Provide oauth2_client_id')

    def get_oauth2_redirect_uri(self):
        if self.oauth2_redirect_uri:
            uri = self.oauth2_redirect_uri
        elif self.oauth2_redirect_uri_lazy:
            uri = reverse(self.oauth2_redirect_uri_lazy)
        else:
            raise ImproperlyConfigured('Provide oauth2_redirect_uri')
        return self.request.build_absolute_uri(uri)

class OAuth2LoginMixin(object):
    oauth2_authorization_endpoint = None
    oauth2_response_type = 'code'
    oauth2_scopes = None

    def get_oauth2_authorization_endpoint(self):
        if self.oauth2_authorization_endpoint:
            return self.oauth2_authorization_endpoint
        raise ImproperlyConfigured('Provide oauth2_authorization_endpoint')

    def get_oauth2_authorization_parameters(self):
        params = {
            'client_id': self.get_oauth2_client_id(),
            'response_type': self.get_oauth2_respone_type(),
        }
        
        scopes = self.get_oauth2_scopes()
        if scopes:
            params['scope'] = ' '.join(scopes)
            
        redirect_uri = self.get_oauth2_redirect_uri()
        if redirect_uri:
            parser = urlparse(redirect_uri)
            if not parser.scheme or not parser.netloc:
                raise ImproperlyConfigured('oauth2_redirect_uri needs to be an absolute URL.')
            params['redirect_uri'] = redirect_uri
        
        state = self.get_oauth2_state()
        if state:
            params['state'] = state
        return params
        
    def get_oauth2_scopes(self):
        scopes = []
        if isinstance(self.oauth2_scopes, list) or isinstance(self.oauth2_scopes, tuple):
            scopes = list(self.oauth2_scopes)
        elif isinstance(self.oauth2_scopes, str):
            scopes = self.oauth2_scopes.split()
        return scopes

    def get_oauth2_state(self):
        return None

    def get_oauth2_respone_type(self):
        if self.oauth2_response_type:
            return self.oauth2_response_type
        raise ImproperlyConfigured('Provide oauth_response_type. "code" recommended.')

    def get_oauth2_login_url(self):
        return '{endpoint}?{params}'.format(endpoint=self.get_oauth2_authorization_endpoint(), params=urllib.urlencode(
            self.get_oauth2_authorization_parameters()
        ))

class OAuth2AuthenticationMixin(object):
    oauth2_authorization_code_name = 'code'
    oauth2_client_secret = None

    def get_oauth2_client_secret(self):
        if self.oauth2_client_secret:
            return self.oauth2_client_secret
        raise ImproperlyConfigured('Provide oauth2_client_secret')

    def get_oauth2_access_token(self):
        auth_code = self.request.GET.get(self.get_oauth_authorization_code_name(), None)
        
        if auth_code:
            try:
                #Need some more modularization
                request = urllib2.Request(
                    url=self.get_oauth2_access_endpoint(),
                    data=urllib.urlencode({
                        'code': auth_code,
                        'client_id': self.get_oauth2_client_id(),
                        'client_secret': self.get_oauth2_client_secret(),
                        'redirect_uri': self.get_oauth2_redirect_uri(),
                        'grant_type': 'authorization_code',
                    })
                )
        
                request_open = urllib2.urlopen(request)
                response = request_open.read()
                request_open.close()
                tokens = json.loads(response)
                return tokens.get('access_token', None), tokens.get('refresh_token', None), tokens.get('expires', 0)
            except urllib2.HTTPError, err:
                pass
        return None, None, None
        
    def get_oauth_authorization_code_name(self):
        return self.oauth2_authorization_code_name

    def get_oauth2_access_endpoint(self):
        if self.oauth2_access_endpoint:
            return self.oauth2_access_endpoint
        raise ImproperlyConfigured('Provide oauth2_access_endpoint')
