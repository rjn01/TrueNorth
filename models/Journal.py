from . import db
from datetime import datetime

class Journal(db.Model):
    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    journal_input = db.Column(db.LargeBinary, nullable=False)
    sentiment = db.Column(db.LargeBinary)
    themes = db.Column(db.LargeBinary)
    empathy = db.Column(db.LargeBinary)
    input_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
