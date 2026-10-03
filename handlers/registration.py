from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.db import get_user_by_telegram_id, register_for_launch
from keyboards.registration import confirm_launch_registration_keyboard
from keyboards.main_menu import back_to_menu_inline
from services.media import send_section

router = Router()


REGISTRATION_INFO = """<b>✅ BUSINESS LAUNCH’ГА РЎЙХАТДАН ЎТИШ</b>

Сиз Business Launch дастурида қатнашиш учун рўйхатдан ўтишингиз мумкин.

Рўйхатдан ўтган иштирокчиларга дастурга оид муҳим маълумотлар бот орқали юборилади:

📅 сана
📍 манзил
📋 шартлар
⏰ эслатмалар
🔥 махсус эълонлар

<b>Business Launch’га рўйхатдан ўтишни тасдиқлайсизми?</b>"""


async def show_registration(message: Message, telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        await message.answer("Аввал /start орқали рўйхатдан ўтинг.")
        return

    await send_section(
        message,
        "registration",
        REGISTRATION_INFO,
        confirm_launch_registration_keyboard(),
    )


@router.message(F.text == "✅ Рўйхатдан ўтиш")
async def register_launch_message(message: Message):
    await show_registration(message, message.from_user.id)


@router.callback_query(F.data == "register_launch")
async def register_launch_callback(callback: CallbackQuery):
    await callback.answer()
    await show_registration(callback.message, callback.from_user.id)


@router.callback_query(F.data == "register_launch_confirm")
async def register_launch_confirm(callback: CallbackQuery):
    await callback.answer()

    user = await register_for_launch(callback.from_user.id)
    if not user:
        await callback.message.answer("Аввал /start орқали рўйхатдан ўтинг.")
        return

    await callback.message.answer(
        "<b>Рўйхатдан ўтдингиз! ✅</b>\n\n"
        "Сиз XJ BUSINESS LAUNCH иштирокчилари рўйхатига қўшилдингиз.\n\n"
        "Кейинги расмий эълонларни кузатиб боринг.\n\n"
        "<b>Business Launch — сизнинг кейинги босқичингиз. 🔥</b>",
        reply_markup=back_to_menu_inline(),
        parse_mode="HTML",
    )

