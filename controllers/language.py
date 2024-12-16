from services.language import getLanguageByCode, createLanguage, getAllLanguages
import json
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3 import  Tag
from flask import request, Response
from controllers.docs import createLanguage200, createLanguage400, getLanguages200
from pydantic import BaseModel, Field, ConfigDict

languageApp = APIBlueprint('language', __name__)
language_tag = Tag(name="language", description="Gerenciar Linguagens")


class LanguageBody(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    language: str = Field("PT", min_length=2, max_length=5, description="Codigo identificador da linguagem. PT | EN | FR...")
    name: str = Field("Portugues", min_length=1, max_length=10, description="Nome da linguagem")

@languageApp.post("/language", tags=[language_tag], responses={
    200: createLanguage200,
    400: createLanguage400
})
def createLanguageResolver(body: LanguageBody):
    """
        Criar linguagem
    """
    language = body.language
    name = body.name

    if (language == None or len(language) > 5 or name == None): return Response("Invalid! language value or name missing", status=400)

    if (getLanguageByCode(language) != None):  return Response("language value already exists", status=400)

    return Response(createLanguage(language.upper(), name).to_JSON(), status=200)


@languageApp.get("/languages", tags=[language_tag], responses={
    200: getLanguages200
})
def getLanguagesResolver():
    """
        Buscar todas as linguagens
    """
    return Response(json.dumps({
        "languages": [lang.as_dict() for lang in list(getAllLanguages())]
    }), status=200)