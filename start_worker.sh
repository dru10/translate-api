watchmedo auto-restart --directory=./ --pattern=tasks.py --recursive -- celery --app=src.celery_app.app worker --loglevel INFO