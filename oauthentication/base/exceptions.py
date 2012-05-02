class ResponseNotAuthenticException(Exception):
    def __init__(self):
        return super(ResponseNotAuthenticException, self).__init__('AuthenticationResponseNotValid')
