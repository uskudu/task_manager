import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await client.post(
        "/api/v1/tasks",
        json={"title": "First Task", "description": "Test description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "First Task"
    assert data["description"] == "Test description"
    assert data["status"] == "CREATED"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_tasks(client: AsyncClient):
    # first create a task
    await client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "description": "For listing"},
    )

    response = await client.get("/api/v1/tasks")
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
        "/api/v1/tasks",
        json={"title": "Check single", "description": "Single task test"},
    )
    task_id = response.json()["id"]

    # ерут get it
    response = await client.get(f"/api/v1/tasks/{task_id}")
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
        "/api/v1/tasks", json={"title": "Update me", "description": "Before update"}
    )
    task_id = response.json()["id"]

    # гpdate the task
    response = await client.put(
        f"/api/v1/tasks/{task_id}",
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
    response = await client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["status"] == "IN_PROGRESS"


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    # create a task first
    response = await client.post(
        "/api/v1/tasks", json={"title": "Delete me", "description": "To be deleted"}
    )
    task_id = response.json()["id"]

    # delete the task
    response = await client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200

    # verify the task is gone
    response = await client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 404

    # verify it's not in the list either
    response = await client.get("/api/v1/tasks")
    assert response.status_code == 200
    tasks = response.json()
    task_ids = [task["id"] for task in tasks]
    assert task_id not in task_ids


@pytest.mark.asyncio
async def test_get_nonexistent_task(client: AsyncClient):
    # try to get a task that doesn't exist
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/tasks/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_nonexistent_task(client: AsyncClient):
    # try to update a task that doesn't exist
    fake_id = str(uuid.uuid4())
    response = await client.put(
        f"/api/v1/tasks/{fake_id}",
        json={"title": "Test", "description": "Test", "status": "DONE"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_task(client: AsyncClient):
    # try to delete a task that doesn't exist
    fake_id = str(uuid.uuid4())
    response = await client.delete(f"/api/v1/tasks/{fake_id}")
    assert response.status_code == 404
