from models import Session, SessionModel, UserModel
from sqlalchemy import select, update

def getUserBySession(token: str) -> UserModel | None:
    with Session() as session:
        userSession = session.execute(select(SessionModel).where(SessionModel.token == token)).scalar()

        if (userSession == None): return None

        return session.execute(select(UserModel).where(UserModel.id == userSession.user_id)).scalar()

def saveSession(token: str, user_id: int) -> SessionModel | None:
    newSession = SessionModel()
    newSession.token = token
    newSession.user_id = user_id

    with Session() as session:
        session.add(newSession)
        session.commit()
        session.refresh(newSession)

    return newSession

def updateSession(oldToken: str, newToken: str) -> SessionModel | None:

    with Session() as session:
        session.execute(update(SessionModel).where(SessionModel.token == oldToken).values(token=newToken)).scalar()
        session.commit()
        
    return getSession(newToken)