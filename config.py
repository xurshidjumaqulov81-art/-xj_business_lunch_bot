import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///xj_bot.db").strip()
OFFICIAL_CHANNEL_URL = os.getenv("OFFICIAL_CHANNEL_URL", "https://t.me/xjmedia").strip()

_raw_admins = os.getenv("ADMIN_IDS", "").strip()
ADMIN_IDS = {
    int(x.strip())
    for x in _raw_admins.split(",")
    if x.strip().isdigit()
}

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN топилмади. Railway Variables ёки .env файлга BOT_TOKEN қўшинг.")

