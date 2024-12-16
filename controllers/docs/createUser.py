from pydantic import BaseModel, Field
from typing import Literal

class User(BaseModel):
    token: str = Field(description="Token do usuario de identificacao para autenticacao")
    login: str = Field(..., description="Login do usuario")
    id: int = Field(..., description="id do usuario")

class createUser200(BaseModel):
    code: int = Field(200, description="Codigo de resultado do http")
    data: User = Field(..., description="Lista de resultado dos namepasces existentes por linguagem")

class createUser400(BaseModel):
    code: int = Field(400, description="Codigo de resultado do http")
    data: str = Field(Literal["User login already taken", "Invalid payload, missing login or password"], description="Mensagem explicativa do erro")