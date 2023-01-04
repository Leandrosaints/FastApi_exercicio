from typing import List, Generator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.site_model import SiteModel
from fastapi import Depends, HTTPException, status
from core.depes import get_session

from models.site_model import SiteModel
from schemas.site_schema import SiteSchemaBase

async def find_url(id:int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SiteModel).filter(SiteModel.id == id)
        result = await session.execute(query)
        find_id: SiteSchemaBase = result.scalars().unique().one_or_none()
        if find_id:
            return find_id
        else:
               raise HTTPException(detail='id nao encontrado', status_code=status.HTTP_404_NOT_FOUND)


