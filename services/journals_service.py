from models import db, Journal
from datetime import datetime
from utils.encryption_utils import EncryptionManager
from sqlalchemy import text
from collections import Counter
from logger import logger
encryption = EncryptionManager()

def save_journal_entry(daily_text: str, emotions: dict):
    print("inside save journal")
    sentiment = emotions.get("sentiment", "")
    themes = ", ".join(emotions.get("themes", []))
    empathy = emotions.get("empathy", "")
    
    print("above journal")
    journal = Journal(
        journal_input=encryption.encrypt(daily_text),
        sentiment=encryption.encrypt(sentiment),
        themes=encryption.encrypt(themes),
        empathy=encryption.encrypt(empathy),
        input_timestamp=datetime.utcnow()
    )
    print("above journal")
    db.session.add(journal)
    db.session.commit()

def get_journal_list():
    sql = text("SELECT journal_input, input_timestamp FROM journals")#should be changed to title
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
        print("Encrypted value (memoryview):", row[0])
        try:
            journal_input = encryption.decrypt(row[0])
            print("Decrypted value:", journal_input)
        except Exception as e:
            print("Decryption failed for row:", e)
            continue #the first data failed because I was using different encryption key. this is to skip it

        journal_list.append({
            "journal_input": journal_input,
            "input_timestamp": row[1]
        })

    return journal_list

def get_summary_sentiment():
    sql = text("SELECT sentiment FROM journals")
    results = db.session.execute(sql)
    #decrypted_sentiment = [encryption.decrypt(row[0]) for row in rows]
    decrypted_sentiment= []
    for row in results:
        print("Encrypted value (memoryview):", row[0])
        try:
            sentiment_data = encryption.decrypt(row[0])
            print("Decrypted value:", sentiment_data)
        except Exception as e:
            print("Decryption failed for row:", e)
            continue #the first data failed because I was using different encryption key. this is to skip it

        decrypted_sentiment.append({
            "sentiment": sentiment_data
        })
    sentiment_values = [item["sentiment"] for item in decrypted_sentiment]
    count_sentiment = Counter(sentiment_values)
    return count_sentiment

def get_summary_themes():
    sql = text("SELECT themes FROM journals")
    results = db.session.execute(sql)
    decrypted_themes= []
    for row in results:
        print("Encrypted value (memoryview):", row[0])
        try:
            themes_data = encryption.decrypt(row[0])
            print("Decrypted value:", themes_data)
        except Exception as e:
            print("Decryption failed for row:", e)
            continue #the first data failed because I was using different encryption key. this is to skip it

        decrypted_themes.append({
            "themes": themes_data
        })
    themes_value = [item["themes"] for item in decrypted_themes]
    count_themes = Counter(themes_value)
    return count_themes

def get_summary_input_streak():
    sql = text("""SELECT DISTINCT EXTRACT(DAY FROM input_timestamp)::int AS day
               FROM public.journals 
               WHERE 
               EXTRACT(MONTH FROM input_timestamp) = EXTRACT(MONTH FROM CURRENT_DATE) 
               AND 
               EXTRACT(YEAR FROM input_timestamp)= EXTRACT(YEAR FROM CURRENT_DATE);""")
    result = db.session.execute(sql)
    return [row[0] for row in result]

