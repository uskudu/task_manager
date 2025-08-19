from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class StatusEnum(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskReadSchema(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    status: StatusEnum

    model_config = ConfigDict(from_attributes=True)


class TaskCreateSchema(BaseModel):
    title: str
    description: str | None = None


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    status: StatusEnum | None = None
