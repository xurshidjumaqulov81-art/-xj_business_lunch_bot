from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from database.db import get_user_by_telegram_id, upsert_user
from keyboards.registration import phone_keyboard, confirm_profile_keyboard
from keyboards.main_menu import main_menu_keyboard
from services.validators import is_valid_xj_id
from services.texts import START_TEXT, ASK_XJ_ID, INVALID_XJ_ID, ASK_PHONE, WELCOME_MENU
from services.notifications import notify_admins_new_user

router = Router()


class RegistrationStates(StatesGroup):
    full_name = State()
    xj_id = State()
    phone = State()
    confirm = State()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()

    user = await get_user_by_telegram_id(message.from_user.id)
    if user:
        await message.answer(
            WELCOME_MENU.format(name=user.full_name),
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML",
        )
        return

    await state.set_state(RegistrationStates.full_name)
    await message.answer(
        START_TEXT,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML",
    )


@router.message(RegistrationStates.full_name, F.text)
async def get_full_name(message: Message, state: FSMContext):
    full_name = message.text.strip()

    if len(full_name) < 3:
        await message.answer("Илтимос, исм ва фамилиянгизни тўлиқ киритинг.")
        return

    await state.update_data(full_name=full_name)
    await state.set_state(RegistrationStates.xj_id)
    await message.answer(ASK_XJ_ID, parse_mode="HTML")


@router.message(RegistrationStates.xj_id, F.text)
async def get_xj_id(message: Message, state: FSMContext):
    xj_id = message.text.strip()

    if not is_valid_xj_id(xj_id):
        await message.answer(INVALID_XJ_ID, parse_mode="HTML")
        return

    await state.update_data(xj_id=xj_id)
    await state.set_state(RegistrationStates.phone)
    await message.answer(
        ASK_PHONE,
        reply_markup=phone_keyboard(),
        parse_mode="HTML",
    )


@router.message(RegistrationStates.phone, F.contact)
async def get_phone_contact(message: Message, state: FSMContext):
    # Қўшимча хавфсизлик: контакт фойдаланувчининг ўзига тегишли бўлиши керак
    if message.contact.user_id and message.contact.user_id != message.from_user.id:
        await message.answer(
            "Илтимос, айнан ўзингизнинг телефон рақамингизни пастдаги тугма орқали юборинг."
        )
        return

    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    data = await state.get_data()

    await state.set_state(RegistrationStates.confirm)

    text = (
        "<b>Маълумотларингизни текширинг:</b>\n\n"
        f"👤 Исм-фамилия: {data['full_name']}\n"
        f"🆔 XJ ID: <code>{data['xj_id']}</code>\n"
        f"📱 Телефон: {phone}\n\n"
        "Маълумотлар тўғрими?"
    )

    await message.answer(
        text,
        reply_markup=confirm_profile_keyboard(),
        parse_mode="HTML",
    )


@router.message(RegistrationStates.phone)
async def phone_only_contact(message: Message):
    await message.answer(
        "Телефон рақамингизни пастдаги <b>📱 Телефон рақамимни юбориш</b> тугмаси орқали юборинг.",
        reply_markup=phone_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "profile_edit")
async def edit_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await state.set_state(RegistrationStates.full_name)
    await callback.message.answer(
        "Маълумотларни қайта киритамиз.\n\n<b>Исм ва фамилиянгизни киритинг.</b>\n\nМасалан: <b>Алишер Каримов</b>",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML",
    )


@router.callback_query(RegistrationStates.confirm, F.data == "profile_confirm")
async def confirm_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    tg = callback.from_user

    user = await upsert_user(
        telegram_id=tg.id,
        telegram_username=tg.username,
        telegram_first_name=tg.first_name,
        telegram_last_name=tg.last_name,
        full_name=data["full_name"],
        xj_id=data["xj_id"],
        phone=data["phone"],
    )

    await state.clear()

    await notify_admins_new_user(callback.bot, user)

    await callback.message.answer(
        WELCOME_MENU.format(name=user.full_name),
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )

