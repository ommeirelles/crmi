from services.language import getLanguageByCode, createLanguage, getAllLanguages
from models.language import LanguageModel
import json
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3 import  Tag
from flask import request, Response

languageApp = APIBlueprint('language', __name__)
language_tag = Tag(name="language", description="Gerenciar Linguagens")

@languageApp.post("/language", tags=[language_tag])
def createLanguageResolver():
    """
        Criar linguagem
    """
    language: str | None = None
    name: str | None = None
    if (request.headers.get("Content-Type") == "application/json"):
        data = request.get_json()
        name = data.get("name")
        language = data.get("language")
    else:
        name = request.form.get("name")
        language = request.form.get("language")

    if (language == None or len(language) > 5 or name == None): return Response("Invalid language value or missing", status=400)

    if (getLanguageByCode(language) != None):  return Response("language value already exists", status=400)

    return Response(createLanguage(language.upper(), name).to_JSON(), status=200)


@languageApp.get("/languages", tags=[language_tag])
def getLanguagesResolver():
    """
        Buscar todas as linguagens
    """
    return Response(json.dumps({
        "languages": [lang.as_dict() for lang in list(getAllLanguages())]
    }), status=200)