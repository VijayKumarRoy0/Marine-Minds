import whisper
from yt_dlp import YoutubeDL
import datetime
import re
import spacy
import json

url = "https://youtube.com/shorts/NsioyXKHjCs?si=Lsx7KcFXpgPqx6YY"
nlp = spacy.load("en_core_web_sm")

disaster_keywords = ["flood", "earthquake", "rain", "fire", "storm", "cyclone", "tsunami"]


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


output = {
    "title": title,
    "upload_date": formatted_date,
    "video_url": video_url,
    "all_hashtags": all_hashtags,
    "disaster_hashtags": disaster_hashtags,
    "transcript": script_text,
    "disaster_sentences": disaster_sentences,
    "extracted_entities": entities
}

print(json.dumps(output, indent=4, ensure_ascii=False))
