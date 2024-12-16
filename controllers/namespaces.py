from pydantic import BaseModel, Field, ConfigDict
from services.entry import getNamespaceData, saveEntryRecursive, emptyEntries
from services.namespace import getNamespace, createNamespace, getNamespaces
from models import Session
from services.language import getLanguageByCode
from flask_openapi3 import  Tag
from flask_openapi3.blueprint import APIBlueprint
from flask import request, Response
from controllers.docs import SaveNamespace200, SaveNamespace400, SaveNamespace500, GetNamespace200, GetNamespace400, GetNamespaces200, CreateNamespace200
import json

namespaceApp = APIBlueprint('namespace', __name__)
namespace_tag = Tag(name="namespace", description="Gerenciar Namespaces")

class LanguagePath(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    language: str = Field(..., description="Codigo da linguage para ser usada")

class CreateNamespaceBody(BaseModel):
    name: str = Field("main", description="Nome do namespace")

@namespaceApp.post("/language/<language>/namespace", tags=[namespace_tag], responses={
    200: CreateNamespace200
})
def createNamespaceResolver(body: CreateNamespaceBody, path: LanguagePath):
    """
    Para criar novos namespaces para a linguagem especifica
    """
    language = path.language
    name: str | None = body.name
    if (request.headers.get("Content-Type") != "application/json"):
        name = request.form.get("name")
    
    if (language == None or name == None): return Response("Invalid payload, missing language or name", status=400)
    
    languageModel = getLanguageByCode(language)
    if (languageModel == None): return Response("Invalid language code", status=400)

    if (getNamespace(name, language) != None): return Response("Namespace already created", status=400)

    namespace = createNamespace(name, languageModel.id)
    return Response(namespace.to_JSON(), status=200)

@namespaceApp.get("/language/<language>/namespaces", tags=[namespace_tag], responses={
    200: GetNamespaces200
})
def getNamespacesResolver(path: LanguagePath):
    """
    Para buscar todos os namespaces disponiveis para uma linguagem especifica
    """
    language = path.language
    return Response(json.dumps({
        "namespaces": [n.as_dict() for n in list(getNamespaces(language))]
    }),status=200)

class NamespacePath(LanguagePath):
    namespaceName: str = Field(..., description="nome do namespace para ser usado")

@namespaceApp.get("/language/<language>/namespace/<namespaceName>", tags=[namespace_tag], responses={
    200: GetNamespace200,
    400: GetNamespace400
})
def loadNamespace(path: NamespacePath):
    """
    Para buscar todos os valores configurados de um namespace
    """
    language = path.language
    namespaceName = path.namespaceName
    namespace = getNamespace(namespaceName, language)
    if (namespace is None): 
        return Response("Invalid namespace provided", status=400)
    return getNamespaceData(namespace.id)

@namespaceApp.post("/language/<language>/namespace/<namespaceName>", tags=[namespace_tag], responses={
    200: SaveNamespace200,
    400: SaveNamespace400,
    500: SaveNamespace500
})
def saveNamespace(path: NamespacePath):
    """
    Para salvar um namespace completo
    """
    language = path.language
    namespaceName = path.namespaceName
    languageModel = getLanguageByCode(language)
    if (languageModel == None):
        return Response("Invalid Language code provided", status=400)

    namespace = getNamespace(namespaceName, language)
    namespaceId = None
    if (namespace is not None): 
        emptyEntries(namespace.id)
        namespaceId = namespace.id
    else:
        namespaceId = createNamespace(namespaceName, languageModel.id, session=session).id


    data = request.get_json()
    if (data is None): return Response("Invalid payload", status=400)

    with Session() as session:
        try:
            saveEntryRecursive(obj=data, namespace_id=namespaceId, session=session)
            session.commit()
            return getNamespaceData(namespaceId)
        except:
            session.rollback()
            return Response("Something went wrong", status=500)