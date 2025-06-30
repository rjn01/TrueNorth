from . import db
from datetime import datetime

class Emotion(db.Model):
    __tablename__ = 'emotions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    journal_id = db.Column(db.Integer,db.ForeignKey('journals.id'), nullable=False)
    emotion = db.Column(db.LargeBinary)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
