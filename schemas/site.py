from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

# 1. Схема для входящих данных (то, что присылает пользователь при добавлении сайта)
class SiteCreate(BaseModel):
    # HttpUrl автоматически проверяет наличие http:// или https:// и валидность домена
    url: HttpUrl = Field(
        ...,
        description="URL-адрес сайта для мониторинга",
        examples=["https://httpbin.org"]
    )
    description: str | None = Field(
        None,
        max_length=500,
        description="Краткое описание сайта (опционально)"
    )

# 2. Схема для вывода информации о сайте пользователю (ответ API)
class SiteResponse(BaseModel):
    id: int
    url: str  # В ответе отдаем как строку для удобства фронтенда
    description: str | None
    is_active: bool
    created_at: datetime

    # В Pydantic v2 этот класс включает автоматическую конвертацию из моделей SQLAlchemy в Pydantic
    class ConfigDict:
        from_attributes = True

# 3. Схема для вывода логов проверок
class SiteCheckLogResponse(BaseModel):
    id: int
    site_id: int
    status_code: int
    response_time: float
    is_available: bool
    checked_at: datetime

    class ConfigDict:
        from_attributes = True
