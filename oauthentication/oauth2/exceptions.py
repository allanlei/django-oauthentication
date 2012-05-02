class OAuth2EmptyScopesError(Exception):
    def __init__(self):
        return super(OAuth2EmptyScopesError, self).__init__('OAuth2 scopes cannot be empty')
