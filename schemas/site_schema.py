from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from schemas.hotel_schemas import HotelSchema

class SiteSchemaBase(BaseModel):
    id:Optional[int] = None
    url:HttpUrl
   

    class Config:
        orm_mode = True

class SiteSchemaAll(SiteSchemaBase):
    id:Optional[int]
    url:HttpUrl
    hoteis:Optional[List[HotelSchema]]

class SiteSchemaUrl(SiteSchemaBase):
    url:HttpUrl 