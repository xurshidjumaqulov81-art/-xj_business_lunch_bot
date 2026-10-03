# XJ Business Launch Telegram Bot

Telegram bot for:
- XJ user registration
- 7-digit XJ ID validation
- phone number collection
- Business Launch information
- Founder Day / Founder Lunch information
- Special Selection application
- admin notifications
- Telegram username + Telegram User ID shown to admins
- admin reply through the bot
- admin select/reject buttons
- optional premium section images
- Railway deployment

## 1. Create Telegram bot

Open `@BotFather` in Telegram:

1. `/newbot`
2. Give the bot a name
3. Give the bot a username
4. Copy the bot token

## 2. Get your Telegram admin ID

Use a Telegram ID bot such as `@userinfobot` to get your numeric Telegram ID.

Example:
`123456789`

You can add multiple admins:

`ADMIN_IDS=123456789,987654321`

## 3. Environment variables

For local test, copy `.env.example` to `.env`.

Example:

```env
BOT_TOKEN=1234567890:ABCDEF...
ADMIN_IDS=123456789
DATABASE_URL=sqlite+aiosqlite:///xj_bot.db
OFFICIAL_CHANNEL_URL=https://t.me/xjmedia
```

IMPORTANT:
- Never publish your real BOT_TOKEN in GitHub.
- For Railway, add variables in Railway > Service > Variables.

## 4. Railway database

For production, add PostgreSQL in Railway.

Railway will provide a `DATABASE_URL`.
Put that value in your bot service Variables.

This project automatically converts Railway's
`postgresql://...`
URL into the async SQLAlchemy URL.

For a quick local test, SQLite works.

## 5. Run locally

Python 3.11+ recommended.

```bash
pip install -r requirements.txt
python bot.py
```

## 6. Deploy to Railway

1. Put the project in GitHub.
2. Create a new Railway project.
3. Deploy from GitHub repo.
4. Add PostgreSQL service.
5. Add these Variables to the bot service:
   - `BOT_TOKEN`
   - `ADMIN_IDS`
   - `DATABASE_URL`
   - `OFFICIAL_CHANNEL_URL`
6. Railway will run:
   `python bot.py`

## 7. Premium images later

The bot already supports section images.

Put your final JPG images into the `assets/` folder with these exact names:

- `business_launch.jpg`
- `founder_day.jpg`
- `founder_lunch.jpg`
- `conditions.jpg`
- `contest.jpg`
- `registration.jpg`
- `faq.jpg`

If an image exists, the bot sends image + text.
If the image does not exist yet, the bot sends text only.

## 8. Admin workflow

When a user completes the Special Selection form, each admin receives:

- Full name
- XJ ID
- Phone
- Telegram @username (if available)
- Telegram User ID
- All 5 answers

Admin buttons:
- `💬 Жавоб ёзиш`
- `✅ Танланди`
- `❌ Танланмади`

When the admin writes a reply, the user receives it directly from the bot.

## Important behavior

A Telegram bot cannot start a private conversation with a user who has never pressed Start.
In this system that is not a problem because every applicant has already started the bot.

## Folder structure

```text
xj_business_launch_bot/
├── assets/
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── models.py
├── handlers/
│   ├── __init__.py
│   ├── admin.py
│   ├── contest.py
│   ├── menu.py
│   ├── registration.py
│   └── start.py
├── keyboards/
│   ├── __init__.py
│   ├── admin.py
│   ├── main_menu.py
│   └── registration.py
├── services/
│   ├── __init__.py
│   ├── media.py
│   ├── notifications.py
│   ├── texts.py
│   └── validators.py
├── .env.example
├── bot.py
├── config.py
├── Procfile
├── railway.json
├── requirements.txt
└── README.md
```

