from oauthentication.contrib.google.backends import OAuth2AuthenticationBackend as GoogleOAuth2AuthenticationBackend


class OAuth2AuthenticationBackend(GoogleOAuth2AuthenticationBackend):
    oauth2_provider_alias = 'googleapps'
