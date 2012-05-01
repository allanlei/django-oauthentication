class AuthenticationBackend(object):
    supports_inactive_user = False
    create_unknown_user = True
    credentials_fields = None

    def __init__(self, *args, **kwargs):
        self.get_credential_fields()
        return super(AuthenticationBackend, self).__init__(*args, **kwargs)

    def authenticate(self, **credentials):
        user = None
        credentials = self.get_credentials(**credentials)
        if not credentials:
            return None
            
        try:
            user = User.objects.get(**credentials())
        except User.DoesNotExist:
            if self.create_unknown_user:
                user = User()
                logger.info('create new user')
#                send user authentication modification signal
#                self.configure_user(user)      user.set_unusable_password()
#                user.save()
                return None
        return user

    def get_credentials(self, **credentials):
        if not credentials:
            return None

        fields = self.get_credentials_fields()
        if fields is not None:
            return dict((key, val) for key, val in credentials.items() if key in fields)
        return credentials

    def get_credential_fields(self):
        if self.credentials_fields is None or not len(self.credentials_fields):
            fields = self.credentials_fields
        else:
            raise ImproperlyConfigured('oauthentication backends require credentials_fields to be not empty')
        return fields
