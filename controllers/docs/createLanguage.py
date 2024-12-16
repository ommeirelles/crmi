from pydantic import BaseModel, Field
from typing import Literal

class Language(BaseModel):
    code: str = Field(description="Codigo identificador da linguagem. PT | EN | FR...")
    name: str = Field(..., description="Nome da linguagem")
    id: int = Field(..., description="id da linguage")

class createLanguage200(BaseModel):
    code: int = Field(200, description="Codigo de resultado do http")
    data: Language = Field(..., description="Object linguagem criada")

class createLanguage400(BaseModel):
    code: int = Field(400, description="Codigo de resultado do http")
    data: str = Field(Literal["language value already exists", "Invalid! language value or name missing"], description="Mensagem explicativa do erro")