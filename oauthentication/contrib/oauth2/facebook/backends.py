from oauthentication.backends.oauth2 import AuthenticationBackend


class OAuth2AuthenticationBackend(AuthenticationBackend):
    endpoint = 'https://graph.facebook.com/me/'
