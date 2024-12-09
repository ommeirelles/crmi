from flask import Blueprint, request, session, Response
from controllers.session import generateSession, HEADER_TOKEN
from services.user import getUserByLogin, saveUser
import bcrypt

userApp = Blueprint('user', __name__)


@userApp.route("/user/auth", methods=["POST"])
def loadUser():
    data = request.get_json()
    login: str | None = data.get("login")
    password = data.get("password")
    if (login == None or password == None): return Response("Invalid payload, missing login or password", status=400)

    user = getUserByLogin(login)
    if (user == None): return Response("Invalid user name or password", status=401)

    if (bcrypt.checkpw(password.encode("utf-8"), user.password) == True):
        session[HEADER_TOKEN] = generateSession(user)
        return Response(status=200)
    else:
        return Response("Invalid user name or password",status=401)

@userApp.route("/user", methods=["POST"])
def createUser():
    data = request.get_json()
    login: str | None = data.get("login")
    password = data.get("password")
    if (login == None or password == None): return Response("Invalid payload, missing login or password", status=400)
    login = login.lower()

    user = getUserByLogin(login)
    if (user != None): return Response("User login already taken", status=400)
    else:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = saveUser(login, hashed_password)
        session[HEADER_TOKEN] = generateSession(user)
        return Response(user.to_JSON(), status=200)