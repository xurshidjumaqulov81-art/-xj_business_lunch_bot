from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from config import OFFICIAL_CHANNEL_URL


def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏆 Business Launch ҳақида маълумот")],
            [KeyboardButton(text="👤 Founder Day ҳақида маълумот")],
            [KeyboardButton(text="🍽 Founder Lunch ҳақида маълумот")],
            [KeyboardButton(text="📋 Қатнашиш шартлари ҳақида маълумот")],
            [KeyboardButton(text="🎁 Махсус танлов ҳақида маълумот")],
            [KeyboardButton(text="✍️ Махсус танловга қатнашиш")],
            [KeyboardButton(text="✅ Рўйхатдан ўтиш")],
            [KeyboardButton(text="❓ Савол-жавоб")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Керакли бўлимни танланг",
    )


def back_to_menu_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Асосий меню", callback_data="main_menu")]
        ]
    )


def business_launch_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Қатнашиш шартлари", callback_data="conditions")],
            [InlineKeyboardButton(text="✅ Рўйхатдан ўтиш", callback_data="register_launch")],
            [InlineKeyboardButton(text="🔙 Асосий меню", callback_data="main_menu")],
        ]
    )


def founder_day_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Қатнашиш шартлари", callback_data="conditions")],
            [InlineKeyboardButton(text="🎁 Махсус танлов", callback_data="contest_info")],
            [InlineKeyboardButton(text="🔙 Асосий меню", callback_data="main_menu")],
        ]
    )


def founder_lunch_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Қатнашиш шартлари", callback_data="conditions")],
            [InlineKeyboardButton(text="✅ Рўйхатдан ўтиш", callback_data="register_launch")],
            [InlineKeyboardButton(text="🔙 Асосий меню", callback_data="main_menu")],
        ]
    )


def conditions_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 XJ расмий канали", url=OFFICIAL_CHANNEL_URL)],
            [InlineKeyboardButton(text="🎁 Махсус танлов ҳақида", callback_data="contest_info")],
            [InlineKeyboardButton(text="✍️ Махсус танловга қатнашиш", callback_data="contest_start")],
            [InlineKeyboardButton(text="🔙 Асосий меню", callback_data="main_menu")],
        ]
    )


def contest_info_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Махсус танловга қатнашиш", callback_data="contest_start")],
            [InlineKeyboardButton(text="🔙 Асосий меню", callback_data="main_menu")],
        ]
    )


def faq_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Махсус танловга қатнашиш", callback_data="contest_start")],
            [InlineKeyboardButton(text="✅ Рўйхатдан ўтиш", callback_data="register_launch")],
            [InlineKeyboardButton(text="🔙 Асосий меню", callback_data="main_menu")],
        ]
    )

