import whisper
from yt_dlp import YoutubeDL
import datetime
import re
import spacy
import json

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# ----------------------------
# FastAPI App Setup
# ----------------------------
app = FastAPI()

# Pydantic Model
class Report(BaseModel):
    name: str
    location: str
    hazard: str
    desc: str
    time: str
    lat: Optional[float] = None
    lng: Optional[float] = None

# In-memory DB
reports: List[Report] = []

# ----------------------------
# Whisper + YouTube Extractor
# ----------------------------
nlp = spacy.load("en_core_web_sm")
disaster_keywords = ["flood", "earthquake", "rain", "fire", "storm", "cyclone", "tsunami"]

def process_youtube_video(url: str):
    """Download YouTube audio, transcribe with Whisper, extract disaster info"""
    ydl_opts = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title")
        upload_date = info.get("upload_date")
        video_url = info.get("webpage_url")
        if upload_date:
            formatted_date = datetime.datetime.strptime(upload_date, "%Y%m%d").strftime("%d-%m-%Y")
        else:
            formatted_date = "Not available"

    hashtags_desc = re.findall(r"#(\w+)", info.get("description") or "")
    hashtags_title = re.findall(r"#(\w+)", info.get("title") or "")
    all_hashtags = hashtags_desc + hashtags_title
    disaster_hashtags = [tag for tag in all_hashtags if any(k in tag.lower() for k in disaster_keywords)]

    audio_opts = {'format': 'bestaudio/best', 'outtmpl': 'audio.%(ext)s', 'quiet': True}
    with YoutubeDL(audio_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info)

    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    script_text = result["text"]

    doc = nlp(script_text)
    disaster_sentences = []
    entities = []

    for sent in doc.sents:
        sent_text = sent.text.strip()
        for k in disaster_keywords:
            if k in sent_text.lower():
                words = sent_text.split()
                idx = [i for i, w in enumerate(words) if k in w.lower()]
                for i in idx:
                    start = max(0, i - 7)
                    end = min(len(words), i + 7)
                    snippet = " ".join(words[start:end])
                    disaster_sentences.append(snippet)

                sent_doc = nlp(sent_text)
                for ent in sent_doc.ents:
                    entities.append({"text": ent.text, "label": ent.label_})

    return {
        "title": title,
        "upload_date": formatted_date,
        "video_url": video_url,
        "all_hashtags": all_hashtags,
        "disaster_hashtags": disaster_hashtags,
        "transcript": script_text,
        "disaster_sentences": disaster_sentences,
        "extracted_entities": entities
    }

# ----------------------------
# API Endpoints
# ----------------------------
@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.get("/reports")
def get_reports():
    return reports

@app.post("/reports")
def add_report(report: Report):
    reports.append(report)
    return {"message": "Report added successfully!", "report": report}

# Optional: YouTube processing endpoint
@app.post("/process_youtube")
def process_video(url: str):
    data = process_youtube_video(url)
    return data
