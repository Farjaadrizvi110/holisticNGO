import os
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HFC.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
