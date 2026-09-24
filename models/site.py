from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Site(Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True) # Мониторить ли сайт сейчас
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Связь с логами проверок (один сайт имеет много логов)
    # lazy="selectin" — это современный асинхронный паттерн SQLAlchemy 2.0
    checks: Mapped[list["SiteCheckLog"]] = relationship(
        "SiteCheckLog", back_populates="site", cascade="all, delete-orphan", lazy="selectin"
    )

# Таблица логов (результатов) проверок Celery-воркером
class SiteCheckLog(Base):
    __tablename__ = "site_check_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    site_id: Mapped[int] = mapped_column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), nullable=False)
    
    status_code: Mapped[int] = mapped_column(Integer, nullable=False)
    response_time: Mapped[float] = mapped_column(Float, nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Обратная связь с сайтом
    site: Mapped["Site"] = relationship("Site", back_populates="checks")
