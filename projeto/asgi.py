import os
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings'),
load_dotenv()
application = get_asgi_application()
