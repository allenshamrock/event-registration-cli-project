from sqlalchemy import Column, Integer, String 
from models import Base
from sqlalchemy.orm import relationship




class Organiser(Base):
    __tablename__ = 'organisers'

    id = Column(Integer, primary_key=True)
    organiser_name = Column(String, unique=True, nullable=False)
    organiser_email = Column(String, unique=True, nullable=False)
    events = relationship("Event", back_populates="organiser")

    def __init__(self, organiser_name, organiser_email):
        self.organiser_name = organiser_name
        self.organiser_email = organiser_email

    def __repr__(self):
        return f"Organiser(id={self.id}, name={self.organiser_name}, email={self.organiser_email})"
