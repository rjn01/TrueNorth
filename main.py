from flask import Flask, render_template, request, jsonify
import model
import json
from logger import logger
from dotenv import load_dotenv
import os
from utils.encryption_utils import set_encryption_key

set_encryption_key()
load_dotenv()  # load env file

from models import db  # load the ORM
from services.journals_service import save_journal_entry, get_journal_detail, get_journal_list, get_summary_total_entry_days, get_summary_input_streak
from services.emotions_service import get_summary_emotion_range
from services.themes_service import get_summary_top_3_theme

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")  # reading DB config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
logger.debug(f"checking if it is reading database url: {os.getenv('DATABASE_URL')}")

db.init_app(app)

# Route for welcome page
@app.route('/', methods=['GET', 'POST'])
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

# Route for options page
@app.route('/options', methods=['GET', 'POST'])
def options():
    return render_template('options.html')

# Route for journal page
@app.route('/journal', methods=['GET', 'POST'])
def journal():
    if request.method == 'POST':
        journal_text = request.form.get('journal_text', '')
        if journal_text:
            json_payload = {"entries": [journal_text]}
            emotions = model.analyze_journal(json_payload)
            logger.info(f"emotions : {emotions}")
            save_journal_entry(journal_text, emotions)
            return jsonify(status="success")
    return render_template('journal.html')

# Route for result page
@app.route('/result', methods=['GET', 'POST'])
def resulthistory():
    return render_template('result.html')

@app.route('/rearview', methods=['GET', 'POST'])
def rearview():
    print("Inside rearview to natigate")
    return render_template('rearview.html')
# Route for detailed history page
@app.route('/history',methods=['GET', 'POST'])
def history():
    return render_template('history.html')

# API to submit journal entry
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    logger.debug(f"Inside submit")
    data = request.get_json()
    journal_text = data.get('text', '')
    logger.debug(f"Journal received: {journal_text}")
    json_payload = {"entries": [journal_text]}
    logger.debug(f"json_payload : {json_payload}")
    #response = model.analyze_journal(json_payload)
    response = {
         "phq9": {
             "total_score": 9,
             "severity": "mild"
         },
         "gad7": {
             "total_score": 9,
             "severity": "mild"
         },
         "themes": [
             "feel anxious",
             "trouble sleeping",
             "anxious trouble"
         ],
         "emotions": [
             "Joy", "Love", "Anger"
         ],
         "feedback": "No significant symptoms detected.",
         "analysis_model": "RoBERTa-GoEmotions+KeyBERT+OPT-1.3b"
    }
    logger.info(f"response : {response}")
    save_journal_entry(journal_text, response)
    #return jsonify(status="success")
    journal_id = save_journal_entry(journal_text, response)
    
    return jsonify(status="success", journal_id=journal_id)

# API to get journal list
@app.route('/journalList', methods=['GET', 'POST'])
def journalList():
    getAllJournalInput = get_journal_list()
    print(getAllJournalInput)
    return jsonify(getAllJournalInput)

@app.route('/journalDetail/<int:journal_id>', methods=['GET'])
def journal_detail(journal_id):
    journalDetail = get_journal_detail(journal_id)
    #return render_template('result.html', entry=journalDetail)
    print(journalDetail)
    return jsonify(journalDetail)

@app.route('/summaryEmotionRange', methods=['GET', 'POST'])
def summaryEmotionRange():
    emotionRangeList = get_summary_emotion_range()
    print(emotionRangeList)
    return jsonify(emotionRangeList)

@app.route('/summaryTotalEntry', methods=['GET', 'POST'])
def summaryTotalEntry():
    noOfTotalEntry = get_summary_total_entry_days()
    print(noOfTotalEntry)
    return jsonify(noOfTotalEntry)


# API to get summary themes
@app.route('/summaryTop3Themes',methods=['GET', 'POST'])
def summaryThemes():
    top3Themes = get_summary_top_3_theme()
    themes = dict(top3Themes)
    print(themes)
    return jsonify(themes)


# API to get input streak
@app.route('/summaryInputStreak', methods=['GET', 'POST'])
def summaryInputStreak():
    noOfInputStreak = get_summary_input_streak()
    print(noOfInputStreak)
    return jsonify(noOfInputStreak)

if __name__ == '__main__':
    app.run(debug=True)