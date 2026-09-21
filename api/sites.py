from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.site import Site, SiteCheckLog
from schemas.site import SiteCreate, SiteResponse

router = APIRouter(prefix="/sites", tags=["Sites"])

# ЭНДПОИНТ 1: Добавление нового сайта в таблицу 'sites'
@router.post("/", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
async def create_site(site_data: SiteCreate, db: AsyncSession = Depends(get_db)):
    # 1. Проверяем, нет ли уже такого сайта в базе
    query = select(Site).where(Site.url == str(site_data.url))
    result = await db.execute(query)
    existing_site = result.scalar_one_or_none()

    if existing_site:
        raise HTTPException(
            status_code=400,
            detail="Этот сайт уже добавлен в систему мониторинга"
        )

    # 2. Создаем объект модели SQLAlchemy из Pydantic-данных
    new_site = Site(
        url=str(site_data.url),
        description=site_data.description
    )

    # 3. Добавляем объект в сессию (подготовка к записи)
    db.add(new_site)

    # 4. Фиксируем изменения в PostgreSQL (физическая запись строки)
    await db.commit()

    # 5. Обновляем объект, чтобы получить его ID, сгенерированный базой
    await db.refresh(new_site)

    return new_site


# ЭНДПОИНТ 2: Получение списка всех сайтов
@router.get("/", response_model=list[SiteResponse])
async def get_all_sites(db: AsyncSession = Depends(get_db)):
    query = select(Site).order_by(Site.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()
