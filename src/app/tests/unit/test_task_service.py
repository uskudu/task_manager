import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from app.services.task_service import TaskService
from app.models.task import Task


@pytest.mark.asyncio
async def test_create_task():
    repo = AsyncMock()
    repo.create.return_value = Task(title="a", description="b")
    service = TaskService(repo)

    task = await service.create_task("a", "b")
    repo.create.assert_called_once_with({"title": "a", "description": "b"})
    assert task.title == "a"


@pytest.mark.asyncio
async def test_update_task():
    repo = AsyncMock()
    repo.update.return_value = "updated_task"
    service = TaskService(repo)

    result = await service.update_task(uuid4(), {"status": "DONE"})
    repo.update.assert_called_once()
    assert result == "updated_task"


@pytest.mark.asyncio
async def test_get_task():
    repo = AsyncMock()
    repo.get.return_value = "task"
    service = TaskService(repo)

    result = await service.get_task(uuid4())
    repo.get.assert_called_once()
    assert result == "task"


@pytest.mark.asyncio
async def test_delete_task():
    repo = AsyncMock()
    repo.delete.return_value = True
    service = TaskService(repo)

    result = await service.delete_task(uuid4())
    repo.delete.assert_called_once()
    assert result is True
