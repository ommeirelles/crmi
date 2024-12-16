from pydantic import BaseModel, Field

class Namespace(BaseModel):
    language_id: int = Field(..., description="Codigo de identificacao da linguagem em que o namespace esta configurada")
    name: str = Field(..., description="Nome do namespace")
    id: int = Field(..., description="id do namespace")

class CreateNamespace200(BaseModel):
    code: int = Field(200, description="Codigo de resultado do http")
    data: Namespace = Field(..., description="Lista de resultado dos namepasces existentes por linguagem")

class CreateNamespace400(BaseModel):
    code: int = Field(400, description="Codigo de resultado do http")
    data: Namespace = Field(..., description="Lista de resultado dos namepasces existentes por linguagem")