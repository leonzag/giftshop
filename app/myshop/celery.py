import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")

app = Celery("myshop")

# Загружаем конфигурацию Celery из настроек Django.
# Все настройки Celery должны быть с префиксом 'CELERY_'.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживаем задачи в файлах tasks.py каждого приложения Django.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
