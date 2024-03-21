#!/usr/bin/env python3
from datetime import date
from models import Organiser, Event, Registration, Base,engine,session

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def seed_data():
    # engine = create_engine("sqlite:///event-registration.db")
    # Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # Create organiser
    organiser = Organiser("Unruly Tour", "unruly@example.com")
    session.add(organiser)

    # Create events
    event1 = Event("Summer Tides", date(2024, 8, 20),
                   "Uhuru Gardens", date(2024, 8, 15))
    event1.organiser = organiser
    event2 = Event("Jameson Connect", date(2024, 4, 15),
                   "Carnivore", date(2024, 3, 10))
    event2.organiser = organiser
    event3 = Event("Blankets & Wine", date(2024, 6, 16),
                   "Tatu City", date(2024, 5, 5))
    event3.organiser = organiser
    event4 = Event("Dancehall Vibes", date(2024, 6, 6),
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

    # Commit the changes
    session.commit()



seed_data()
