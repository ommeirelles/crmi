from flask import Flask
from sqlalchemy import create_engine
from os import environ
from models import Base, bind_engine
from controllers import namespaceApp, AuthMiddleware, userApp

isDev: bool = environ.get('ENV') == 'development'
secretKey: str = environ.get('SECRET')
app: Flask = Flask(__name__)
engine =create_engine("sqlite:///crmi.db", echo=isDev)


if __name__ == "__main__":
    bind_engine(engine=engine)
    Base.metadata.create_all(engine)
    app.wsgi_app = AuthMiddleware(app.wsgi_app)
    app.secret_key = secretKey.encode("utf-8")
    app.register_blueprint(namespaceApp) 
    app.register_blueprint(userApp)
    app.run(debug=isDev)
