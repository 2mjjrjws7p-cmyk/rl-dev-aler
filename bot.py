import os
import time
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
STEAM_API_KEY = os.environ["STEAM_API_KEY"]
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

# Add verified Psyonix developer SteamID64 accounts here.
DEVS = {
    # "Psyonix Developer": "7656119xxxxxxxxxx",
}

RL_APP_ID = "252950"
last_state = {}

def telegram(text):
    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text},
        timeout=20,
    )
    r.raise_for_status()

def get_players():
    if not DEVS:
        return []
    ids = ",".join(DEVS.values())
    r = requests.get(
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
        params={"key": STEAM_API_KEY, "steamids": ids},
        timeout=20,
    )
    r.raise_for_status()
    return r.json().get("response", {}).get("players", [])

telegram("✅ RL Dev Alert is running.")

while True:
    try:
        by_id = {v: k for k, v in DEVS.items()}
        for p in get_players():
            sid = p.get("steamid")
            name = by_id.get(sid, p.get("personaname", "Psyonix developer"))
            in_rl = p.get("gameid") == RL_APP_ID
            before = last_state.get(sid, False)

            if in_rl and not before:
                telegram(
                    "🚨 PSYONIX DEV DETECTED\n\n"
                    f"👤 {name}\n"
                    "🎮 Rocket League\n"
                    "⚡ دخل اللعبة الآن — افتح Rocket League!"
                )

            last_state[sid] = in_rl

    except Exception as e:
        print("poll error:", repr(e), flush=True)

    time.sleep(CHECK_INTERVAL)
