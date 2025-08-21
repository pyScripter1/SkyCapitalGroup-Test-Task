import pytest
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.exceptions import TaskNotFoundError


def test_create_task(db: Session):
    task_data = schemas.TaskCreate(title="Test Task", description="Test Description")
    task = crud.create_task(db, task_data)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == models.TaskStatus.CREATED
    assert task.uuid is not None


def test_get_task(db: Session):
    task_data = schemas.TaskCreate(title="Test Task")
    created_task = crud.create_task(db, task_data)

    retrieved_task = crud.get_task(db, created_task.uuid)
    assert retrieved_task.uuid == created_task.uuid
    assert retrieved_task.title == "Test Task"


def test_get_nonexistent_task(db: Session):
    with pytest.raises(TaskNotFoundError):
        crud.get_task(db, "nonexistent-uuid")


def test_get_tasks(db: Session):
    # Create test tasks
    for i in range(5):
        task_data = schemas.TaskCreate(title=f"Task {i}")
        crud.create_task(db, task_data)

    tasks = crud.get_tasks(db)
    assert len(tasks) == 5
    assert tasks[0].title == "Task 4"  # Should be ordered by created_at desc


def test_update_task(db: Session):
    task_data = schemas.TaskCreate(title="Old Title")
    task = crud.create_task(db, task_data)

    update_data = schemas.TaskUpdate(
        title="New Title",
        status=models.TaskStatus.IN_PROGRESS
    )
    updated_task = crud.update_task(db, task.uuid, update_data)

    assert updated_task.title == "New Title"
    assert updated_task.status == models.TaskStatus.IN_PROGRESS


def test_delete_task(db: Session):
    task_data = schemas.TaskCreate(title="Test Task")
    task = crud.create_task(db, task_data)

    crud.delete_task(db, task.uuid)

    with pytest.raises(TaskNotFoundError):
        crud.get_task(db, task.uuid)


def test_get_tasks_stats(db: Session):
    # Create tasks with different statuses
    tasks_data = [
        ("Task 1", models.TaskStatus.CREATED),
        ("Task 2", models.TaskStatus.IN_PROGRESS),
        ("Task 3", models.TaskStatus.COMPLETED),
        ("Task 4", models.TaskStatus.CREATED),
    ]

    for title, status in tasks_data:
        task = models.Task(title=title, status=status)
        db.add(task)
    db.commit()

    stats = crud.get_tasks_stats(db)

    assert stats["total"] == 4
    assert stats["created"] == 2
    assert stats["in_progress"] == 1
    assert stats["completed"] == 1