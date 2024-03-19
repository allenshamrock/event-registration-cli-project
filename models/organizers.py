from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Organisers(Base):
    __table__ = "orgainisers"

    id = Column(Integer, primary_key=True)
    organiser_name = Column(String, unique=True)
    organiser_email = Column(String,unique=True)

    events = relationship('Event', back_populates='organizer')

