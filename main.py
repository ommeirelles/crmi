from flask import Flask
from sqlalchemy import create_engine
from os import environ
from models import Base, bind_engine
from controllers import namespaceApp

isDev: bool = environ['ENV'] == 'development'
app: Flask = Flask(__name__)
engine =create_engine("sqlite:///crmi.db", echo=isDev)


if __name__ == "__main__":
    bind_engine(engine=engine)
    Base.metadata.create_all(engine)
    app.register_blueprint(namespaceApp)
    app.run(debug=isDev)
