from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.model import LinusModel
from schemas.model_schema import LinusSchema
from core.deps import get_session

router = APIRouter()

#criar recursos

#quando postar na raiz do endpoint
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=LinusSchema)
#pydantic vai pegar o LinusSchema, converter para JSON e devolver para a API
async def post_linus(linus: LinusSchema, db: AsyncSession = Depends(get_session)):
    novo_projeto = LinusModel(nome=linus.nome, empresa=linus.empresa, cnpj=linus.cnpj, obs=linus.obs)
    
    db.add(novo_projeto)
    await db.commit()

    return novo_projeto


#trazer recursos

#GET projeto
@router.get('/', response_model=List[LinusSchema])
async def get_projetos(db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(LinusModel)
        result = await session.execute(query)
        projetos: List[LinusModel] = result.scalars().all()

        return projetos

#trazer recurso específico

#GET projeto
@router.get('/{projeto_id}', response_model=LinusSchema, status_code=status.HTTP_200_OK)
async def get_projeto(projeto_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(LinusModel).filter(LinusModel.id == projeto_id)
        result = await session.execute(query)
        projeto = result.scalar_one_or_none()
        
        if projeto:
            return projeto
        else:
            raise HTTPException(detail='Projeto não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

#atualizar recurso

#PUT projeto
@router.put('/{projeto_id}', response_model=LinusSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_projeto(projeto_id: int, projeto: LinusSchema, db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(LinusModel).filter(LinusModel.id == projeto_id)
        result = await session.execute(query)
        projeto_up = result.scalar_one_or_none()
        
        if projeto_up:
            projeto_up.nome = projeto.nome
            projeto_up.empresa = projeto.empresa
            projeto_up.cnpj = projeto.cnpj
            projeto_up.obs = projeto.obs
            await session.commit()

            return projeto_up
        else:
            raise HTTPException(detail='Projeto não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

#deletar recurso

#DELETE projeto
@router.delete('/{projeto_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_projeto(projeto_id: int, db: AsyncSession=Depends(get_session)):
    async with db as session:
        query = select(LinusModel).filter(LinusModel.id == projeto_id)
        result = await session.execute(query)
        projeto_del = result.scalar_one_or_none()
        
        if projeto_del:
            await session.delete(projeto_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Projeto não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

