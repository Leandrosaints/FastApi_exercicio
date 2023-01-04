from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioSchemaBase(BaseModel):
    id:Optional[int]= None
    nome:str
    sobrenome:str
    email:EmailStr
    admin:bool

    class Config:
        orm_mode = True

class UsuarioSchemaUp(UsuarioSchemaBase):
    nome:Optional[str]
    sobrenome:Optional[str]
    email:Optional[EmailStr]
    senha:Optional[str]
    admin:Optional[bool]

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha:str

