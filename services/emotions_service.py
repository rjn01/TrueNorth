from models import db, Emotion
from utils.encryption_utils import EncryptionManager
from sqlalchemy import text
from collections import Counter
encryption = EncryptionManager()

def get_summary_emotion_range():
    sql = text("SELECT emotion FROM emotions")
    results = db.session.execute(sql)
    #decrypted_sentiment = [encryption.decrypt(row[0]) for row in rows]
    decrypted_emotion= []
    for row in results:
        print("Encrypted value (memoryview):", row[0])
        try:
            emotion_data = encryption.decrypt(row[0])
            print("Decrypted value:", emotion_data)
        except Exception as e:
            print("Decryption failed for row:", e)
            continue #the first data failed because I was using different encryption key. this is to skip it

        decrypted_emotion.append({
            "emotion": emotion_data
        })
    emotion_values = [item["emotion"] for item in decrypted_emotion]
    count_emotion = Counter(emotion_values)
    return count_emotion

