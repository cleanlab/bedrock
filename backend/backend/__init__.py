# Flask app config

from flask import Flask

app = Flask(__name__)

import os

env = os.environ
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{env['DB_USERNAME']}:{env['DB_PASSWORD']}@{env['DB_HOST']}:{env['DB_PORT']}/{env['DB_NAME']}"

from backend.models import db

db.app = app
db.init_app(app)

import backend.controllers

# Celery config

from celery import Celery, Task


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


app.config.from_mapping(
    CELERY={
        "broker_url": "redis://redis",
        "result_backend": "redis://redis",
        "task_ignore_result": True,
    }
)
celery_app = celery_init_app(app)

# Celery beat config

from celery.schedules import crontab
import backend.tasks.user

celery_app.conf.beat_schedule = {
    "clear status at midnight": {
        "task": "backend.tasks.user.clear_status",
        "schedule": crontab(hour=0),
    }
}
