from fastapi import APIRouter
from api.v1.endpoints import hotel_route
from api.v1.endpoints import site_route
#prefix: adicione o prefixo em cada decorador fornecido pelo fastapi naquela página específica
api_router = APIRouter()
api_router.include_router(hotel_route.router, prefix='/hoteis', tags=['hotel'])
api_router.include_router(site_route.router, prefix='/sites', tags=['site'])

