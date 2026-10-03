from html import escape

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from config import ADMIN_IDS
from database.db import get_application_with_user, set_application_status

router = Router()


class AdminReplyStates(StatesGroup):
    waiting_text = State()


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.callback_query(F.data.startswith("admin_reply:"))
async def admin_reply_start(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        await callback.answer("Рухсат йўқ.", show_alert=True)
        return

    await callback.answer()
    application_id = int(callback.data.split(":")[1])

    app, user = await get_application_with_user(application_id)
    if not app or not user:
        await callback.message.answer("Ариза топилмади.")
        return

    await state.set_state(AdminReplyStates.waiting_text)
    await state.update_data(
        application_id=application_id,
        target_telegram_id=user.telegram_id,
    )

    await callback.message.answer(
        f"<b>{escape(user.full_name)}</b>га юбориладиган жавобни ёзинг.\n\n"
        "Бекор қилиш учун /cancel ёзинг.",
        parse_mode="HTML",
    )


@router.message(AdminReplyStates.waiting_text, F.text == "/cancel")
async def admin_reply_cancel(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.clear()
    await message.answer("Жавоб бериш бекор қилинди.")


@router.message(AdminReplyStates.waiting_text, F.text)
async def admin_reply_send(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()
    target_id = data["target_telegram_id"]
    application_id = data["application_id"]

    try:
        await message.bot.send_message(
            target_id,
            "<b>📩 XJ BUSINESS LAUNCH АДМИНИСТРАТОРИДАН ЖАВОБ</b>\n\n"
            + escape(message.text),
            parse_mode="HTML",
        )
        await set_application_status(application_id, "replied", admin_note=message.text)
        await message.answer("✅ Жавоб фойдаланувчига бот орқали юборилди.")
    except Exception as e:
        await message.answer(f"❌ Жавоб юборилмади: {escape(str(e))}", parse_mode="HTML")

    await state.clear()


@router.callback_query(F.data.startswith("admin_select:"))
async def admin_select(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Рухсат йўқ.", show_alert=True)
        return

    application_id = int(callback.data.split(":")[1])
    app, user = await get_application_with_user(application_id)

    if not app or not user:
        await callback.answer("Ариза топилмади.", show_alert=True)
        return

    await set_application_status(application_id, "selected")

    await callback.bot.send_message(
        user.telegram_id,
        "<b>🎉 ТАБРИКЛАЙМИЗ!</b>\n\n"
        "Сизнинг Махсус танлов аризангиз танлаб олинди.\n\n"
        "Сизга кейинги ташкилий маълумотлар шу бот орқали юборилади.",
        parse_mode="HTML",
    )

    await callback.answer("Танланди ✅")
    await callback.message.answer(
        f"✅ Ариза №{application_id}: <b>{escape(user.full_name)}</b> танланди.",
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("admin_reject:"))
async def admin_reject(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Рухсат йўқ.", show_alert=True)
        return

    application_id = int(callback.data.split(":")[1])
    app, user = await get_application_with_user(application_id)

    if not app or not user:
        await callback.answer("Ариза топилмади.", show_alert=True)
        return

    await set_application_status(application_id, "rejected")

    await callback.bot.send_message(
        user.telegram_id,
        "<b>Махсус танлов бўйича жавоб</b>\n\n"
        "Аризангиз кўриб чиқилди. Бу сафар танловдан ўтмадингиз.\n\n"
        "XJ BUSINESS LAUNCH’нинг кейинги имкониятлари ва расмий эълонларини кузатиб боринг.",
        parse_mode="HTML",
    )

    await callback.answer("Танланмади ❌")
    await callback.message.answer(
        f"❌ Ариза №{application_id}: <b>{escape(user.full_name)}</b> танланмади.",
        parse_mode="HTML",
    )

