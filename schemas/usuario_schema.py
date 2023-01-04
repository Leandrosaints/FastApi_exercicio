from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioSchema(BaseModel):
    id:Optional[int]= None
    nome:str
    sobrenome:str
    email:EmailStr
    class Config:
        orm_mode = True

class UsuarioSchemaUp(UsuarioSchema):
    nome:Optional[str]
    sobrenome:Optional[str]
    email:Optional[EmailStr]
    senha:Optional[str]
    

