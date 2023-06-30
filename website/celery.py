from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную окружения с именем вашего проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')


# Создайте экземпляр Celery
app = Celery('website')


# Загрузите настройки проекта из файла настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач в приложениях Django
app.autodiscover_tasks()
