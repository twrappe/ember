import os
import requests
import pandas as pd
from datetime import date, timedelta
from dotenv import load_dotenv
from token_manager import get_valid_token

load_dotenv()

BASE_URL = "https://api.ouraring.com/v2/usercollection"
DATA_DIR = "data"

def get_start_date(name: str) -> str:
    path = os.path.join(DATA_DIR, f"{name}.csv")
    if os.path.exists(path):
        existing = pd.read_csv(path)
        if "day" in existing.columns and not existing.empty:
            return (date.fromisoformat(existing["day"].max()) + timedelta(days=1)).isoformat()
    return (date.today() - timedelta(days=30)).isoformat()

def fetch(endpoint: str, token: str, start_date: str) -> list:
    end_date = date.today().isoformat()
    resp = requests.get(
        f"{BASE_URL}/{endpoint}",
        headers={"Authorization": f"Bearer {token}"},
        params={"start_date": start_date, "end_date": end_date},
    )
    resp.raise_for_status()
    return resp.json().get("data", [])

def save(df: pd.DataFrame, name: str):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, f"{name}.csv")
    if os.path.exists(path):
        existing = pd.read_csv(path)
        df = pd.concat([existing, df]).drop_duplicates(subset=["day"]).sort_values("day")
    df.to_csv(path, index=False)
    print(f"  Saved {len(df)} rows → {path}")

def main():
    token = get_valid_token()

    readiness_data = fetch("daily_readiness", token, get_start_date("daily_readiness"))
    df_readiness = pd.DataFrame(readiness_data)
    print("\n=== Daily Readiness ===")
    print(df_readiness.to_string())
    save(df_readiness, "daily_readiness")

    sleep_data = fetch("daily_sleep", token, get_start_date("daily_sleep"))
    df_sleep = pd.DataFrame(sleep_data)
    print("\n=== Daily Sleep ===")
    print(df_sleep.to_string())
    save(df_sleep, "daily_sleep")

if __name__ == "__main__":
    main()