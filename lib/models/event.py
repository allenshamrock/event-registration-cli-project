from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models import Base



class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    event_name = Column(String)
    date = Column(Date)
    location = Column(String)
    registration_deadline = Column(Date)
    organiser_id = Column(Integer, ForeignKey('organisers.id'))
    organiser = relationship("Organiser", back_populates="events")
    registrations = relationship("Registration", back_populates="event")

    def __init__(self, event_name, date, location, registration_deadline):
        self.event_name = event_name
        self.date = date
        self.location = location
        self.registration_deadline = registration_deadline

    def __repr__(self):
        return f"Event(id={self.id}, name={self.event_name}, date={self.date}, location={self.location}, registration_deadline={self.registration_deadline})"
