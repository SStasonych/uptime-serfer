from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

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

class SiteResponse(BaseModel):
    id: int
    url: str  # В ответе отдаем как строку для удобства фронтенда
    description: str | None
    is_active: bool
    created_at: datetime

    class ConfigDict:
        from_attributes = True

class SiteCheckLogResponse(BaseModel):
    id: int
    site_id: int
    status_code: int
    response_time: float
    is_available: bool
    checked_at: datetime

    class ConfigDict:
        from_attributes = True
