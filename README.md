# ember

EMBER passively monitors continuous biometric data from Oura Ring — HRV, sleep stages, resting heart rate, and temperature trends — to support early detection of manic episodes in individuals with Bipolar I disorder, using a personalized baseline model to identify physiological deviations indicative of mood state transitions.

## Setup

### 1. Prerequisites

- Python 3.10+
- An [Oura Ring](https://ouraring.com) and developer account
- An Oura OAuth app with a registered `REDIRECT_URI` (e.g. `http://localhost:8000/callback`)

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file in the project root:

```
OURA_CLIENT_ID=your_client_id
OURA_CLIENT_SECRET=your_client_secret
OURA_REDIRECT_URI=http://localhost:8000/callback
```

### 4. Authenticate

Run the OAuth flow once to obtain and store tokens:

```bash
python auth.py
```

This opens a browser, completes the OAuth 2.0 + PKCE flow, and saves `OURA_ACCESS_TOKEN` and `OURA_REFRESH_TOKEN` to `.env`.

### 5. Pull data

```bash
python pull_data.py
```

Fetches the last 30 days of daily readiness and sleep data from the Oura API and saves CSV files to `data/`.

## Project structure

```
auth.py            # OAuth 2.0 + PKCE authentication flow
token_manager.py   # Token validation and automatic refresh
pull_data.py       # Fetches and saves biometric data
data/              # Output directory (gitignored)
requirements.txt   # Python dependencies
.env               # Credentials (gitignored — never commit this)
```

## Notes

- Tokens are automatically refreshed by `token_manager.py` — re-authentication is only needed if the refresh token expires or access is revoked.
- All data is stored locally. See [privacy.md](privacy.md) for details on data handling.
