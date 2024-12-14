from sqlalchemy import select
from models import Session, NamespaceModel
from services.language import getLanguageByCode

def getNamespace(name: str, language: str):
    languageModel = getLanguageByCode(language)
    if (languageModel is None): return None;

    return Session().execute(
        select(
            NamespaceModel
        ).where(
            NamespaceModel.name == name and NamespaceModel.language_id == languageModel.id
        )
    ).scalar()


def createNamespace(name: str, language_id: int) -> NamespaceModel:
    namespace = NamespaceModel()
    namespace.name = name
    namespace.language_id = language_id

    with Session() as session:
        session.add(namespace)
        session.commit()
        session.refresh(namespace)
        return namespace

def getNamespaces(langCode: str):
    language = getLanguageByCode(langCode)
    return Session().execute(select(NamespaceModel).where(NamespaceModel.language_id == language.id)).scalars()