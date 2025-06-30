from models import db
from utils.encryption_utils import EncryptionManager
from sqlalchemy import text
from collections import Counter
encryption = EncryptionManager()

def get_summary_top_3_theme():
    sql = text("SELECT theme FROM themes")
    results = db.session.execute(sql)
    #decrypted_sentiment = [encryption.decrypt(row[0]) for row in rows]
    decrypted_theme= []
    for row in results:
        print("Encrypted value (memoryview):", row[0])
        try:
            theme_data = encryption.decrypt(row[0])
            print("Decrypted value:", theme_data)
        except Exception as e:
            print("Decryption failed for row:", e)
            continue #the first data failed because I was using different encryption key. this is to skip it

        decrypted_theme.append({
            "theme": theme_data
        })
    theme_values = [item["theme"] for item in decrypted_theme]
    count_theme = Counter(theme_values)
    top_3_theme = count_theme.most_common(3)

    return top_3_theme