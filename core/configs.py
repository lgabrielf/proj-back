# configurações gerais  de todo o projeto
from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

#criando as classes
class Settings(BaseSettings):
    #configurações gerais usadas na aplicação
    API_V1_STR: str = '/api/v1'  #versão da api
    DB_URL: str = "mysql+asyncmy://root:@localhost:3306/linuslog"
    DBBaseModel = declarative_base() 
    #os models irão erdar as configs do alchemy
    
    JWT_SECRET: str = 'JZDsEmQ0XsTDH8MCMXQzvsnlNrQanGV5QM4z6j6dpFk' 
    #padrão token (JSON), cada API vai utilizar uma criptografia
   

    #algoritmo utilizado para gerar o token do JWT_SECRET
    
    """
    import secrets 
    token: str = secrets.token_urlsafe(32)
    """
    
    ALGORITHM: str = 'HS256'
    #token válido por 1 semana (em minutos)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    

    class Config:
        case_sensitive = True

settings: Settings = Settings() #instanciando objeto, para ser importado de qualquer lugar
