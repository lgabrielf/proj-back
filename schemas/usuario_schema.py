from typing import Optional
from typing import List
from pydantic import BaseModel, EmailStr
from schemas.artigo_schema import ArtigoSchema

# base do schema
class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False

    class Config:
        orm_mode = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

    class Config:
        orm_mode = True

class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]

    class Config:
        orm_mode = True

# para atualizar apenas um parâmetro do usuário
class UsuarioSchemaUp(UsuarioSchemaBase):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    eh_admin: Optional[bool]
    class Config:
        orm_mode = True