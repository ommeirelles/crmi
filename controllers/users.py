from controllers.session import generateSession
from services.user import getUserByLogin, saveUser
from services.session import saveSession
from flask_openapi3 import  Tag
from flask_openapi3.blueprint import APIBlueprint
from flask import request, Response
from controllers.docs import createUser200, createUser400,loadUser200, loadUser400
from pydantic import BaseModel, Field, ConfigDict
import bcrypt
import json

userApp = APIBlueprint('user', __name__)
user_tag = Tag(name="user", description="Gerenciar usuarios")

class UserBody(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    login: str = Field("ommeirelles@gmail.com", description="Login do usuario")
    password: str = Field(..., min_length=6, max_length=10, description="Senha do usuario")

@userApp.post("/user/auth", tags=[user_tag],responses={
    200: loadUser200,
    400: loadUser400
})
def loadUser(form: UserBody):
    """
        Authentica usuario
    """
    login = form.login
    password = form.password

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

@userApp.post("/user", tags=[user_tag], responses={
    200: createUser200,
    400: createUser400
})
def createUser(form: UserBody):
    """
        Cria e authentica usuario
    """
    login = form.login
    password = form.password

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