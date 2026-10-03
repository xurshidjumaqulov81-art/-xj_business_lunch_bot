from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def phone_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Телефон рақамимни юбориш", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Телефон рақамингизни юборинг",
    )


def confirm_profile_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ҳа, давом этиш", callback_data="profile_confirm")],
            [InlineKeyboardButton(text="✏️ Таҳрирлаш", callback_data="profile_edit")],
        ]
    )


def confirm_launch_registration_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ҳа, рўйхатдан ўтаман", callback_data="register_launch_confirm")],
            [InlineKeyboardButton(text="🔙 Асосий меню", callback_data="main_menu")],
        ]
    )

