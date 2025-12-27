from flask import Flask, render_template, request, jsonify, session, redirect
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
import model
from logger import logger
from dotenv import load_dotenv
import os
from utils.encryption_utils import set_encryption_key

set_encryption_key()
load_dotenv()

from models import db
from services.journals_service import (
    save_journal_entry,
    get_journal_detail,
    get_journal_list,
    get_summary_total_entry_days,
    get_summary_input_streak
)
from services.emotions_service import get_summary_emotion_range
from services.themes_service import get_summary_top_3_theme

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------- AUTH DECORATOR ----------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated

# ---------------- AUTH PAGES ----------------
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

# ---------------- AUTH APIs ----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    password_hash = generate_password_hash(password)

    try:
        db.session.execute(
            text("""
                INSERT INTO users (username, email, password_hash)
                VALUES (:username, :email, :password_hash)
            """),
            {
                "username": username,
                "email": email,
                "password_hash": password_hash
            }
        )
        db.session.commit()
        return jsonify(success=True)

    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error="User already exists"), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = db.session.execute(
        text("SELECT id, password_hash FROM users WHERE username=:username"),
        {"username": username}
    ).fetchone()

    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        return jsonify(success=True)

    return jsonify(success=False), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- PAGES ----------------
@app.route('/')
@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/options', methods=['GET', 'POST'])
@login_required
def options():
    return render_template('options.html')

@app.route('/journal', methods=['GET', 'POST'])
@login_required
def journal():
    return render_template('journal.html')

@app.route('/result', methods=['GET', 'POST'])
@login_required
def resulthistory():
    return render_template('result.html')

@app.route('/rearview', methods=['GET', 'POST'])
@login_required
def rearview():
    return render_template('rearview.html')

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    return render_template('history.html')

# ---------------- APIs ----------------
@app.route('/submit', methods=['POST'])
@login_required
def submit():
    data = request.get_json()
    journal_text = data.get('text', '')
    response = model.analyze_journal({"entries": [journal_text]})
    journal_id = save_journal_entry(journal_text, response)
    return jsonify(status="success", journal_id=journal_id)

@app.route('/journalList', methods=['GET', 'POST'])
@login_required
def journalList():
    return jsonify(get_journal_list())

@app.route('/journalDetail/<int:journal_id>')
@login_required
def journal_detail(journal_id):
    return jsonify(get_journal_detail(journal_id))

@app.route('/summaryEmotionRange')
@login_required
def summaryEmotionRange():
    return jsonify(get_summary_emotion_range())

@app.route('/summaryTotalEntry')
@login_required
def summaryTotalEntry():
    return jsonify(get_summary_total_entry_days())

@app.route('/summaryTop3Themes')
@login_required
def summaryThemes():
    return jsonify(dict(get_summary_top_3_theme()))

@app.route('/summaryInputStreak')
@login_required
def summaryInputStreak():
    return jsonify(get_summary_input_streak())

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
