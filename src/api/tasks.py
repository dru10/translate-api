from time import sleep

from celery import shared_task
from transformers import pipeline

translator = pipeline("translation_en_to_ro", model="google-t5/t5-small")


@shared_task
def hello():
    sleep(20)
    return "Hello, world!"


@shared_task
def translate(text: str):
    return translator(text)
