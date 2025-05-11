import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MotoRentCL.settings')

# 🚀 Fuerza migraciones en Render
import django
django.setup()

from django.core.management import call_command
import traceback

try:
    print("🔥 Ejecutando migraciones desde wsgi.py...")
    call_command('migrate', interactive=False)
    print("✅ Migraciones completadas correctamente.")
except Exception as e:
    print("❌ Error ejecutando migraciones:")
    traceback.print_exc()

application = get_wsgi_application()
