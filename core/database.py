# pegar informações do banco de dados
from typing import AsyncIterable
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from core.configs import settings  # chamando instancia do core

engine: AsyncEngine = create_async_engine(settings.DB_URL)
# utilizada para criação das tabelas

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)  # abrir e fechar a conexão com o db
