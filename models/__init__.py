from models.namespace import NamespaceModel
from models.entry import EntryModel
from models.language import LanguageModel
from models.base import Base
from models.user import UserModel
from models.session import SessionModel
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()

def bind_engine(engine):
    Base.metadata.bind = engine
    Session.configure(bind=engine)
