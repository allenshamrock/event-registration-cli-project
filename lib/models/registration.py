from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, primary_key=True ,nullable=False)
    attendee_name = Column(String ,unique=True, nullable=False)
    attendee_email = Column(String , unique=True, nullable=False)
    registration_status = Column(String)
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", back_populates="registrations")

    def __init__(self, attendee_name, attendee_email, registration_status, event_id):
        self.attendee_name = attendee_name
        self.attendee_email = attendee_email
        self.registration_status = registration_status
        self.event_id = event_id

    def __repr__(self):
        return f"Registration(id={self.id}, attendee_name={self.attendee_name}, attendee_email={self.attendee_email}, registration_status={self.registration_status})"

 
