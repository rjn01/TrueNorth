from models import db, Journal
from models.Score import Score
from models.Emotion import Emotion
from models.Theme import Theme
from datetime import datetime
from utils.encryption_utils import EncryptionManager
from sqlalchemy import text
from collections import Counter
from logger import logger
from datetime import timedelta
encryption = EncryptionManager()

def save_journal_entry(daily_text: str, response: dict):
    print("inside save journal")
    phq9 = response.get("depression", "")
    gad7 = response.get("anxiety", "")
    themes = response.get("themes", [])
    emotions = response.get("emotions", [])
    feedback = response.get("feedback", "")
    
    print("above journal")
    journal = Journal(
        journal_input=encryption.encrypt(daily_text),
        feedback=encryption.encrypt(feedback),
        created_time=datetime.utcnow()
    )
    print("above journal")
    db.session.add(journal)
    db.session.commit()

    if phq9:
        score = Score(
            journal_id=journal.id,
            severity=encryption.encrypt(phq9.get("severity")),
            total_score=encryption.encrypt(phq9.get("total_score")),
            score_type="depression",
            created_time=datetime.utcnow()
        )
        db.session.add(score)

    if gad7:
        score = Score(
            journal_id=journal.id,
            severity=encryption.encrypt(gad7.get("severity")),
            total_score=encryption.encrypt(gad7.get("total_score")),
            score_type="anxiety",
            created_time=datetime.utcnow()
        )
        db.session.add(score)

    for theme in themes:
        theme_bytes = encryption.encrypt(theme)
        db.session.add(Theme(journal_id=journal.id, theme=theme_bytes, created_time=datetime.utcnow()))

    for emotion in emotions:
        emotion_bytes = encryption.encrypt(emotion)
        db.session.add(Emotion(journal_id=journal.id, emotion=emotion_bytes, created_time=datetime.utcnow()))

    db.session.commit()
    print("Journal entry saved successfully.")
    return journal.id

def get_journal_list():
    sql = text("SELECT id, journal_input, created_time FROM journals")
    results = db.session.execute(sql)
    #for row in results:
    #    print("Type of row[0]:", type(row[0]))
    
    #journal_list = [
    #    {
    #        "journal_input": encryption.decrypt(row[0]),
    #        "input_timestamp": row[1]
    #    }
    #    for row in results
    #]
    #return journal_list
    journal_list = []
    for row in results:
        print("Encrypted value (memoryview):", row[1])
        try:
            journal_input = encryption.decrypt(row[1])
            print("Decrypted value:", journal_input)
        except Exception as e:
            print("Decryption failed for row:", e)
            continue #the first data failed because I was using different encryption key. this is to skip it

        journal_list.append({
            "id":row[0],
            "journal_input": journal_input,
            "created_time": row[2]
        })

    return journal_list

def get_journal_detail(journal_id):
    journal = db.session.query(Journal).get(journal_id)

    if not journal:
        return None

    try:
        decrypted_journal_input = encryption.decrypt(journal.journal_input)
        decrypted_feedback = encryption.decrypt(journal.feedback) if journal.feedback else None

        decrypted_emotions = []
        for emotion in journal.emotions:
            try:
                decrypted_emotions.append(encryption.decrypt(emotion.emotion))
            except Exception as e:
                print(f"Decryption failed for emotion id {emotion.id}: {e}")

        decrypted_scores = []
        for score in journal.scores:
            try:
                decrypted_scores.append({
                    "severity": encryption.decrypt(score.severity) if score.severity else None,
                    "total_score": encryption.decrypt(score.total_score) if score.total_score else None,
                    "score_type": score.score_type,
                    "created_time": score.created_time
                })
            except Exception as e:
                print(f"Decryption failed for score id {score.id}: {e}")

        decrypted_themes = []
        for theme in journal.themes:
            try:
                decrypted_themes.append(encryption.decrypt(theme.theme))
            except Exception as e:
                print(f"Decryption failed for theme id {theme.id}: {e}")

    except Exception as e:
        print("Decryption failed for journal ID", journal_id, ":", e)
        return None

    return {
        "id": journal.id,
        "journal_input": decrypted_journal_input,
        "feedback": decrypted_feedback,
        "created_time": journal.created_time,
        "emotions": decrypted_emotions,
        "scores": decrypted_scores,
        "themes": decrypted_themes
    }


def get_summary_total_entry_days():
    sql = text("""SELECT COUNT(DISTINCT created_time::date) FROM public.journals""")
    result = db.session.execute(sql).scalar()
    return result

def get_summary_input_streak():
    sql = text("""SELECT DISTINCT created_time::date AS entry_date FROM public.journals""")
    result = db.session.execute(sql)
    dates = [row[0] for row in result]

    input_streak = 1
    temp = 1
    for i in range(1, len(dates)):
        if dates[i] == dates[i-1] + timedelta(days=1):
            temp+=1
        else:
            input_streak = max(input_streak, temp)
            temp = 0
    input_streak = max(input_streak, temp)
    return input_streak