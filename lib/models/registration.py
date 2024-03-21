from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models import Base






class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, primary_key=True)
    attendee_name = Column(String)
    attendee_email = Column(String)
    registration_status = Column(String)
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", back_populates="registrations")

    def __init__(self, attendee_name, attendee_email, registration_status):
        self.attendee_name = attendee_name
        self.attendee_email = attendee_email
        self.registration_status = registration_status

    def __repr__(self):
        return f"Registration(id={self.id}, attendee_name={self.attendee_name}, attendee_email={self.attendee_email}, registration_status={self.registration_status})"
