from models import db
from utils.encryption_utils import EncryptionManager
from sqlalchemy import text
from collections import Counter
encryption = EncryptionManager()

def get_summary_risk_level_phq9():
    sql = text("SELECT severity FROM scores WHERE score_type='phq9' ")
    results = db.session.execute(sql)
    #decrypted_sentiment = [encryption.decrypt(row[0]) for row in rows]
    decrypted_score= []
    for row in results:
        print("Encrypted value (memoryview):", row[0])
        try:
            score_data = encryption.decrypt(row[0])
            print("Decrypted value:", score_data)
        except Exception as e:
            print("Decryption failed for row:", e)
            continue #the first data failed because I was using different encryption key. this is to skip it

        decrypted_score.append({
            "score": score_data
        })
    score_values = [item["score"] for item in decrypted_score]
    count_score_phq9 = Counter(score_values)

    return count_score_phq9

def get_summary_risk_level_gad7():
    sql = text("SELECT severity FROM scores WHERE score_type='gad7' ")
    results = db.session.execute(sql)
    #decrypted_sentiment = [encryption.decrypt(row[0]) for row in rows]
    decrypted_score= []
    for row in results:
        print("Encrypted value (memoryview):", row[0])
        try:
            score_data = encryption.decrypt(row[0])
            print("Decrypted value:", score_data)
        except Exception as e:
            print("Decryption failed for row:", e)
            continue #the first data failed because I was using different encryption key. this is to skip it

        decrypted_score.append({
            "score": score_data
        })
    score_values = [item["score"] for item in decrypted_score]
    count_score_gad7 = Counter(score_values)

    return count_score_gad7