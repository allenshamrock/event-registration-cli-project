# models/event.py

from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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

    @classmethod
    def seed_data(cls, session):
        organiser = Organiser("Unruly Tour", "unruly@example.com")
        session.add(organiser)

        event1 = cls("Summer Tides", date(2024, 8, 20),
                     "Uhuru Gardens", date(2024, 8, 15))
        event1.organiser = organiser
        event2 = cls("Jameson Connect", date(2024, 4, 15),
                     "Carnivore", date(2024, 3, 10))
        event2.organiser = organiser
        event3 = cls("Blankets & Wine", date(2024, 6, 16),
                     "Tatu City", date(2024, 5, 5))
        event3.organiser = organiser
        event4 = cls("Dancehall Vibes", date(2024, 6, 6),
                     "Kitusuru Manor", date(2024, 5, 12))
        event4.organiser = organiser

        session.add_all([event1, event2, event3, event4])

        # Create registrations
        registration1 = Registration(
            "Allen Shamrock", "allen@gmail.com", "pending")
        registration1.event = event1
        registration2 = Registration(
            "Leonard Omusula", "leon@gmail.com", "pending")
        registration2.event = event2
        registration3 = Registration("Wiz kid", "wiz@gmail.com", "pending")
        registration3.event = event3
        registration4 = Registration(
            "Dave Chappelle", "dave@gmail.com", "pending")
        registration4.event = event4

        session.add_all([registration1, registration2,
                        registration3, registration4])

# models/registration.py


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

# models/organiser.py


class Organiser(Base):
    __tablename__ = 'organisers'

    id = Column(Integer, primary_key=True)
    organiser_name = Column(String)
    organiser_email = Column(String)
    events = relationship("Event", back_populates="organiser")

    def __init__(self, organiser_name, organiser_email):
        self.organiser_name = organiser_name
        self.organiser_email = organiser_email

    def __repr__(self):
        return f"Organiser(id={self.id}, name={self.organiser_name}, email={self.organiser_email})"


# Creating engine and session
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from models.event import Event
    from models.organiser import Organiser
    from models.registration import Registration

    engine = create_engine("sqlite:///event-registration.db", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        Event.seed_data(session)
        session.commit()
        print("Data persisted successfully.")

    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")

    finally:
        session.close()
