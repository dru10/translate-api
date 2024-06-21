from time import sleep

from celery import shared_task
from transformers import pipeline

translators = {}


@shared_task
def hello():
    sleep(20)
    return "Hello, world!"


def setup_translator(source: str, target: str):
    key = f"{source}-{target}"
    if key not in translators:
        print(f"Setting up translator for {source} to {target}")
        translators[key] = pipeline(
            f"translation_{source}_to_{target}", model="google-t5/t5-small"
        )

    print(f"Translator for {source} to {target} is ready")
    return translators[key]


@shared_task
def translate(text: str, source: str, target: str):
    translator = setup_translator(source, target)
    return translator(text)
