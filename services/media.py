from pathlib import Path

from aiogram.types import FSInputFile


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

SECTION_IMAGES = {
    "business_launch": ASSETS_DIR / "business_launch.jpg",
    "founder_day": ASSETS_DIR / "founder_day.jpg",
    "founder_lunch": ASSETS_DIR / "founder_lunch.jpg",
    "conditions": ASSETS_DIR / "conditions.jpg",
    "contest_info": ASSETS_DIR / "contest.jpg",
    "contest_apply": ASSETS_DIR / "contest_apply.jpg",
    "registration": ASSETS_DIR / "registration.jpg",
    "faq": ASSETS_DIR / "faq.jpg",
}


async def send_section(message, section: str, text: str, reply_markup=None):
    """
    Агар мос расм бор бўлса, аввал расмни алоҳида юборади.
    Кейин матн ва тугмаларни алоҳида юборади.

    Бу усул Telegram caption лимитига урилиб қолишни олдини олади.
    """
    path = SECTION_IMAGES.get(section)

    if path and path.exists():
        await message.answer_photo(photo=FSInputFile(path))

    await message.answer(
        text,
        reply_markup=reply_markup,
        parse_mode="HTML",
    )

