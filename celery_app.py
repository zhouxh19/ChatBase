from celery import Celery

app = Celery('data_chat_celery', broker='redis://localhost:6379/0', include=['server.celery.tasks'])
