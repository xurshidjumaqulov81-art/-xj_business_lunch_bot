from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from config import DATABASE_URL
from database.models import Base, User, ContestApplication


def normalize_database_url(url: str) -> str:
    # Railway often provides postgresql://...
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


DB_URL = normalize_database_url(DATABASE_URL)

engine = create_async_engine(
    DB_URL,
    echo=False,
    pool_pre_ping=True,
)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_user_by_telegram_id(telegram_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()


async def upsert_user(
    telegram_id: int,
    telegram_username: str | None,
    telegram_first_name: str | None,
    telegram_last_name: str | None,
    full_name: str,
    xj_id: str,
    phone: str,
):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_id=telegram_id,
                telegram_username=telegram_username,
                telegram_first_name=telegram_first_name,
                telegram_last_name=telegram_last_name,
                full_name=full_name,
                xj_id=xj_id,
                phone=phone,
            )
            session.add(user)
        else:
            user.telegram_username = telegram_username
            user.telegram_first_name = telegram_first_name
            user.telegram_last_name = telegram_last_name
            user.full_name = full_name
            user.xj_id = xj_id
            user.phone = phone

        await session.commit()
        await session.refresh(user)
        return user


async def save_contest_application(
    user_id: int,
    about: str,
    goal: str,
    why_founder: str,
    one_question: str,
    after_meeting: str,
):
    async with SessionLocal() as session:
        app = ContestApplication(
            user_id=user_id,
            about=about,
            goal=goal,
            why_founder=why_founder,
            one_question=one_question,
            after_meeting=after_meeting,
        )
        session.add(app)
        await session.commit()
        await session.refresh(app)
        return app


async def get_application_with_user(application_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(ContestApplication, User)
            .join(User, ContestApplication.user_id == User.id)
            .where(ContestApplication.id == application_id)
        )
        row = result.first()
        if not row:
            return None, None
        return row[0], row[1]


async def set_application_status(application_id: int, status: str, admin_note: str | None = None):
    async with SessionLocal() as session:
        result = await session.execute(
            select(ContestApplication).where(ContestApplication.id == application_id)
        )
        app = result.scalar_one_or_none()
        if not app:
            return None
        app.status = status
        if admin_note is not None:
            app.admin_note = admin_note
        await session.commit()
        await session.refresh(app)
        return app


async def register_for_launch(telegram_id: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return None
        user.is_registered_for_launch = True
        await session.commit()
        await session.refresh(user)
        return user


