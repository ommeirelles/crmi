from models import EntryModel, Session, UserModel
from sqlalchemy import select
from sqlalchemy.orm import aliased
import bcrypt

def getUserByLogin(login: str) -> UserModel | None:
    return Session().execute(select(UserModel).where(UserModel.login == login)).scalar()

def saveUser(login:str, pwd: str):
    user = UserModel()
    user.login = login
    user.password = pwd

    with Session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    
    return user
