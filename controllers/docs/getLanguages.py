from pydantic import BaseModel, Field
from typing import Literal

class Language(BaseModel):
    code: str = Field(description="Codigo identificador da linguagem. PT | EN | FR...")
    name: str = Field(..., description="Nome da linguagem")
    id: int = Field(..., description="id da linguage")

class getLanguages200(BaseModel):
    code: int = Field(200, description="Codigo de resultado do http")
    data: list[Language] = Field(..., description="Linguagesm cadastradas")