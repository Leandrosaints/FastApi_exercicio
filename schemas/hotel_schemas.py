from typing import Optional
from pydantic import BaseModel

class HotelSchema(BaseModel):
    id:Optional[int] = None
    nome:str
    estrelas:float
    diaria:float
    cidade:str
    site_id:int

    class Config:
        orm_mode = True#

class HotelSchemaUp(HotelSchema):
    nome:Optional[str]
    estrelas:Optional[float]
    diaria:Optional[float]
    cidade:Optional[str]
    site_id:Optional[int]



