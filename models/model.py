from core.configs import settings
from sqlalchemy import Column, Integer, String


class LinusModel(settings.DBBaseModel):
    __tablename__ = 'Projetos' 
    
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    empresa: str = Column(String(100))
    cnpj: str = Column(String(100))
    obs: str = Column(String(100))
