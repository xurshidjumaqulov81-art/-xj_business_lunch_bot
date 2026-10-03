from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from database.db import get_user_by_telegram_id, save_contest_application
from keyboards.main_menu import back_to_menu_inline
from services.notifications import notify_admins_application
from services.texts import CONTEST_START
from services.media import send_section

router = Router()


class ContestStates(StatesGroup):
    about = State()
    goal = State()
    why_founder = State()
    one_question = State()
    after_meeting = State()


async def begin_contest(message: Message, state: FSMContext, telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        await message.answer("Аввал /start орқали рўйхатдан ўтинг.")
        return

    await state.clear()
    await state.set_state(ContestStates.about)

    # 6-расм: Maxsus tanlovga qatnashish
    await send_section(
        message,
        "contest_apply",
        CONTEST_START,
    )


@router.message(F.text == "✍️ Махсус танловга қатнашиш")
async def contest_start_message(message: Message, state: FSMContext):
    await begin_contest(message, state, message.from_user.id)


@router.callback_query(F.data == "contest_start")
async def contest_start_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await begin_contest(callback.message, state, callback.from_user.id)


@router.message(ContestStates.about, F.text)
async def contest_about(message: Message, state: FSMContext):
    await state.update_data(about=message.text.strip())
    await state.set_state(ContestStates.goal)
    await message.answer(
        "<b>2/5. XJ бизнесида қандай мақсадингиз бор?</b>\n\n"
        "Қайси даражага чиқмоқчисиз? XJ орқали келажакда нималарга эришишни хоҳлайсиз?",
        parse_mode="HTML",
    )


@router.message(ContestStates.goal, F.text)
async def contest_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text.strip())
    await state.set_state(ContestStates.why_founder)
    await message.answer(
        "<b>3/5. Нега Xurshid Ilhamiddinovich билан шахсан учрашмоқчисиз?</b>\n\n"
        "Фикрингизни эркин ва самимий ёзинг.",
        parse_mode="HTML",
    )


@router.message(ContestStates.why_founder, F.text)
async def contest_why_founder(message: Message, state: FSMContext):
    await state.update_data(why_founder=message.text.strip())
    await state.set_state(ContestStates.one_question)
    await message.answer(
        "<b>4/5. Агар компания асосчисига фақат битта савол бериш имконияти берилса, қандай савол берган бўлардингиз?</b>",
        parse_mode="HTML",
    )


@router.message(ContestStates.one_question, F.text)
async def contest_one_question(message: Message, state: FSMContext):
    await state.update_data(one_question=message.text.strip())
    await state.set_state(ContestStates.after_meeting)
    await message.answer(
        "<b>5/5. Агар ушбу учрашувга танлансангиз, ундан кейин бизнесингизда нимани ўзгартирмоқчисиз?</b>",
        parse_mode="HTML",
    )


@router.message(ContestStates.after_meeting, F.text)
async def contest_after_meeting(message: Message, state: FSMContext):
    await state.update_data(after_meeting=message.text.strip())
    data = await state.get_data()

    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        await state.clear()
        await message.answer("Аввал /start орқали рўйхатдан ўтинг.")
        return

    app = await save_contest_application(
        user_id=user.id,
        about=data["about"],
        goal=data["goal"],
        why_founder=data["why_founder"],
        one_question=data["one_question"],
        after_meeting=data["after_meeting"],
    )

    await state.clear()

    await notify_admins_application(message.bot, user, app)

    await message.answer(
        "<b>Аризангиз қабул қилинди! ✅</b>\n\n"
        f"Раҳмат, <b>{user.full_name}</b>.\n\n"
        "Сизнинг жавобларингиз Махсус танлов учун кўриб чиқилади.\n\n"
        "Барча аризалар орасидан <b>2 нафар иштирокчи танлаб олинади.</b>\n\n"
        "Аризангиз бўйича жавоб <b>шу бот орқали юборилади.</b> "
        "Зарур ҳолатда администратор сиз билан бот орқали ёзишади.\n\n"
        "<b>Танланган 2 иштирокчидан бири сиз бўлишингиз мумкин. 🔥</b>",
        reply_markup=back_to_menu_inline(),
        parse_mode="HTML",
    )

