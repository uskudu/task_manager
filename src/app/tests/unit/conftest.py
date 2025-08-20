import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.db.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.session import get_session


DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(DATABASE_URL_TEST, future=True, echo=False)

async_session_maker_test = async_sessionmaker(
    engine_test, expire_on_commit=False, class_=AsyncSession
)


# db dep override
async def override_get_db():
    async with async_session_maker_test() as session:
        yield session


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
