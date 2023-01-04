from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.future import select
from models.hotel_model import HotelModel
from schemas.hotel_schemas import HotelSchema, HotelSchemaUp
from models.site_model import SiteModel
from schemas.site_schema import SiteSchemaBase
from core.depes import get_session
from core.filter import find_url
  
router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=HotelSchema)
async def post_hotel(hotel:HotelSchema, db:AsyncSession=Depends(get_session)):

    novo_hotel:HotelModel = HotelModel(nome=hotel.nome, estrelas=hotel.estrelas, diaria=hotel.diaria, cidade=hotel.cidade,
    site_id=hotel.site_id)
    async with db as session:
        query = select(SiteModel).filter(SiteModel.id == hotel.site_id)
        result = await session.execute(query)
        find_id: SiteSchemaBase = result.scalars().unique().one_or_none() 
        if find_id:
            db.add(novo_hotel)
            await db.commit()
            return novo_hotel
        else:    
               raise HTTPException(detail='id nao encontrado', status_code=status.HTTP_404_NOT_FOUND)
@router.get('/', response_model=list[HotelSchema], status_code=status.HTTP_200_OK)
async def get_hoteis(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(HotelModel)
        result = await session.execute(query)
        hoteis: List[HotelModel] = result.scalars().unique().all()

        return hoteis

#buscar hotel especifico
@router.get('/{hotel_id}', response_model=HotelSchema, status_code=status.HTTP_200_OK)
async def get_hoteis(hotel_id:int, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(HotelModel).filter(HotelModel.id == hotel_id)
        result = await session.execute(query)
        hotel: HotelModel = result.scalars().unique().one_or_none()
        if hotel:
            return hotel
        else:
            raise HTTPException(detail=f'nao foi encontrado hotel com o {hotel_id}', status_code=status.HTTP_404_NOT_FOUND)




#atualizar hotel
@router.put('/{hotel_id}', response_model=HotelSchemaUp, status_code=status.HTTP_202_ACCEPTED)
async def put_hotel(hotel_id:int, hotel:HotelSchemaUp, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query  = select(HotelModel).filter(HotelModel.id == hotel_id)
        result = await session.execute(query)
        hotel_up: HotelModel = result.scalars().unique().one_or_none()

        if hotel_up:
            hotel_up.nome = hotel.nome
            hotel_up.estrelas = hotel.estrelas
            hotel_up.diaria =  hotel.diaria
            hotel_up.cidade = hotel.cidade
        
            await session.commit()
            return hotel_up
        else:
            raise HTTPException(detail='nao foi possivel fazer as alteracoes', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{hotel_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(hotel_id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(HotelModel).filter(HotelModel.id == hotel_id)
        result = await session.execute(query)

        del_hotel:HotelSchema= result.scalars().unique().one_or_none()
        if del_hotel:
            await session.delete(del_hotel)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail=f'nao foi possivel encontrar o hotel de id {hotel_id}', status_code=status.HTTP_404_NOT_FOUND)
   
      
  


