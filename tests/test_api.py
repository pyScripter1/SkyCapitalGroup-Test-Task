import pytest
from fastapi.testclient import TestClient
from app import models


def test_create_task(client: TestClient):
    response = client.post("/api/v1/tasks/", json={
        "title": "Test Task",
        "description": "Test Description"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "создано"
    assert "uuid" in data


def test_create_task_validation(client: TestClient):
    response = client.post("/api/v1/tasks/", json={"title": ""})
    assert response.status_code == 422


def test_get_task(client: TestClient):
    create_response = client.post("/api/v1/tasks/", json={"title": "Test Task"})
    task_uuid = create_response.json()["uuid"]

    response = client.get(f"/api/v1/tasks/{task_uuid}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"


def test_get_nonexistent_task(client: TestClient):
    response = client.get("/api/v1/tasks/nonexistent-uuid")
    assert response.status_code == 404


def test_get_tasks(client: TestClient):
    for i in range(3):
        client.post("/api/v1/tasks/", json={"title": f"Task {i}"})

    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 3
    assert data["total"] == 3


def test_update_task(client: TestClient):
    create_response = client.post("/api/v1/tasks/", json={"title": "Old Title"})
    task_uuid = create_response.json()["uuid"]

    update_response = client.put(f"/api/v1/tasks/{task_uuid}", json={
        "title": "New Title",
        "status": "в работе"
    })

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "в работе"


def test_delete_task(client: TestClient):
    create_response = client.post("/api/v1/tasks/", json={"title": "Test Task"})
    task_uuid = create_response.json()["uuid"]

    delete_response = client.delete(f"/api/v1/tasks/{task_uuid}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/tasks/{task_uuid}")
    assert get_response.status_code == 404


def test_get_stats(client: TestClient):
    # Create tasks with different statuses
    tasks = [
        {"title": "Task 1", "status": "создано"},
        {"title": "Task 2", "status": "в работе"},
        {"title": "Task 3", "status": "завершено"},
    ]

    for task in tasks:
        client.post("/api/v1/tasks/", json=task)

    response = client.get("/api/v1/stats/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["created"] == 1
    assert data["in_progress"] == 1
    assert data["completed"] == 1