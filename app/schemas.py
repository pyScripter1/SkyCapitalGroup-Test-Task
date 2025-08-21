from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from .models import TaskStatus


class TaskBase(BaseModel):
    # валидация данных
    title: str = Field(..., min_length=1, max_length=200, description="Название задачи")
    description: Optional[str] = Field(default="", max_length=1000, description="Описание задачи")


class TaskCreate(TaskBase):
    @validator('title')
    def title_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Название задачи не может быть пустым")
        return v.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None

    @validator('title')
    def title_not_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Название задачи не может быть пустым")
        return v.strip() if v else v


class TaskResponse(TaskBase):
    uuid: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    offset: int
    limit: int


class TaskStatsResponse(BaseModel):
    total: int
    created: int
    in_progress: int
    completed: int