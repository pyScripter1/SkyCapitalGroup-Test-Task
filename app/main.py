from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from . import crud, schemas, models
from .database import get_db, init_db
from .exceptions import TaskNotFoundError

# настраиваем приложение с док
app = FastAPI(
    title="Task Manager API",
    description="CRUD API для управления задачами",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# инициализация бд при старте
@app.on_event("startup")
def on_startup():
    init_db()

# корневая точка
@app.get("/")
async def root():
    return {"message": "Task Manager API"}

# создание задачи
@app.post(
    "/api/v1/tasks/",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу",
    tags=["Tasks"]
)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Создает новую задачу с указанным названием и описанием."""
    return crud.create_task(db, task)


@app.get(
    "/api/v1/tasks/{task_uuid}",
    response_model=schemas.TaskResponse,
    summary="Получить задачу по UUID",
    tags=["Tasks"]
)
def read_task(task_uuid: str, db: Session = Depends(get_db)):
    """Возвращает задачу по ее UUID."""
    try:
        return crud.get_task(db, task_uuid)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get(
    "/api/v1/tasks/",
    response_model=schemas.TaskListResponse,
    summary="Получить список задач",
    tags=["Tasks"]
)
def read_tasks(
        status: Optional[schemas.TaskStatus] = Query(None, description="Фильтр по статусу"),
        offset: int = Query(0, ge=0, description="Смещение для пагинации"),
        limit: int = Query(100, ge=1, le=1000, description="Лимит задач"),
        db: Session = Depends(get_db)
):
    """Возвращает список задач с возможностью фильтрации по статусу и пагинацией."""
    tasks = crud.get_tasks(db, status=status, offset=offset, limit=limit)
    total = crud.get_tasks_count(db)

    return {
        "tasks": tasks,
        "total": total,
        "offset": offset,
        "limit": limit
    }


@app.put(
    "/api/v1/tasks/{task_uuid}",
    response_model=schemas.TaskResponse,
    summary="Обновить задачу",
    tags=["Tasks"]
)
def update_task(
        task_uuid: str,
        task_data: schemas.TaskUpdate,
        db: Session = Depends(get_db)
):
    """Обновляет данные задачи по UUID."""
    try:
        return crud.update_task(db, task_uuid, task_data)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete(
    "/api/v1/tasks/{task_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу",
    tags=["Tasks"]
)
def delete_task(task_uuid: str, db: Session = Depends(get_db)):
    """Удаляет задачу по UUID."""
    try:
        crud.delete_task(db, task_uuid)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get(
    "/api/v1/stats/",
    response_model=schemas.TaskStatsResponse,
    summary="Получить статистику по задачам",
    tags=["Statistics"]
)
def get_stats(db: Session = Depends(get_db)):
    """Возвращает статистику по задачам."""
    return crud.get_tasks_stats(db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)