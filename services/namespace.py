from sqlalchemy import select
from models import Session, NamespaceModel
from services.language import getLanguageIDByCode

def getNamespace(name: str, language: str):
    languageModel = getLanguageIDByCode(language)
    if (languageModel is None): return None;

    return Session().execute(
        select(
            NamespaceModel
        ).where(
            NamespaceModel.name == name and NamespaceModel.language_id == languageModel.id
        )
    ).scalar()


def createNamespace(name: str, language_id: int, session = Session()) -> NamespaceModel:
    namespace = NamespaceModel()
    namespace.name = name
    namespace.language_id = language_id

    session.add(namespace)
    session.flush()
    session.refresh(namespace)
    return namespace