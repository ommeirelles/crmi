from flask import Flask
from sqlalchemy import create_engine
from os import environ
from models import Base, bind_engine
from controllers import namespaceApp, AuthMiddleware, userApp, languageApp

isDev: bool = environ.get('ENV') == 'development'
secretKey: str = environ.get('SECRET')
app: Flask = Flask(__name__)
engine =create_engine("sqlite:///crmi.db", echo=isDev)

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
    app.register_blueprint(namespaceApp) 
    app.register_blueprint(userApp)
    app.register_blueprint(languageApp)
    app.run(debug=isDev)

