from pydantic import BaseModel,Field
from typing import Literal

class SaveNamespace200(BaseModel):
    code: int = Field(200, description="Codigo de resultado do http")
    data: dict = Field(..., description="Objeto json com chave valor generico")


class SaveNamespace400(BaseModel):
    code: int = Field(400, description="Codigo de resultado do http")
    data: str = Field(Literal["Invalid Language code provided", "Invalid payload"], description="Mensagem explicativa do erro")

class SaveNamespace500(BaseModel):
    code: int = Field(500, description="Codigo de resultado do http")
    data: str = Field(Literal["Something went wrong"], description="Mensagem explicativa do erro")