from pydantic import BaseModel, Field
from typing import Literal

class GetNamespace200(BaseModel):
    code: int = Field(200, description="Codigo de resultado do http")
    data: dict = Field(..., description="Objeto json com chave valor generico")


class GetNamespace400(BaseModel):
    code: int = Field(400, description="Codigo de resultado do http")
    data: str = Field("Invalid namespace provided", description="Mensagem explicativa do erro")