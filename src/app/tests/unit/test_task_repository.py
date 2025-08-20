import pytest
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, StatusEnum
from app.repositories.task_repository import TaskRepository


@pytest.mark.asyncio
async def test_create_task():
    session = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(session)

    data = {"title": "Test task", "description": "desc"}
    task = await repo.create(data)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(task)
    assert task.title == "Test task"
    assert task.description == "desc"
    assert task.status == StatusEnum.CREATED


@pytest.mark.asyncio
async def test_get_task():
    session = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(session)

    fake_task = Task(title="a", description="b")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_task

    session.execute.return_value = mock_result

    task = await repo.get(uuid4())
    assert task == fake_task


@pytest.mark.asyncio
async def test_update_task():
    session = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(session)

    session.execute.return_value = AsyncMock()
    session.commit.return_value = AsyncMock()
    repo.get = AsyncMock(return_value="updated_task")

    data = {"title": "New title"}
    result = await repo.update(uuid4(), data)
    session.execute.assert_called_once()
    session.commit.assert_called_once()
    assert result == "updated_task"


@pytest.mark.asyncio
async def test_delete_task():
    session = AsyncMock(spec=AsyncSession)
    repo = TaskRepository(session)

    session.execute.return_value.scalar_one_or_none.return_value = uuid4()
    session.commit.return_value = AsyncMock()

    deleted = await repo.delete(uuid4())
    session.commit.assert_called_once()
    assert deleted is True
