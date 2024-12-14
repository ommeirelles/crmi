from controllers.session import generateSession
from services.user import getUserByLogin, saveUser
from services.session import saveSession
from flask_openapi3 import  Tag
from flask_openapi3.blueprint import APIBlueprint
from flask import request, Response

import bcrypt
import json

userApp = APIBlueprint('user', __name__)
user_tag = Tag(name="user", description="Gerenciar usuarios")

@userApp.post("/user/auth", tags=[user_tag])
def loadUser():
    """
        Authentica usuario
    """
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

@userApp.post("/user", tags=[user_tag])
def createUser():
    """
        Cria e authentica usuario
    """
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