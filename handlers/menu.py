from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.db import get_user_by_telegram_id
from keyboards.main_menu import (
    main_menu_keyboard,
    business_launch_inline,
    founder_day_inline,
    founder_lunch_inline,
    conditions_inline,
    contest_info_inline,
    faq_inline,
)
from services.media import send_section
from services.texts import (
    WELCOME_MENU,
    BUSINESS_LAUNCH,
    FOUNDER_DAY,
    FOUNDER_LUNCH,
    CONDITIONS,
    CONTEST_INFO,
    FAQ,
)

router = Router()


async def show_main_menu(message: Message, telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    name = user.full_name if user else "иштирокчи"

    await message.answer(
        WELCOME_MENU.format(name=name),
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    await callback.answer()
    await show_main_menu(callback.message, callback.from_user.id)


@router.message(F.text == "🏆 Business Launch ҳақида маълумот")
async def business_launch(message: Message):
    await send_section(
        message,
        "business_launch",
        BUSINESS_LAUNCH,
        business_launch_inline(),
    )


@router.message(F.text == "👤 Founder Day ҳақида маълумот")
async def founder_day(message: Message):
    await send_section(
        message,
        "founder_day",
        FOUNDER_DAY,
        founder_day_inline(),
    )


@router.message(F.text == "🍽 Founder Lunch ҳақида маълумот")
async def founder_lunch(message: Message):
    await send_section(
        message,
        "founder_lunch",
        FOUNDER_LUNCH,
        founder_lunch_inline(),
    )


@router.message(F.text == "📋 Қатнашиш шартлари ҳақида маълумот")
async def conditions(message: Message):
    await send_section(
        message,
        "conditions",
        CONDITIONS,
        conditions_inline(),
    )


@router.message(F.text == "🎁 Махсус танлов ҳақида маълумот")
async def contest_info(message: Message):
    await send_section(
        message,
        "contest_info",
        CONTEST_INFO,
        contest_info_inline(),
    )


@router.message(F.text == "❓ Савол-жавоб")
async def faq(message: Message):
    await send_section(
        message,
        "faq",
        FAQ,
        faq_inline(),
    )


@router.callback_query(F.data == "conditions")
async def conditions_cb(callback: CallbackQuery):
    await callback.answer()
    await send_section(
        callback.message,
        "conditions",
        CONDITIONS,
        conditions_inline(),
    )


@router.callback_query(F.data == "contest_info")
async def contest_info_cb(callback: CallbackQuery):
    await callback.answer()
    await send_section(
        callback.message,
        "contest_info",
        CONTEST_INFO,
        contest_info_inline(),
    )

