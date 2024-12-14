from sqlalchemy import select
from models import Session, LanguageModel

def getLanguageByCode(language: str) -> LanguageModel | None:
    return Session().execute(
        select(
            LanguageModel
        ).where(
            LanguageModel.code == language.upper()
        )
    ).scalar()

def createLanguage(code: str, name: str) -> LanguageModel:
    lang = LanguageModel()
    lang.code = code
    lang.name = name

    with Session() as session:
        session.add(lang)
        session.commit()
        session.refresh(lang)
        return lang
    
def getAllLanguages():
    return Session().execute(
        select(
            LanguageModel
        )
    ).scalars()