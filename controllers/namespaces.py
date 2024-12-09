from flask import Blueprint, request, Response
from services.entry import getNamespaceData, saveEntryRecursive
from services.namespace import getNamespace, createNamespace
from models import Session
from services.language import getLanguageIDByCode

namespaceApp = Blueprint('namespace', __name__)

@namespaceApp.route("/<language>/<namespaceName>", methods=["GET"])
def loadNamespace(language: str, namespaceName: str):
    namespace = getNamespace(namespaceName, language)
    if (namespace is None): 
        return Response("Invalid namespace provided", status=400)
    return getNamespaceData(namespace.id)

@namespaceApp.route("/<language>/<namespaceName>", methods=["POST"])
def saveNamespace(language: str, namespaceName: str):
    languageModel = getLanguageIDByCode(language)
    if (languageModel == None):
        return Response("Invalid Language code provided", status=400)

    namespace = getNamespace(namespaceName, language)
    if (namespace is not None): 
        return Response("Namespaces must be uniques", status=400)

    data = request.get_json()
    if (data is None): return Response("Invalid payload", status=400)

    with Session() as session:
        try:
            namespaceId = createNamespace(namespaceName, languageModel.id, session=session).id
            saveEntryRecursive(obj=data, namespace_id=namespaceId, session=session)
            session.flush()
            session.commit()
            return getNamespaceData(namespaceId)
        except:
            session.rollback()
            return Response("Something went wrong", status=500)