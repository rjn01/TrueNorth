#!/usr/bin/env python
# coding: utf-8
import os
import re
import json
import torch
import gdown
import nltk
import nest_asyncio
import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
from pathlib import Path
from rake_nltk import Rake
from transformers import pipeline
from llama_cpp import Llama
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from logger import logger


# Setup
nest_asyncio.apply()
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

app = FastAPI()

# Mistral model config
MODEL_DIR = "MODEL"
MODEL_FILE = "mistral-7b-instruct-v0.1.Q5_K_M.gguf"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILE)

# Download instructions (manual or automated if hosted)
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_DIR, exist_ok=True)
    raise FileNotFoundError(
        f"Please manually download {MODEL_FILE} from Hugging Face "
        f"https://huggingface.co/TheBloke/mistral-7b-instruct-v0.1.Q5_K_M.gguf "
        f"and place it in {MODEL_DIR}"
    )

# Load Mistral
llm_raw = Llama(model_path=MODEL_PATH, n_ctx=2048)
llm = LlamaCpp(model_path=MODEL_PATH, n_ctx=2048, temperature=0.6, top_p=0.8)

# Emotion classifier
device = 0 if torch.backends.mps.is_available() else -1
sentiment_pipeline = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    tokenizer="SamLowe/roberta-base-go_emotions",
    framework="pt",
    device=device
)

# Request structure
class JournalRequest(BaseModel):
    entry: str

# Emotion extractor
def get_sentiment(journal_entries):
    emotion_counts = Counter()
    for entry in journal_entries:
        results = sentiment_pipeline(entry)
        for r in results:
            emotion_counts[r['label']] += 1
    return [label for label, _ in emotion_counts.most_common(3)] or ["neutral"]

# Theme extractor
def get_themes(journal_entries, top_n=3):
    print(f"type of journal enteries : {type(journal_entries)}")
    text = " ".join(journal_entries[0])
    print(f"journal enteries text: {text}")

    r = Rake()
    r.extract_keywords_from_text(text)
    return [kw for _, kw in r.get_ranked_phrases_with_scores()[:top_n]]

# Robust JSON extractor
def extract_json(text):
    match = re.search(r'{\s*"phq9":\s*{.*?}\s*,\s*"gad7":\s*{.*?}\s*}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return {
        "phq9": {"total_score": 0, "severity": "unknown"},
        "gad7": {"total_score": 0, "severity": "unknown"}
    }

# PHQ-9 and GAD-7 scorer
def infer_phq9_gad7(entries):
    journal = " ".join(entries[0])
    prompt_template = PromptTemplate.from_template("""
Based on the user's journal, infer PHQ-9 and GAD-7 scores and severity and respond using this exact JSON format:

{{
  "phq9": {{
    "total_score": INT,
    "severity": "SEVERITY"
  }},
  "gad7": {{
    "total_score": INT,
    "severity": "SEVERITY"
  }}
}}

Journal Entry:
{journal}

Please return only the JSON without any additional text or explanations
""")
    chain = LLMChain(llm=llm, prompt=prompt_template)
    output = chain.run(journal=journal)
    print("Raw model output:", output)
    return extract_json(output)

# Feedback generator
def get_empathy(entries, emotions, scores):
    journal = " ".join(entries[0])
    prompt_template = PromptTemplate.from_template("""
You are a gentle, wise therapist. Based on this journal, emotion list, and scores, provide few soft sentence of emotional support.
Include a touch of evidence from the journal or emotion summary. No greetings or explanations.

Journal: {journal}
Emotions: {emotions}
PHQ-9: {phq} ({phq_severity})
GAD-7: {gad} ({gad_severity})
""")
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run(
        journal=journal,
        emotions=", ".join(emotions),
        phq=scores['phq9']['total_score'],
        phq_severity=scores['phq9']['severity'],
        gad=scores['gad7']['total_score'],
        gad_severity=scores['gad7']['severity']
    ).strip()

# API route
@app.post("/analyze")
def analyze_journal(data: JournalRequest):
    entries = [data['entries']]
    print(f"entries : {entries}")
    try:
        emotions = get_sentiment(entries)
        logger.debug(f"emotions; {emotions}")
    except:
        logger.debug(f"error in get sentiment")
    
    try:
        themes = get_themes(entries)
        logger.debug(f"themes; {themes}")
    except:
        logger.debug(f"error in get_themes")

    try:
        scores = infer_phq9_gad7(entries)
        logger.debug(f"scores; {scores}")
    except:
        logger.debug(f"error in infer_phq9_gad7")

    try:
        feedback = get_empathy(entries, emotions, scores)
        logger.debug(f"feedback; {feedback}")
    except:
        logger.debug(f"error in  feedback")


    return {
        "depression": scores["phq9"],
        "anxiety": scores["gad7"],
        "themes": themes,
        "emotions": emotions,
        "feedback": feedback
    }

# Run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
