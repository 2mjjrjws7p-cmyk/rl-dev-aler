# RL Dev Alert

Telegram worker that checks known public Steam profiles for Rocket League presence.

## Railway variables
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `STEAM_API_KEY`
- `CHECK_INTERVAL` (optional, default: 60 seconds)

## Important
Add verified Psyonix developer SteamID64 values to `DEVS` in `bot.py`.
Detection works only when Steam exposes the player's current game.
