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
from services.journals_service import save_journal_entry, get_journal_list, get_summary_sentiment, get_summary_themes, get_summary_input_streak

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


@app.route('/history', methods=['GET', 'POST'])
def history():
    print("Inside history to natigate")
    return render_template('history.html')
# Route for detailed history page
@app.route('/detailed_history',methods=['GET', 'POST'])
def detailed_history():
    return render_template('detailed_history.html')

# API to submit journal entry
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    logger.debug(f"Inside submit")
    data = request.get_json()
    journal_text = data.get('text', '')
    logger.debug(f"Journal received: {journal_text}")
    json_payload = {"entries": [journal_text]}
    logger.debug(f"json_payload : {json_payload}")
    emotions = model.analyze_journal(json_payload)
    logger.info(f"emotions : {emotions}")
    save_journal_entry(journal_text, emotions)
    return jsonify(status="success")

# API to get journal list
@app.route('/journalList', methods=['GET', 'POST'])
def journalList():
    getAllJournalInput = get_journal_list()
    print(getAllJournalInput)
    return jsonify(getAllJournalInput)

# API to get summary sentiment
@app.route('/summarySentiment', methods=['GET', 'POST'])
def summarySentiment():
    sentimentAllTime = get_summary_sentiment()
    countSentiment = dict(sentimentAllTime)
    print(countSentiment)
    return jsonify(countSentiment)

# API to get summary themes
@app.route('/summaryThemes',methods=['GET', 'POST'])
def summaryThemes():
    themesAllTime = get_summary_themes()
    countThemes = dict(themesAllTime)
    print(countThemes)
    return jsonify(countThemes)

# API to get input streak
@app.route('/summaryInputStreak', methods=['GET', 'POST'])
def summaryInputStreak():
    listDateInputStreak = get_summary_input_streak()
    date_list = [int(day) for day in listDateInputStreak]
    print(date_list)
    return jsonify(date_list)

if __name__ == '__main__':
    app.run(debug=True)