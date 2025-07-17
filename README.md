# TrueNorth: Mental Health Journal App

TrueNorth is a web application designed to improve mental health and self-awareness by helping users link emotions to habits, encouraging positive behaviors and avoiding negative ones. With a focus on privacy and safety, TrueNorth supports unlimited daily journal entries, integrates with an AI backend for emotion analysis, theme detection, and mental health feedback, and provides gentle actionable advice. The AI backend is powered by the [llm-journal-analyzer](https://github.com/beb0/llm-journal-analyzer) API endpoint.

## Why TrueNorth?
- **Comprehensive Emotion Analysis**: Detects 28 emotions with 97% accuracy via the `roberta-base-go_emotions` model (see [llm-journal-analyzer](https://github.com/beb0/llm-journal-analyzer)).
- **Theme Detection**: Connects habits and concerns to emotions using the RAKE algorithm.
- **Mental Health Focus**: Infers depression and anxiety scores using PHQ-9 and GAD-7 standards, identifying struggles early.
- **Privacy & Safety**: Secures user data with PostgreSQL and Fernet encryption.
- **Unlimited Journaling**: Log entries without restrictions.

## Features
- **Unlimited Daily Entries**: Journal as often as needed.
- **Emotion Analysis**: Displays top 3 emotions from text (processed by AI backend).
- **Theme Extraction**: Highlights key habits and concerns.
- **Gentle Actionable Advice**: Offers empathetic, therapist-like feedback.
- **Depression & Anxiety Feedback**: Provides scores based on PHQ-9 and GAD-7.
- **Secure Storage**: Encrypts data for user privacy.

## GAD-7 and PHQ-9 Screening
TrueNorth uses standard clinical guidelines for transparency:
- **GAD-7 (Generalized Anxiety Disorder Scale)**:
  - 7 questions, scored 0 (not at all) to 3 (nearly every day).
  - Total score: 0–21 (higher indicates more severe symptoms).
- **PHQ-9 (Patient Health Questionnaire-9)**:
  - 9 questions, scored 0 (not at all) to 3 (nearly every day).
  - Total score: 0–27 (higher indicates more severe symptoms).
- **More Info**: [GAD-7 and PHQ-9 Details](https://www.medi-stats.com/gad-7-phq-9)

## Architecture
### Frontend
- **Technologies**: HTML, CSS, JavaScript
- **Purpose**: Provides an intuitive interface for journal entry and feedback display.

### Backend
- **Framework**: Python (Flask)
- **Database**: PostgreSQL with Fernet encryption for secure data storage.
- **AI Integration**: Connects to the [llm-journal-analyzer](https://github.com/beb0/llm-journal-analyzer) API for emotion detection, theme extraction, depression/anxiety scoring, and therapeutic feedback.

### AI Backend
- **Details**: See the [llm-journal-analyzer README](https://github.com/beb0/llm-journal-analyzer) for information on the Dockerized FastAPI endpoint, LangChain, `roberta-base-go_emotions`, RAKE, and Mistral-7B LLM.

### Component Licensing and Costs
- **Flask**: Free (BSD license); hosting costs apply (e.g., $10–$100/month on AWS).
- **PostgreSQL**: Free (PostgreSQL license); cloud hosting may incur costs.
- **Fernet Encryption**: Free (part of Python’s `cryptography` library, BSD license).
- **AI Backend Components** (via llm-journal-analyzer):
  - Dockerized API Endpoint: Free (Apache 2.0); cloud hosting costs apply.
  - FastAPI: Free (MIT license).
  - LangChain: Free (MIT license); external API costs may apply.
  - roberta-base-go_emotions: Free (MIT license); cloud inference ~$0.06–$1/hour.
  - RAKE: Free (MIT license for `rake-nltk`).
  - Mistral-7B: Free (Apache 2.0); API inference ~$0.10–$0.25 per 1M tokens.
- **Note**: Self-hosting is free (excluding hardware/electricity). Cloud deployment or API usage incurs costs. For xAI API services, see [x.ai/api](https://x.ai/api).

## Setup Instructions
### Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js (for frontend development)
- Running instance of [llm-journal-analyzer](https://github.com/beb0/llm-journal-analyzer) API (see its README for setup).

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rjn01/TrueNorth.git
   cd TrueNorth
   ```

2. **Backend Setup**:
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Configure PostgreSQL:
     - Create a database and update connection details in `config.py`.
     - Generate and store a Fernet encryption key securely.
   - Run the Flask app:
     ```bash
     python app.py
     ```

3. **Environment Variables**:
   - Create a `.env` file with:
     ```bash
     DATABASE_URL=postgresql://user:password@localhost:5432/dbname
     FERNET_KEY=your-fernet-key
     API_ENDPOINT=http://localhost:5000  # URL of llm-journal-analyzer
     ```

### Running the App
- Ensure the [llm-journal-analyzer](https://github.com/beb0/llm-journal-analyzer) API is running.
- Start the Flask server 
- Access TrueNorth at `http://localhost:5000`.
- Journal entries are processed via the AI API, with encrypted storage and real-time insights.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.
