"""
Views and functions for serving static files. These are only to be used during
development, and SHOULD NOT be used in a production setting.

"""
import os
import posixpath

from hibee.conf import settings
from hibee.contrib.staticfiles import finders
from hibee.http import Http404
from hibee.views import static


def serve(request, path, insecure=False, **kwargs):
    """
    Serve static files below a given point in the directory structure or
    from locations inferred from the staticfiles finders.

    To use, put a URL pattern such as::

        from hibee.contrib.staticfiles import views

        path('<path:path>', views.serve)

    in your URLconf.

    It uses the hibee.views.static.serve() view to serve the found files.
    """
    if not settings.DEBUG and not insecure:
        raise Http404
    normalized_path = posixpath.normpath(path).lstrip("/")
    absolute_path = finders.find(normalized_path)
    if not absolute_path:
        if path.endswith("/") or path == "":
            raise Http404("Directory indexes are not allowed here.")
        raise Http404("'%s' could not be found" % path)
    document_root, path = os.path.split(absolute_path)
    return static.serve(request, path, document_root=document_root, **kwargs)
