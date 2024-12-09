from models import UserModel
from services.session import getUserBySession
import bcrypt

HEADER_TOKEN = "Authorization"
INVALID_TOKEN = Exception("Token not valid for the user")

def generateSession(user: UserModel):
    return bcrypt.hashpw(str(user.id).encode("utf-8"), bcrypt.gensalt())

def checkSession(session: str, user: UserModel) -> bool:
    return bcrypt.checkpw(str(user.id).encode("utf-8"), session)

def getSessionByToken(token: str) -> UserModel | None:
    user = getUserBySession(token)

    if (not checkSession(token, user)):
        raise INVALID_TOKEN
    
    return user
