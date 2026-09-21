from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL


# 2. Создаем асинхронный движок (Engine)
# echo=True позволит вам видеть все SQL-запросы в терминале (очень круто для разработки)
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 3. Создаем фабрику асинхронных сессий
async_session_factory = async_sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False, 
    expire_on_commit=False
)

# 4. Создаем современный базовый класс для будущих моделей (таблиц)
class Base(DeclarativeBase):
    pass

# 5. Функция-зависимость (Dependency) для FastAPI Depends
# Она будет выдавать каждому HTTP-запросу свою чистую сессию и закрывать её после ответа
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
