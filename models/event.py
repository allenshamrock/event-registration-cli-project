from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, ForeignKey, declarative_base

Base = declarative_base()

class Event(Base):
    __table__ = "events"
    id = Column(Integer,primary_key=True)
    event_name = Column(String, unique=True)
    date = Column(Integer, unique=True)
    location = Column(String, unique=True)
    registration_deadline = Column(Integer,unique=True)
    organizer_id = Column(Integer,ForeignKey("organizers.id") ,nullable=False)


    organizer = relationship('Organizer', back_populates='events')
    registrations = relationship('Registration', back_populates='event')