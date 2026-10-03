from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_application_keyboard(application_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ðŸ’¬ Ð–Ð°Ð²Ð¾Ð± Ñ‘Ð·Ð¸Ñˆ",
                    callback_data=f"admin_reply:{application_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="âœ… Ð¢Ð°Ð½Ð»Ð°Ð½Ð´Ð¸",
                    callback_data=f"admin_select:{application_id}"
                ),
                InlineKeyboardButton(
                    text="âŒ Ð¢Ð°Ð½Ð»Ð°Ð½Ð¼Ð°Ð´Ð¸",
                    callback_data=f"admin_reject:{application_id}"
                ),
            ],
        ]
    )

