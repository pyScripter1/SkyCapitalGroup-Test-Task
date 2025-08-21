# Task Manager API

CRUD API для управления задачами, построенный на FastAPI с бд orm и тестами.

## Функциональность

- Создание, чтение, обновление, удаление задач
- Фильтрация задач по статусу
- Пагинация списка задач
- Статистика по задачам
- Автоматическая документация Swagger

## Технические требования
- Backend: FastApi
- Tests: pytest

## Структура 
```
task_manager/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   └── exceptions.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   └── test_crud.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Запуск

### Установка зависимостей
```
pip install -r requirements.txt
```

## Локальный запуск
```
uvicorn app.main:app --reload --port 8000
```

## Docker
```
docker-compose up
```

## Тесты
```
pytest tests/ -v --cov=app
```

### API Endpoints
- GET / - корневая страницы
- POST /api/v1/tasks/ - создание задачи
- GET /api/v1/tasks/{uuid} - получить задачу
- GET /api/v1/tasks/ - список задач
- PUT /api/v1/tasks/{uuid} - обновить задачу
- DELETE /api/v1/tasks/{uuid} - удалить задачу
- GET /api/v1/stats/ - статистика задач

## Документация
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Результат
<img width="640" height="420" alt="image" src="https://github.com/user-attachments/assets/eea67314-4c87-4f5c-b4f4-2e147ae0fb42" />







