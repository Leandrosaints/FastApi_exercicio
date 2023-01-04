from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.site_model import SiteModel
from models.hotel_model import HotelModel
from schemas.site_schema import SiteSchemaBase, SiteSchemaAll, SiteSchemaUrl
from core.depes import get_session
from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import List

router = APIRouter()
#inserir os dados
@router.post('/', response_model=SiteSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_site(site:SiteSchemaBase, db:AsyncSession = Depends(get_session)):
    novo_site:SiteModel = SiteModel(url=site.url)
    async with db as session:
        try:
            session.add(novo_site)
            await session.commit()
            return novo_site
        except:
            raise HTTPException(detail='nao foi possivel cadastrar o site', status_code=status.HTTP_406_NOT_ACCEPTABLE)

#buscar todos os sites
@router.get('/', response_model=List[SiteSchemaAll])
async def get_sites(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SiteModel)
        result = await session.execute(query)
        sites:List[SiteModel] = result.scalars().unique().all()
        return sites


#buscar um site especifico
@router.get('/{site_id}', response_model=SiteSchemaAll, status_code=status.HTTP_200_OK)
async def get_site(site_id:int, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(SiteModel).filter(SiteModel.id == site_id)
        result = await session.execute(query)
        site: SiteModel = result.scalars().unique().one_or_none()

        if site:
            return site
        else:
            raise HTTPException(detail='site nao encontrado', status_code=status.HTTP_404_NOT_FOUND)


#atualizar os dados
@router.put('/{site_id}', response_model=SiteSchemaUrl, status_code=status.HTTP_202_ACCEPTED)
async def put_site(site_id:str, url_nova:SiteSchemaUrl, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(SiteModel).filter(SiteModel.id == site_id)
        result = await session.execute(query)
        nova_url: SiteModel = result.scalars().unique().one_or_none()

        if nova_url:
            nova_url.url = url_nova.url
            await session.commit()
            return nova_url

        else:
            raise HTTPException(detail='site id nao encontrado patra atualizar a url do mesmo', status_code=status.HTTP_404_NOT_FOUND)


#deletar os dados
@router.delete('/{site_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_site(site_id:int, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(SiteModel).filter(SiteModel.id == site_id)
        result = await session.execute(query)
        del_site: SiteSchemaAll= result.scalars().unique().one_or_none()

        if del_site:
            await session.delete(del_site)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(detail='site nao encontrado', status_code=status.HTTP_404_NOT_FOUND)
