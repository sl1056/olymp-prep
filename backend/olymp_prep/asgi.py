<<<<<<< Updated upstream
"""
ASGI config for olymp_prep project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
<<<<<<< Updated upstream

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "olymp_prep.settings")

application = get_asgi_application()
=======
=======
import os
>>>>>>> Stashed changes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olymp_prep.settings')

from django.conf import settings
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from channels.routing import ProtocolTypeRouter, URLRouter

django_asgi_app = get_asgi_application()
if settings.DEBUG:
    django_asgi_app = ASGIStaticFilesHandler(django_asgi_app)

def websocket_application():
    # Delay imports until Django app registry is initialized.
    from pvp.routing import websocket_urlpatterns
    from pvp.middleware import TokenAuthMiddleware
    return TokenAuthMiddleware(URLRouter(websocket_urlpatterns))

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": websocket_application(),
})
>>>>>>> Stashed changes
