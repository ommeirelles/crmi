from sqlalchemy import create_engine
from os import environ
from models import Base, bind_engine
from controllers import namespaceApp, AuthMiddleware, userApp, languageApp
from flask_openapi3 import OpenAPI, Info

isDev: bool = environ.get('ENV') == 'development'
secretKey: str = environ.get('SECRET')
app: OpenAPI = OpenAPI(__name__, info=Info(title="MVP Api", version="1.0.0"))
dbName = environ.get("DB_NAME")
engine = create_engine("sqlite:///"+dbName+".db", echo=isDev)

@app.after_request
def applyCORS(response):
    response.headers.add('Accept', '*/*')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    return response


if __name__ == "__main__":
    bind_engine(engine=engine)
    Base.metadata.create_all(engine)
    app.wsgi_app = AuthMiddleware(app.wsgi_app)
    app.secret_key = secretKey.encode("utf-8")
    app.register_api(namespaceApp) 
    app.register_api(userApp)
    app.register_api(languageApp)
    app.run(debug=isDev, port=int(environ.get("PORT")))

