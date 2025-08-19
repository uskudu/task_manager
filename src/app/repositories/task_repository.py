from typing import Iterable, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.task import Task, StatusEnum


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict) -> Task:
        task = Task(
            title=data["title"],
            description=data.get("description"),
            status=StatusEnum.CREATED,
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, id: UUID) -> Optional[Task]:
        result = await self.session.execute(select(Task).where(Task.id == id))
        return result.scalar_one_or_none()

    async def list(self, limit: int = 100, offset: int = 0) -> Iterable[Task]:
        result = await self.session.execute(select(Task).offset(offset).limit(limit))
        return result.scalars().all()

    async def update(self, id: UUID, data: dict) -> Optional[Task]:
        await self.session.execute(
            update(Task)
            .where(Task.id == id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.commit()
        return await self.get(id)

    async def delete(self, id: UUID) -> bool:
        result = await self.session.execute(
            delete(Task).where(Task.id == id).returning(Task.id)
        )
        deleted_id = result.scalar_one_or_none()
        await self.session.commit()
        return deleted_id is not None
