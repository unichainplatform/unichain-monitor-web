from celery import shared_task
from fabric.api import execute
from restapi.builder import start
from time import sleep


@shared_task
def build():
    execute(start)


@shared_task
def sleepp():
    sleep(20)