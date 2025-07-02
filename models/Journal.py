from . import db
from datetime import datetime

class Journal(db.Model):
    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    journal_input = db.Column(db.LargeBinary, nullable=False)
    feedback = db.Column(db.LargeBinary)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    emotions = db.relationship('Emotion', backref='journal', lazy=True)
    themes = db.relationship('Theme', backref='journal', lazy=True)
    scores = db.relationship('Score', backref='journal', lazy=True)

