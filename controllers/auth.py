from flask_openapi3 import OpenAPI
from werkzeug.wrappers import Request, Response
from controllers.session import getSessionByToken, INVALID_TOKEN, HEADER_TOKEN
import re

UNAUTHORIZED_RES = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
OPEN_ROUTES = ("/user", "/user/auth")
class AuthMiddleware():
    def __init__(self, app: OpenAPI):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        if (re.match('^/openapi/?.*', request.path) or request.path in OPEN_ROUTES or request.method == "OPTIONS"): return self.app(environ, start_response)

        try:
            token = request.headers.get(HEADER_TOKEN)
            if (token == None): raise INVALID_TOKEN
            
            user = getSessionByToken(token)
            if (user == None): raise INVALID_TOKEN
            
            environ['user'] = user.as_dict()
            return self.app(environ, start_response)
        except INVALID_TOKEN:
            return UNAUTHORIZED_RES(environ, start_response)

