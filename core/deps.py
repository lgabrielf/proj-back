#dependências 
from typing import Generator, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from pydantic import BaseModel

class TokenData(BaseModel):
    username: Optional[str] = None

async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session  #abre conexão com o db
    finally:
        await session.close() #depois de fazer uso, eh encerrada a conexão


async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) -> UsuarioModel:
   # caso o usuário não autentique, retorne essa variável a seguir
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Não foi possível autenticar a credencial', 
        headers={"WWWW-Authenticate": "Bearer"}
    )

    try:
    #decodificando token
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.ALGORITHM], 
            options={"verify_aud": False}
        )
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception
        
        token_data: TokenData = TokenData(username=username)
    except JWTError: 
        #se não conseguir decodificar
        raise credential_exception
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == int(token_data.username))
        #id do bd
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if usuario is None:
            raise credential_exception
        return usuario
    