import os
import sys
from pathlib import Path
# ensure project root is on sys.path so DJANGO_SETTINGS_MODULE imports work
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_project.settings')
import django
django.setup()
from django.conf import settings
# allow test client host
settings.ALLOWED_HOSTS = ['testserver']
from django.test import Client

paths = ['/', '/inicio/', '/nosotros/', '/obras/', '/iniciativas/', '/contacto/']
client = Client()
print('Running smoke tests:')
for p in paths:
    r = client.get(p)
    print(p, '->', r.status_code)
    # optional: show if template used
    try:
        tmpl = ','.join([t.name or '<string>' for t in r.templates])
    except Exception:
        tmpl = ''
    print('  templates:', tmpl)
