import sys
import os

project_home = '/home/catttnyz/Katteleya-coffee'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cattleya_coffee.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
