from services.entry import getNamespaceData, saveEntryRecursive, emptyEntries
from services.namespace import getNamespace, createNamespace, getNamespaces
from models import Session
from services.language import getLanguageByCode
from flask_openapi3 import  Tag
from flask_openapi3.blueprint import APIBlueprint
from flask import request, Response
import json

namespaceApp = APIBlueprint('namespace', __name__)
namespace_tag = Tag(name="namespace", description="Manage namespaces")

@namespaceApp.post("/language/<language>/namespace", tags=[namespace_tag])
def createNamespaceResolver():
    """
    Para criar novos namespaces para a linguagem especifica
    """
    language = request.view_args.get("language")
    name: str | None = None
    if (request.headers.get("Content-Type") == "application/json"):
        data = request.get_json()
        name = data.get("name")
    else:
        name = request.form.get("name")
    
    if (language == None or name == None): return Response("Invalid payload, missing language or name", status=400)
    
    languageModel = getLanguageByCode(language)
    if (languageModel == None): return Response("Invalid language code", status=400)

    if (getNamespace(name, language) != None): return Response("Namespace already created", status=400)

    namespace = createNamespace(name, languageModel.id)
    return Response(namespace.to_JSON(), status=200)

@namespaceApp.get("/language/<language>/namespaces", tags=[namespace_tag])
def getNamespacesResolver():
    """
    Para buscar todos os namespaces disponiveis para uma linguagem especifica
    """
    language = request.view_args.get("language")
    return Response(json.dumps({
        "namespaces": [n.as_dict() for n in list(getNamespaces(language))]
    }),status=200)

@namespaceApp.get("/language/<language>/namespace/<namespaceName>", tags=[namespace_tag])
def loadNamespace():
    """
    Para buscar todos os valores configurados de um namespace
    """
    language = request.view_args.get("language")
    namespaceName = request.view_args.get("namespaceName")
    namespace = getNamespace(namespaceName, language)
    if (namespace is None): 
        return Response("Invalid namespace provided", status=400)
    return getNamespaceData(namespace.id)

@namespaceApp.post("/language/<language>/namespace/<namespaceName>", tags=[namespace_tag])
def saveNamespace():
    """
    Para salvar um namespace completo
    """
    namespaceName = request.view_args.get("namespaceName")
    language = request.view_args.get("language")
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