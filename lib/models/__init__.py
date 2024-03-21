from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

Base = declarative_base()

db_uri = "event-registration.db"

engine = create_engine(f"sqlite:///{db_uri}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

from .organiser import Organiser
from .event import Event
from .registration import Registration


