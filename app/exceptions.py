from fastapi import HTTPException, status

# создание своих классов ошибок, наследуемся от Httpexception
class TaskNotFoundError(HTTPException):
    def __init__(self, task_uuid: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с UUID {task_uuid} не найдена"
        )


class TaskValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )