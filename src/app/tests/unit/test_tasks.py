import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.db.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# from sqlalchemy.orm import sessionmaker
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
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await client.post(
        "/api/v1/tasks/",
        json={"title": "First Task", "description": "Test description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "First Task"
    assert data["description"] == "Test description"
    assert data["status"] == "CREATED"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_tasks(client: AsyncClient):
    # first create a task
    await client.post(
        "/api/v1/tasks/",
        json={"title": "Test Task", "description": "For listing"},
    )

    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0]
    assert "title" in data[0]
    assert "status" in data[0]


@pytest.mark.asyncio
async def test_get_task_by_id(client: AsyncClient):
    # create a task first
    response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Check single", "description": "Single task test"},
    )
    task_id = response.json()["id"]

    # ерут get it
    response = await client.get(f"/api/v1/tasks/{task_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Check single"
    assert data["description"] == "Single task test"
    assert data["status"] == "CREATED"


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    # create a task first
    response = await client.post(
        "/api/v1/tasks/", json={"title": "Update me", "description": "Before update"}
    )
    task_id = response.json()["id"]

    # гpdate the task
    response = await client.put(
        f"/api/v1/tasks/{task_id}/",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "status": "IN_PROGRESS",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"
    assert data["status"] == "IN_PROGRESS"

    # verify the update by getting the task again
    response = await client.get(f"/api/v1/tasks/{task_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["status"] == "IN_PROGRESS"


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    # create a task first
    response = await client.post(
        "/api/v1/tasks/", json={"title": "Delete me", "description": "To be deleted"}
    )
    task_id = response.json()["id"]

    # delete the task
    response = await client.delete(f"/api/v1/tasks/{task_id}/")
    assert response.status_code == 204

    # verify the task is gone
    response = await client.get(f"/api/v1/tasks/{task_id}/")
    assert response.status_code == 404

    # verify it's not in the list either
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    task_ids = [task["id"] for task in tasks]
    assert task_id not in task_ids


@pytest.mark.asyncio
async def test_get_nonexistent_task(client: AsyncClient):
    # try to get a task that doesn't exist
    response = await client.get("/api/v1/tasks/nonexistent-id/")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_nonexistent_task(client: AsyncClient):
    # try to update a task that doesn't exist
    response = await client.put(
        "/api/v1/tasks/nonexistent-id/",
        json={"title": "Test", "description": "Test", "status": "DONE"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_task(client: AsyncClient):
    # try to delete a task that doesn't exist
    response = await client.delete("/api/v1/tasks/nonexistent-id/")
    assert response.status_code == 404
