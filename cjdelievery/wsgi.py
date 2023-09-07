"""
WSGI config for cjdelievery project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
# uwsgi --http :[포트번호] --home [가상환경 경로] --chdir [장고프로젝트폴더 경로] -w [wsgi 모듈이 있는 폴더].wsgi
# sudo /home/ubuntu/myvenv/bin/uwsgi -i /srv/django-deploy-delivery/.config/uwsgi/mysite.ini

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cjdelievery.settings')

application = get_wsgi_application()
