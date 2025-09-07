from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json, os
from datetime import datetime

app = FastAPI()

# ✅ CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ya phir sirf tumhare Netlify URL: ["https://marine-minds-frontend.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPORTS_FILE = "saved_reports.json"
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Save report into JSON file
def save_to_json(report):
    if os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(report)

    with open(REPORTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ✅ Submit report endpoint
@app.post("/submit_report/")
async def submit_report(
    name: str = Form(...),
    location: str = Form(...),
    disaster: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(None)
):
    file_path = None
    if file:
        file_path = os.path.join(UPLOAD_DIR, f"{datetime.utcnow().timestamp()}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(await file.read())

    report = {
        "name": name,
        "location": location,
        "disaster": disaster,
        "description": description,
        "file": file_path,
        "timestamp": datetime.utcnow().isoformat()
    }

    save_to_json(report)
    return JSONResponse({"status": "saved", "report": report})

# ✅ Get reports endpoint
@app.get("/reports/")
def get_reports():
    if not os.path.exists(REPORTS_FILE):
        return []
    with open(REPORTS_FILE, "r") as f:
        return json.load(f)
