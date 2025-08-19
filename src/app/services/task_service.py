from typing import Iterable, Optional
from uuid import UUID

from app.models.task import Task
from app.repositories.base import TaskRepositoryProtocol


class TaskService:
    def __init__(self, repo: TaskRepositoryProtocol):
        self.repo = repo

    async def create_task(self, title: str, description: str | None = None) -> Task:
        return await self.repo.create({"title": title, "description": description})

    async def get_task(self, task_id: UUID) -> Optional[Task]:
        return await self.repo.get(task_id)

    async def list_tasks(self, limit: int = 100, offset: int = 0) -> Iterable[Task]:
        return await self.repo.list(limit=limit, offset=offset)

    async def update_task(self, task_id: UUID, data: dict) -> Optional[Task]:
        return await self.repo.update(task_id, data)

    async def delete_task(self, task_id: UUID) -> bool:
        return await self.repo.delete(task_id)
