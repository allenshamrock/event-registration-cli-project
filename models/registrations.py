from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship,ForeignKey, declarative_base

Base = declarative_base()

class Registrations(Base):
    __table__ = "registrations"

    id = Column(Integer,primary_key=True)
    atendee_name = Column(String, unique=True)
    atendee_email = Column(String, unique = True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    registration_status = Column(String, nullable=True)

    event = relationship('Event', back_populates='registrations')

