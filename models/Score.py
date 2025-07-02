from . import db
from datetime import datetime

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    journal_id = db.Column(db.Integer,db.ForeignKey('journals.id'), nullable=False)
    severity = db.Column(db.LargeBinary)
    total_score = db.Column(db.LargeBinary)
    score_type = db.Column(db.String)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
