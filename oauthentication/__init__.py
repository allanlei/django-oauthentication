from django.contrib.auth import load_backend
from django.conf import settings


def authenticate(backend_path, **credentials):
    if backend_path not in settings.AUTHENTICATION_BACKENDS:
        raise Exception('{backend} is not in AUTHENTICATION_BACKENDS'.format(backend_path))
    user = None
    backend = load_backend(backend_path)
    
    try:
        user = backend.authenticate(**credentials)
    except TypeError:
        # This backend doesn't accept these credentials as arguments.
        pass
    # Annotate the user object with the path of the backend.
    if user is not None:
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    return user
