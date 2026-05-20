# EMBER

EMBER is a personal health intelligence platform that passively monitors continuous biometric data from an Oura Ring — HRV, sleep stages, resting heart rate, and temperature trends — to detect early physiological warning signs before they become clinical events.

Built for anyone who wants to understand their body's patterns over time, EMBER is designed with chronic condition management in mind: mood disorders, autoimmune conditions, chronic fatigue, long-term stress monitoring, and general wellness tracking. Rather than reacting to symptoms after the fact, EMBER surfaces deviations from your personal baseline and generates AI-assisted summaries for self-reflection or clinical review.

## How it works

```
Oura Ring → pull_data.py → score_baseline.py → summarize.py
                                                       ↓
                              api.py ← data/   mood_server.py
                                ↓
                         React dashboard
```

1. **Collect** — pulls daily readiness and sleep data from the Oura API
2. **Score** — computes z-score deviations from your rolling 30-day personal baseline
3. **Summarise** — generates a plain-language clinical summary via Claude AI
4. **Visualise** — serves a live dashboard showing risk trends, alerts, and biometric charts
5. **Log** — morning and evening mood journals add subjective context to the objective data

## Stack

| Layer | Technology |
|---|---|
| Data pipeline | Python, pandas, Oura API v2 |
| Auth | OAuth 2.0 + PKCE (S256) |
| AI summaries | Anthropic Claude |
| REST API | FastAPI + uvicorn |
| Dashboard | React, Vite, Recharts |
| E2E tests | Playwright |

## Setup

### 1. Prerequisites

- Python 3.10+
- Node.js 18+
- An [Oura Ring](https://ouraring.com) and developer account
- An Oura OAuth app with redirect URI set to `http://localhost:8080/callback`
- An [Anthropic API key](https://console.anthropic.com/) for AI summaries

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

```
OURA_CLIENT_ID=your_client_id
OURA_CLIENT_SECRET=your_client_secret
OURA_REDIRECT_URI=http://localhost:8080/callback
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 4. Authenticate with Oura

Run once to complete the OAuth 2.0 + PKCE flow and store tokens:

```bash
python auth.py
```

This opens a browser, completes authorisation, and saves `OURA_ACCESS_TOKEN` and `OURA_REFRESH_TOKEN` to `.env` automatically.

### 5. Run the pipeline

Pulls data, scores deviations, and generates an AI summary:

```bash
python run_ember.py
```

Logs are written to `logs/ember.log`. Output CSVs and summaries are saved to `data/`.

### 6. Start the dashboard

**Terminal 1 — REST API:**
```bash
uvicorn api:app --reload --port 8000
```

**Terminal 2 — React frontend:**
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### 7. Mood logging (optional)

**Terminal 3 — Mood server:**
```bash
uvicorn mood_server:app --host 0.0.0.0 --port 8001
```

Morning form: `http://localhost:8001/morning`
Evening form: `http://localhost:8001/evening`

## Project structure

```
auth.py              # OAuth 2.0 + PKCE authentication
token_manager.py     # Token validation and auto-refresh
pull_data.py         # Incremental Oura data collection
score_baseline.py    # Rolling z-score deviation scoring
summarize.py         # AI-generated clinical summaries (Claude)
run_ember.py         # Pipeline orchestrator
api.py               # FastAPI REST API for the dashboard
mood_server.py       # Morning/evening mood logging server
frontend/            # React + Vite dashboard
data/                # Local data storage (gitignored)
logs/                # Pipeline run logs (gitignored)
.env                 # Credentials (gitignored — never commit)
.env.example         # Environment variable template
```

## Notes

- Tokens refresh automatically — re-authentication is only needed if the refresh token expires.
- All biometric data is stored locally and never transmitted beyond the Oura and Anthropic APIs.
- See [privacy.md](privacy.md) for full data handling details.
