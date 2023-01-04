from fastapi import APIRouter, status, HTTPException, Depends, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.depes import get_session 
from schemas.usuario_schema import UsuarioSchemaBase,UsuarioSchemaUp, UsuarioSchemaCreate
from models.usuario_model import UsuarioModel
from core.security import gerar_hash_senha


router = APIRouter()


#post usuario
@router.post('/register', response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def RegisterUser(usuario:UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario:UsuarioModel = UsuarioModel(nome=usuario.nome,sobrenome=usuario.sobrenome, email=usuario.email, senha=gerar_hash_senha(usuario.senha), admin=usuario.admin)

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except:
            raise HTTPException(detail='nao foi possivel cadastrar o usuario', status_code=status.HTTP_406_NOT_ACCEPTABLE)
@router.get('/', response_model=List[UsuarioSchemaBase], status_code=status.HTTP_200_OK)
async def get_usuarios(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioModel] = result.scalars().unique().all()
        
        return usuarios


@router.get('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id:int, db:AsyncSession =Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuarios:UsuarioModel = result.scalars().unique().one_or_none()

        if usuarios:
            return usuarios
        else:
            raise HTTPException(detail=f'nao foi encontrar um usuario com o id {usuario_id}.', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def put_usuario(usuario_id:int, usuario:UsuarioSchemaUp, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)

        usuario_up:UsuarioSchemaBase = result.scalars().unique().one_or_none()
        
       
        
        if usuario_up:
            if usuario_up.nome:
                usuario_up.nome = usuario.nome
            if usuario_up.sobrenome:
                usuario_up.sobrenome = usuario.sobrenome
            if usuario_up.email:
                usuario_up.email = usuario.email
            if usuario_up.senha:
                usuario_up.senha = usuario.senha
            if usuario_up.admin:
                usuario_up.admin = usuario.admin

            await session.commit()
            return usuario_up
        else:
            raise HTTPException(detail='nao foi posivel atualizar os campos desejados',  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



@router.delete('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def delete_usuario(usuario_id:int, db:AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)

        del_usuario:UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if del_usuario:
            await session.delete(del_usuario)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail=f'nao foi possivel excluir o usuario de id {usuario_id}.', status_code=status.HTTP_404_NOT_FOUND)

