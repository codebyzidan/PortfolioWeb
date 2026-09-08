"""
Startup file Passenger untuk cPanel (Setup Python App).

Passenger mengimpor file ini dan memakai variabel `application` sebagai
titik masuk WSGI. Di cPanel, field "Application startup file" harus
diisi dengan: passenger_wsgi.py
"""

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()