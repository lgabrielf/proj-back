from typing import Optional
from pydantic import BaseModel as SCBaseModel #para diferenciar do BM do sqlalchemy

class LinusSchema(SCBaseModel):
    id: Optional[int]
    nome: str
    empresa: str
    cnpj: str
    obs: str

    class Config:
        orm_mode = True