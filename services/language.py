from sqlalchemy import select
from models import Session, LanguageModel

def getLanguageIDByCode(language: str) -> LanguageModel | None:
    return Session().execute(
        select(
            LanguageModel
        ).where(
            LanguageModel.code == language
        )
    ).scalar()