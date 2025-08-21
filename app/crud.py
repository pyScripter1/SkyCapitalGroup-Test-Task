from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from .models import Task, TaskStatus
from .schemas import TaskCreate, TaskUpdate
from .exceptions import TaskNotFoundError, TaskValidationError

# получение задачи по uuid с проверкой на наличие
def get_task(db: Session, task_uuid: str) -> Task:
    task = db.query(Task).filter(Task.uuid == task_uuid).first()
    if not task:
        raise TaskNotFoundError(task_uuid)
    return task

# поулчаем все задачи
def get_tasks(
        db: Session,
        status: Optional[TaskStatus] = None,
        offset: int = 0,
        limit: int = 100
) -> List[Task]:
    query = db.query(Task).order_by(desc(Task.created_at))

    if status:
        query = query.filter(Task.status == status)

    return query.offset(offset).limit(limit).all()

# создание задачи с добавление в бд
def create_task(db: Session, task_data: TaskCreate) -> Task:
    task = Task(
        title=task_data.title,
        description=task_data.description or ""
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# обновление задачи
def update_task(db: Session, task_uuid: str, task_data: TaskUpdate) -> Task:
    task = get_task(db, task_uuid)

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.status is not None:
        task.status = task_data.status

    db.commit()
    db.refresh(task)
    return task

# удаление задачи
def delete_task(db: Session, task_uuid: str) -> None:
    task = get_task(db, task_uuid)
    db.delete(task)
    db.commit()

# получение кол-ва задач
def get_tasks_count(db: Session) -> int:
    return db.query(Task).count()

# получаем статистику по задачам
def get_tasks_stats(db: Session) -> dict:
    total = db.query(Task).count()
    created = db.query(Task).filter(Task.status == TaskStatus.CREATED).count()
    in_progress = db.query(Task).filter(Task.status == TaskStatus.IN_PROGRESS).count()
    completed = db.query(Task).filter(Task.status == TaskStatus.COMPLETED).count()

    return {
        "total": total,
        "created": created,
        "in_progress": in_progress,
        "completed": completed
    }