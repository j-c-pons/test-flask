#import app
from flask import current_app
with current_app.app_context():
    current_app.db.drop_all()
    current_app.db.create_all()
