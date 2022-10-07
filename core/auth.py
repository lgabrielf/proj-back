from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import checar_senha
from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None

        if not checar_senha(senha, usuario.senha):
            return None

        return usuario

def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}
    rn = timezone('America/Fortaleza')

    #tempo de expiração do token
    expira = datetime.now(tz=rn) + tempo_vida

    payload["type"] = tipo_token

    payload["exp"] = expira
    #iat: gerado em
    payload["iat"] = datetime.now(tz=rn)
    #sub: pode ser id, email, nome, qualquer coisa que identifique o usuário
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str) -> str:
    """
    http://jwt.io
    """

    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), 
        sub=sub
    )