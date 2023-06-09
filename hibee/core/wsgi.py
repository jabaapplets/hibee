import hibee
from hibee.core.handlers.wsgi import WSGIHandler


def get_wsgi_application():
    """
    The public interface to Hibee's WSGI support. Return a WSGI callable.

    Avoids making hibee.core.handlers.WSGIHandler a public API, in case the
    internal WSGI implementation changes or moves in the future.
    """
    hibee.setup(set_prefix=False)
    return WSGIHandler()
