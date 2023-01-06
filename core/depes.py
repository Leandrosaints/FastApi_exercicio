from typing import Generator, Optional
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session
from jose import jwt, JWTError
from core.configs import settings
from core.auth import Oauth_2_schema
from models.usuario_model import UsuarioModel
from pydantic import BaseModel
from sqlalchemy.future import select

async def get_session() -> Generator:
    session:AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close()


class TokenData(BaseModel):
    username:Optional[str]=None


"""
Na funcao abaixo criamos um filtro no qual buscamos um usuario comparando os dados provido da dependencia(Oauth_2_schema) que nos retornara o token jwt ao entra na rota da dependencia. pegamos aqui esse token decodificamos e extraimos dele (payload.get("sub")) aqual atribuimos ao variavel username, passamos a mesma como argumento para o parametro de mesmo nome da class TokenData, para um melhor tratamento de dados.

Ainda nesta mesma funcao criamos uma query no qual usaremos a conexao com o db para comparamos e retonarmos os dado do usuario caso o id do token decodificado seja igual
"""


async def get_current_user(db:AsyncSession = Depends(get_session), 
token:str=Depends(Oauth_2_schema)) -> UsuarioModel:
    credential_exeception:HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="nao foi possivel autenticar as credenciais", headers={"www-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM], 
            options={"verify_aud":False}
        )

        username:str=payload.get("sub")
        if username is None:
            raise credential_exeception

        token_data:TokenData = TokenData(username=username)

    except JWTError:
        raise credential_exeception

    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username))
        rusult = await session.execute(query)
        usuario:UsuarioModel = rusult.scalars().unique().one_or_none()
    
        if usuario is None:
            raise credential_exeception
        return usuario


