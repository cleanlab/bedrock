from backend import db, celery_app
from backend.models import User


@celery_app.task
def clear_status():
    User.query.update({User.status: None})
    db.session.commit()
