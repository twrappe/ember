import csv
import os
from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = "data"
LOG_FILE = os.path.join(DATA_DIR, "mood_log.csv")

FIELDS = [
    "date",
    "session",
    # Morning
    "rested",
    "early_waking",
    "less_sleep_fine",
    "thought_speed_morning",
    "classification_night",
    # Evening
    "energy",
    "new_projects",
    "effortful",
    "concentration",
    "mood",
    "irritable",
    "impulsive",
    "withdrew",
    "alcohol",
    "illness",
    "travel",
    "life_stress",
    "classification_day",
    "notes",
]

class MorningEntry(BaseModel):
    rested: int
    early_waking: str
    less_sleep_fine: str
    thought_speed_morning: int
    classification_night: str

class EveningEntry(BaseModel):
    energy: int
    new_projects: str
    effortful: str
    concentration: int
    mood: int
    irritable: str
    impulsive: str
    withdrew: str
    alcohol: str
    illness: str
    travel: str
    life_stress: str
    classification_day: str
    notes: Optional[str] = ""

def ensure_log():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()

def already_logged(today: str, session: str) -> bool:
    if not os.path.exists(LOG_FILE):
        return False
    with open(LOG_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] == today and row["session"] == session:
                return True
    return False

def write_row(row: dict):
    ensure_log()
    full_row = {field: row.get(field, "") for field in FIELDS}
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow(full_row)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html><body style="font-family:monospace;background:#0a0a0a;color:#e8e4dc;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;gap:20px;">
    <div style="font-size:13px;letter-spacing:0.2em;color:#e85d26;">EMBER</div>
    <a href="/morning" style="color:#e8e4dc;font-size:14px;">Morning check-in</a>
    <a href="/evening" style="color:#e8e4dc;font-size:14px;">Evening check-in</a>
    </body></html>
    """

@app.get("/morning", response_class=HTMLResponse)
def morning_form():
    with open("mood_form_morning.html") as f:
        return f.read()

@app.get("/evening", response_class=HTMLResponse)
def evening_form():
    with open("mood_form_evening.html") as f:
        return f.read()

@app.post("/submit/morning")
def submit_morning(entry: MorningEntry):
    today = date.today().isoformat()
    if already_logged(today, "morning"):
        return JSONResponse(status_code=409, content={"message": "Morning entry already logged today."})
    write_row({"date": today, "session": "morning", **entry.dict()})
    return {"message": "Logged", "date": today, "session": "morning"}

@app.post("/submit/evening")
def submit_evening(entry: EveningEntry):
    today = date.today().isoformat()
    if already_logged(today, "evening"):
        return JSONResponse(status_code=409, content={"message": "Evening entry already logged today."})
    write_row({"date": today, "session": "evening", **entry.dict()})
    return {"message": "Logged", "date": today, "session": "evening"}

@app.get("/history")
def history():
    ensure_log()
    rows = []
    with open(LOG_FILE, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return {"entries": rows[-14:]}
