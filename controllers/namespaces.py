from flask import Blueprint, request, Response
from services.entry import getNamespaceData, saveEntryRecursive, emptyEntries
from services.namespace import getNamespace, createNamespace, getNamespaces
from models import Session
from services.language import getLanguageByCode
import json

namespaceApp = Blueprint('namespace', __name__)

@namespaceApp.route("/language/<language>/namespace", methods=["POST"])
def createNamespaceResolver(language):
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

@namespaceApp.route("/language/<language>/namespaces", methods=["GET"])
def getNamespacesResolver(language):
    return Response(json.dumps({
        "namespaces": [n.as_dict() for n in list(getNamespaces(language))]
    }),status=200)


@namespaceApp.route("/language/<language>/namespace/<namespaceName>", methods=["GET"])
def loadNamespace(language: str, namespaceName: str):
    namespace = getNamespace(namespaceName, language)
    if (namespace is None): 
        return Response("Invalid namespace provided", status=400)
    return getNamespaceData(namespace.id)

@namespaceApp.route("/language/<language>/namespace/<namespaceName>", methods=["POST"])
def saveNamespace(language: str, namespaceName: str):
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