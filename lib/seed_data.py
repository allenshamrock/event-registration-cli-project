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
    organiser1 = Organiser("Unruly Tour", "unruly@example.com")
    organiser2 = Organiser("Thrift Social Nairobi", "thriftsocial@co.ke")
    organiser3 = Organiser("Pop-up", "fashiontrends@gmail.com")
    organiser4 = Organiser("Afrosayari", "afrosayari.co.ke")
    organiser5 = Organiser("solFest" , "solfest@gmail.com")
    organiser6 = Organiser("rongrende", "rongrende@gmail.com")
    organiser7 = Organiser("Buruklyn Fest", "buruklyn@gmail.com")
    organiser8 = Organiser("zozanation", "zozzanation.co.ke")
    session.add_all([organiser1, organiser2, organiser3,
                organiser4, organiser5, organiser6, organiser7, organiser8])

    # Create events
    event1 = Event("Summer Tides", date(2024, 8, 20),
                   "Uhuru Gardens", date(2024, 8, 15))
    event1.organiser = organiser1
    event2 = Event("Jameson Connect", date(2024, 4, 15),
                   "Carnivore", date(2024, 3, 10))
    event2.organiser = organiser2
    event3 = Event("Blankets & Wine", date(2024, 6, 16),
                   "Tatu City", date(2024, 5, 5))
    event3.organiser = organiser3
    event4 = Event("Dancehall Vibes", date(2024, 6, 6),
                   "Kitusuru Manor", date(2024, 5, 12))
    event4.organiser = organiser4
    event5 = Event("Solgeneration Fest", date(2024, 7, 9),
                   "Diani", date(2024, 6, 12))
    event5.organiser = organiser5
    event6 = Event("Rong Experience", date(2024, 4, 20),
                   "The Alchemist", date(2024, 4, 5))
    event6.organiser = organiser6
    event7 = Event("Throwback Thursday ", date(2024, 12, 8),
                   "Nairobi street Kitchen", date(2024, 8, 8))
    event7.organiser = organiser7
    event8 = Event("Zozzanation", date(2024, 7, 7),
                   "Cavali", date(2024, 11, 7))
    event8.organiser = organiser8
    session.add_all([event1, event2, event3, event4,event5,event6,event7,event8])

    # Create registrations
    registration1 = Registration(
        "Allen Shamrock", "allen@gmail.com", "pending",event1.id)
    registration1.event = event1
    registration2 = Registration(
        "Leonard Omusula", "leon@gmail.com", "pending", event2.id)
    registration2.event = event2
    registration3 = Registration(
        "Wiz kid", "wiz@gmail.com", "pending", event3.id)
    registration3.event = event3
    registration4 = Registration(
        "Dave Chappelle", "dave@gmail.com", "pending", event4.id)
    registration4.event = event4
    registration5 = Registration(
        "Brian Kiprono", "kip@gmail.com", "pending", event5.id)
    registration5.event = event5
    registration6 = Registration(
        "Anne Shiko", "shiks@gmail.com", "confirmed", event6.id)
    registration6.event = event6
    registration7 = Registration(
        "Scar mkadianli", "scar@gmail.com", "confirmed", event7.id)
    registration7.event = event7
    registration8 = Registration(
        "Domani hamna", "dosh@gmail.com", "confirmed", event8.id)
    registration8.event = event8


    session.add_all([registration1, registration2,
                     registration3, registration4, registration5, registration6, registration7, registration8])

    # Commit the changes
    session.commit()



seed_data()
