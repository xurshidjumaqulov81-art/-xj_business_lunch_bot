from html import escape

from aiogram import Bot

from config import ADMIN_IDS
from keyboards.admin import admin_application_keyboard


def tg_identity(user) -> str:
    username = f"@{user.telegram_username}" if user.telegram_username else "username ўрнатилмаган"
    return (
        f"💬 Telegram: {escape(username)}\n"
        f"🔢 Telegram User ID: <code>{user.telegram_id}</code>"
    )


async def notify_admins_new_user(bot: Bot, user):
    if not ADMIN_IDS:
        return

    text = (
        "<b>🆕 ЯНГИ ФОЙДАЛАНУВЧИ</b>\n\n"
        f"👤 Исм-фамилия: {escape(user.full_name)}\n"
        f"🆔 XJ ID: <code>{escape(user.xj_id)}</code>\n"
        f"📱 Телефон: {escape(user.phone)}\n"
        f"{tg_identity(user)}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text, parse_mode="HTML")
        except Exception:
            pass


async def notify_admins_application(bot: Bot, user, app):
    if not ADMIN_IDS:
        return

    text = (
        "<b>🎁 ЯНГИ МАХСУС ТАНЛОВ АРИЗАСИ</b>\n\n"
        f"📝 Ариза №: <code>{app.id}</code>\n"
        f"👤 Исм-фамилия: {escape(user.full_name)}\n"
        f"🆔 XJ ID: <code>{escape(user.xj_id)}</code>\n"
        f"📱 Телефон: {escape(user.phone)}\n"
        f"{tg_identity(user)}\n\n"
        f"<b>1. Ўзи ҳақида:</b>\n{escape(app.about)}\n\n"
        f"<b>2. XJ’даги мақсади:</b>\n{escape(app.goal)}\n\n"
        f"<b>3. Нега асосчи билан учрашмоқчи:</b>\n{escape(app.why_founder)}\n\n"
        f"<b>4. Асосчига битта саволи:</b>\n{escape(app.one_question)}\n\n"
        f"<b>5. Учрашувдан кейин нимани ўзгартиради:</b>\n{escape(app.after_meeting)}"
    )

    keyboard = admin_application_keyboard(app.id)

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        except Exception:
            pass

