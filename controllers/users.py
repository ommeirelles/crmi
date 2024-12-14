from flask import Blueprint, request, Response
from controllers.session import generateSession
from services.user import getUserByLogin, saveUser
from services.session import saveSession
import bcrypt
import json

userApp = Blueprint('user', __name__)

@userApp.route("/user/auth", methods=["POST"])
def loadUser():
    login: str | None = None;
    password: str | None = None;
    if (request.headers.get("Content-Type") == "application/json"):
        data = request.get_json()
        login = data.get("login")
        password = data.get("password")
    else:
        login = request.form.get("login")
        password = request.form.get("password")
    if (login == None or password == None): return Response("Invalid payload, missing login or password", status=400)

    user = getUserByLogin(login)
    if (user == None): return Response("Invalid user name or password", status=401)

    if (bcrypt.checkpw(password.encode("utf-8"), user.password) == True):
        userWIthTokenDict = user.as_dict()
        userWIthTokenDict["token"] = generateSession(user).decode("utf-8")

        saveSession(userWIthTokenDict["token"], user.id)
        return Response(json.dumps(userWIthTokenDict), status=200)
    else:
        return Response("Invalid user name or password",status=401)

@userApp.route("/user", methods=["POST"])
def createUser():
    login: str | None = None;
    password: str | None = None;
    if (request.headers.get("Content-Type") == "application/json"):
        data = request.get_json()
        login = data.get("login")
        password = data.get("password")
    else:
        login = request.form.get("login")
        password = request.form.get("password")

    if (login == None or password == None): return Response("Invalid payload, missing login or password", status=400)
    login = login.lower()

    user = getUserByLogin(login)
    if (user != None): return Response("User login already taken", status=400)
    else:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = saveUser(login, hashed_password)
        userWIthTokenDict = user.as_dict()
        userWIthTokenDict["token"] = generateSession(user).decode("utf-8")

        saveSession(userWIthTokenDict["token"], user.id)
        return Response(json.dumps(userWIthTokenDict), status=200)