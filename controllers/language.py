from flask import Blueprint, Response, request
from services.language import getLanguageByCode, createLanguage, getAllLanguages
import json

languageApp = Blueprint('language', __name__)

@languageApp.route("/language", methods=["POST"])
def createLanguageResolver():
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


@languageApp.route("/languages", methods=["GET"])
def getLanguagesResolver():
    return Response(json.dumps({
        "languages": [lang.as_dict() for lang in list(getAllLanguages())]
    }), status=200)