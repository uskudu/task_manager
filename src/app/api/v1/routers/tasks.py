from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.db.session import get_session

from app.schemas.task import TaskReadSchema, TaskCreateSchema, TaskUpdateSchema

router = APIRouter(prefix="/tasks")


async def get_task_service(session=Depends(get_session)) -> TaskService:
    repo = TaskRepository(session)
    return TaskService(repo)


@router.post("/", response_model=TaskReadSchema)
async def create_task(
    data: TaskCreateSchema,
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(data.title, data.description)


@router.get("/{task_id}", response_model=TaskReadSchema | None)
async def get_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.get("/", response_model=list[TaskReadSchema])
async def list_tasks(service: TaskService = Depends(get_task_service)):
    return await service.list_tasks()


@router.put("/{task_id}", response_model=TaskReadSchema | None)
async def update_task(
    task_id: UUID,
    data: TaskUpdateSchema,
    service: TaskService = Depends(get_task_service),
):
    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
    task = await service.update_task(task_id, update_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return {"deleted": success}
