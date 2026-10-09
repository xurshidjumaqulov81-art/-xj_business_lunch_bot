from html import escape

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from sqlalchemy import select, func

from config import ADMIN_IDS
from database.db import (
    SessionLocal,
    get_application_with_user,
    set_application_status,
)
from database.models import User, ContestApplication

router = Router()


class AdminReplyStates(StatesGroup):
    waiting_text = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def admin_application_keyboard(application_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Жавоб ёзиш",
                    callback_data=f"admin_reply:{application_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Танланди",
                    callback_data=f"admin_select:{application_id}",
                ),
                InlineKeyboardButton(
                    text="❌ Танланмади",
                    callback_data=f"admin_reject:{application_id}",
                ),
            ],
        ]
    )


def status_name(status: str) -> str:
    names = {
        "pending": "⏳ Кўриб чиқилмаган",
        "replied": "💬 Жавоб берилган",
        "selected": "✅ Танланган",
        "rejected": "❌ Танланмаган",
    }
    return names.get(status, status or "—")


async def send_chunks(message: Message, text: str, reply_markup=None):
    limit = 3900

    if len(text) <= limit:
        await message.answer(
            text,
            reply_markup=reply_markup,
        )
        return

    parts = [
        text[i:i + limit]
        for i in range(0, len(text), limit)
    ]

    for i, part in enumerate(parts):
        markup = reply_markup if i == len(parts) - 1 else None

        await message.answer(
            part,
            reply_markup=markup,
        )


# =========================
# ADMIN MENU
# =========================

@router.message(Command("admin"))
async def admin_help(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "🛠 АДМИН КОМАНДАЛАР\n\n"
        "/stats — умумий статистика\n"
        "/users — барча фойдаланувчилар\n"
        "/applications — барча махсус танлов аризалари\n"
        "/registered — Business Launch'га рўйхатдан ўтганлар\n"
        "/selected — танланган аризалар\n"
        "/cancel — жавоб ёзишни бекор қилиш"
    )


# =========================
# STATISTIKA
# =========================

@router.message(Command("stats"))
async def admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        return

    async with SessionLocal() as session:

        users_count = (
            await session.execute(
                select(func.count(User.id))
            )
        ).scalar_one()

        applications_count = (
            await session.execute(
                select(func.count(ContestApplication.id))
            )
        ).scalar_one()

        registered_count = (
            await session.execute(
                select(func.count(User.id))
                .where(
                    User.is_registered_for_launch.is_(True)
                )
            )
        ).scalar_one()

        selected_count = (
            await session.execute(
                select(func.count(ContestApplication.id))
                .where(
                    ContestApplication.status == "selected"
                )
            )
        ).scalar_one()

    await message.answer(
        "📊 XJ BUSINESS LAUNCH СТАТИСТИКА\n\n"
        f"👥 Фойдаланувчилар: {users_count}\n"
        f"🎁 Махсус танлов аризалари: {applications_count}\n"
        f"✅ Business Launch'га рўйхатдан ўтганлар: {registered_count}\n"
        f"🏆 Танланган аризалар: {selected_count}"
    )


# =========================
# BARCHA USERLAR
# =========================

@router.message(Command("users"))
async def admin_users(message: Message):
    if not is_admin(message.from_user.id):
        return

    async with SessionLocal() as session:

        result = await session.execute(
            select(User)
            .order_by(
                User.created_at.asc(),
                User.id.asc()
            )
        )

        users = result.scalars().all()

    if not users:
        await message.answer(
            "Ҳозирча фойдаланувчилар йўқ."
        )
        return

    lines = [
        f"👥 БАРЧА ФОЙДАЛАНУВЧИЛАР — {len(users)} та\n"
    ]

    for i, user in enumerate(users, start=1):

        username = (
            f"@{user.telegram_username}"
            if user.telegram_username
            else "username йўқ"
        )

        created = (
            user.created_at.strftime("%d.%m.%Y %H:%M")
            if user.created_at
            else "—"
        )

        lines.append(
            f"\n{i}. {user.full_name}\n"
            f"🆔 XJ ID: {user.xj_id}\n"
            f"📱 Телефон: {user.phone}\n"
            f"💬 Telegram: {username}\n"
            f"🔢 Telegram ID: {user.telegram_id}\n"
            f"📅 Кирган сана: {created}"
        )

    await send_chunks(
        message,
        "\n".join(lines)
    )


# =========================
# BUSINESS LAUNCH REGISTERED
# =========================

@router.message(Command("registered"))
async def admin_registered(message: Message):
    if not is_admin(message.from_user.id):
        return

    async with SessionLocal() as session:

        result = await session.execute(
            select(User)
            .where(
                User.is_registered_for_launch.is_(True)
            )
            .order_by(
                User.updated_at.asc(),
                User.id.asc()
            )
        )

        users = result.scalars().all()

    if not users:
        await message.answer(
            "Business Launch'га рўйхатдан ўтганлар ҳозирча йўқ."
        )
        return

    lines = [
        f"✅ BUSINESS LAUNCH'ГА РЎЙХАТДАН ЎТГАНЛАР — {len(users)} та\n"
    ]

    for i, user in enumerate(users, start=1):

        username = (
            f"@{user.telegram_username}"
            if user.telegram_username
            else "username йўқ"
        )

        lines.append(
            f"\n{i}. {user.full_name}\n"
            f"🆔 XJ ID: {user.xj_id}\n"
            f"📱 {user.phone}\n"
            f"💬 {username}\n"
            f"🔢 Telegram ID: {user.telegram_id}"
        )

    await send_chunks(
        message,
        "\n".join(lines)
    )


# =========================
# BARCHA ARIZALAR
# =========================

@router.message(Command("applications"))
async def admin_applications(message: Message):
    if not is_admin(message.from_user.id):
        return

    async with SessionLocal() as session:

        result = await session.execute(
            select(
                ContestApplication,
                User
            )
            .join(
                User,
                ContestApplication.user_id == User.id
            )
            .order_by(
                ContestApplication.created_at.asc(),
                ContestApplication.id.asc()
            )
        )

        rows = result.all()

    if not rows:
        await message.answer(
            "Ҳозирча махсус танлов аризалари йўқ."
        )
        return

    await message.answer(
        f"🎁 Жами махсус танлов аризалари: {len(rows)} та"
    )

    for app, user in rows:

        username = (
            f"@{user.telegram_username}"
            if user.telegram_username
            else "username йўқ"
        )

        created = (
            app.created_at.strftime("%d.%m.%Y %H:%M")
            if app.created_at
            else "—"
        )

        text = (
            f"🎁 МАХСУС ТАНЛОВ АРИЗАСИ №{app.id}\n\n"

            f"👤 Исм-фамилия: {user.full_name}\n"
            f"🆔 XJ ID: {user.xj_id}\n"
            f"📱 Телефон: {user.phone}\n"
            f"💬 Telegram: {username}\n"
            f"🔢 Telegram User ID: {user.telegram_id}\n"
            f"📅 Ариза санаси: {created}\n"
            f"📌 Ҳолати: {status_name(app.status)}\n\n"

            f"1. Ўзи ҳақида:\n"
            f"{app.about}\n\n"

            f"2. XJ'даги мақсади:\n"
            f"{app.goal}\n\n"

            f"3. Нега асосчи билан учрашмоқчи:\n"
            f"{app.why_founder}\n\n"

            f"4. Асосчига битта саволи:\n"
            f"{app.one_question}\n\n"

            f"5. Учрашувдан кейин нимани ўзгартиради:\n"
            f"{app.after_meeting}"
        )

        await send_chunks(
            message,
            text,
            reply_markup=admin_application_keyboard(
                app.id
            ),
        )


# =========================
# TANLANGANLAR
# =========================

@router.message(Command("selected"))
async def admin_selected(message: Message):
    if not is_admin(message.from_user.id):
        return

    async with SessionLocal() as session:

        result = await session.execute(
            select(
                ContestApplication,
                User
            )
            .join(
                User,
                ContestApplication.user_id == User.id
            )
            .where(
                ContestApplication.status == "selected"
            )
            .order_by(
                ContestApplication.created_at.asc()
            )
        )

        rows = result.all()

    if not rows:
        await message.answer(
            "Ҳозирча танланган аризалар йўқ."
        )
        return

    lines = [
        f"🏆 ТАНЛАНГАНЛАР — {len(rows)} та\n"
    ]

    for app, user in rows:

        username = (
            f"@{user.telegram_username}"
            if user.telegram_username
            else "username йўқ"
        )

        lines.append(
            f"\n✅ Ариза №{app.id}\n"
            f"👤 {user.full_name}\n"
            f"🆔 {user.xj_id}\n"
            f"📱 {user.phone}\n"
            f"💬 {username}\n"
            f"🔢 {user.telegram_id}"
        )

    await send_chunks(
        message,
        "\n".join(lines)
    )


# =========================
# CANCEL
# =========================

@router.message(Command("cancel"))
async def admin_reply_cancel(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    await state.clear()

    await message.answer(
        "Жавоб ёзиш бекор қилинди."
    )


# =========================
# ADMIN REPLY BUTTON
# =========================

@router.callback_query(
    F.data.startswith("admin_reply:")
)
async def admin_reply_start(
    callback: CallbackQuery,
    state: FSMContext
):
    if not is_admin(callback.from_user.id):

        await callback.answer(
            "Рухсат йўқ.",
            show_alert=True
        )
        return

    await callback.answer()

    application_id = int(
        callback.data.split(":")[1]
    )

    app, user = await get_application_with_user(
        application_id
    )

    if not app or not user:

        await callback.message.answer(
            "Ариза топилмади."
        )
        return

    await state.set_state(
        AdminReplyStates.waiting_text
    )

    await state.update_data(
        application_id=application_id,
        target_telegram_id=user.telegram_id,
    )

    await callback.message.answer(
        f"<b>{escape(user.full_name)}</b>га юбориладиган жавобни ёзинг.\n\n"
        "Бекор қилиш учун /cancel ёзинг.",
        parse_mode="HTML",
    )


# =========================
# TANLANDI
# =========================

@router.callback_query(
    F.data.startswith("admin_select:")
)
async def admin_select(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):

        await callback.answer(
            "Рухсат йўқ.",
            show_alert=True
        )
        return

    application_id = int(
        callback.data.split(":")[1]
    )

    app, user = await get_application_with_user(
        application_id
    )

    if not app or not user:

        await callback.answer(
            "Ариза топилмади.",
            show_alert=True
        )
        return

    await set_application_status(
        application_id,
        "selected"
    )

    try:

        await callback.bot.send_message(
            user.telegram_id,

            "<b>🎉 ТАБРИКЛАЙМИЗ!</b>\n\n"

            "Сизнинг Махсус танлов аризангиз танлаб олинди.\n\n"

            "Сизга кейинги ташкилий маълумотлар "
            "шу бот орқали юборилади.",

            parse_mode="HTML",
        )

        send_status = (
            "Фойдаланувчига хабар юборилди."
        )

    except Exception as e:

        send_status = (
            f"Фойдаланувчига хабар юборилмади: {e}"
        )

    await callback.answer(
        "Танланди ✅"
    )

    await callback.message.answer(
        f"✅ Ариза №{application_id}: "
        f"<b>{escape(user.full_name)}</b> танланди.\n"
        f"{escape(send_status)}",
        parse_mode="HTML",
    )


# =========================
# TANLANMADI
# =========================

@router.callback_query(
    F.data.startswith("admin_reject:")
)
async def admin_reject(
    callback: CallbackQuery
):
    if not is_admin(callback.from_user.id):

        await callback.answer(
            "Рухсат йўқ.",
            show_alert=True
        )
        return

    application_id = int(
        callback.data.split(":")[1]
    )

    app, user = await get_application_with_user(
        application_id
    )

    if not app or not user:

        await callback.answer(
            "Ариза топилмади.",
            show_alert=True
        )
        return

    await set_application_status(
        application_id,
        "rejected"
    )

    try:

        await callback.bot.send_message(
            user.telegram_id,

            "<b>Махсус танлов бўйича жавоб</b>\n\n"

            "Аризангиз кўриб чиқилди. "
            "Бу сафар танловдан ўтмадингиз.\n\n"

            "XJ BUSINESS LAUNCH'нинг кейинги "
            "имкониятлари ва расмий эълонларини "
            "кузатиб боринг.",

            parse_mode="HTML",
        )

        send_status = (
            "Фойдаланувчига хабар юборилди."
        )

    except Exception as e:

        send_status = (
            f"Фойдаланувчига хабар юборилмади: {e}"
        )

    await callback.answer(
        "Танланмади ❌"
    )

    await callback.message.answer(
        f"❌ Ариза №{application_id}: "
        f"<b>{escape(user.full_name)}</b> танланмади.\n"
        f"{escape(send_status)}",
        parse_mode="HTML",
    )


# =========================
# ADMINNING YOZGAN JAVOBI
# =========================

@router.message(
    AdminReplyStates.waiting_text,
    F.text
)
async def admin_reply_send(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()

    target_id = data.get(
        "target_telegram_id"
    )

    application_id = data.get(
        "application_id"
    )

    if not target_id or not application_id:

        await state.clear()

        await message.answer(
            "Ариза маълумоти топилмади. "
            "Қайта уриниб кўринг."
        )
        return

    try:

        await message.bot.send_message(
            target_id,

            "<b>📩 XJ BUSINESS LAUNCH "
            "АДМИНИСТРАТОРИДАН ЖАВОБ</b>\n\n"

            + escape(message.text),

            parse_mode="HTML",
        )

        await set_application_status(
            application_id,
            "replied",
            admin_note=message.text,
        )

        await message.answer(
            "✅ Жавоб фойдаланувчига "
            "бот орқали юборилди."
        )

    except Exception as e:

        await message.answer(
            f"❌ Жавоб юборилмади: "
            f"{escape(str(e))}",
            parse_mode="HTML",
        )

    await state.clear()
