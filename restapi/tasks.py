from celery import shared_task
from fabric.api import execute
from builder import start


@shared_task
def build():
    execute(start)