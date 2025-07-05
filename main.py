from flask import Flask, render_template, request, jsonify, redirect, url_for
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
    return render_template('journal.html')

# Route for result page
#@app.route('/result', methods=['GET', 'POST'])
#def resulthistory():
#    return render_template('result.html')
#

@app.route('/history', methods=['GET', 'POST'])
def history():
    print("Inside history to natigate")
    return render_template('history.html')
# Route for detailed history page
@app.route('/detailed_history',methods=['GET', 'POST'])
def detailed_history():
    return render_template('detailed_history.html')

# API to submit journal entry
@app.route('/submit', methods=['POST'])
def submit():
    logger.debug("Inside submit")

    # Get text from HTML form (not JSON)
    journal_text = request.form.get('text', '')
    logger.debug(f"Journal received: {journal_text}")
    
    json_payload = {"entries": [journal_text]}
    logger.debug(f"json_payload : {json_payload}")
    
    # Simulated model response
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

    # Save journal and get ID
    journal_id = save_journal_entry(journal_text, response)
    journal_detail = get_journal_detail(journal_id)  # Make sure this returns correct data
    
    if not journal_detail:
        return "Journal not found", 404
    
    return render_template('result.html', journal=journal_detail)



# API to get journal list
@app.route('/journalList', methods=['GET', 'POST'])
def journalList():
    getAllJournalInput = get_journal_list()
    print(getAllJournalInput)
    return jsonify(getAllJournalInput)

@app.route('/journalDetail/<int:journal_id>', methods=['GET'])
def journal_detail(journal_id):
    journalDetail = get_journal_detail(journal_id)
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

@app.route('/result', methods=['POST'])
def result_post():
    print(" is it here?")
    journal_id = save_journal_entry(request.form)
    return redirect(url_for('result', journal_id=journal_id))

@app.route('/result/<int:journal_id>', methods=['GET'])
def result(journal_id):
    print(" is it here or here?")
    journal_detail = get_journal_detail(journal_id)
    if not journal_detail:
        return "Journal not found", 404
    return render_template('result.html', journal=journal_detail)


if __name__ == '__main__':
    app.run(debug=True)