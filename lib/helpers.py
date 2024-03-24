from models import Event, Registration, session
from models import Event,session,Registration,Organiser
from datetime import datetime

def get_required_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip():  
            return user_input
        else:
            print("This field is required. Please provide a value.")

def register_attendee():
    print("Please provide the following information to register for an event:")
    attendee_name = get_required_input("Attendee Name: ")
    attendee_email = get_required_input("Attendee Email: ")
    print("Available Events:")
    events = session.query(Event).all()
    for event in events:
        print(f"{event.id}: {event.event_name} - {event.date}")

    while True:
        try:
            event_id = int(
                input("Enter the ID of the event you want to register for: "))
            event = session.query(Event).filter(Event.id == event_id).first()
            if event:
                registration = Registration(
                    attendee_name=attendee_name,
                    attendee_email=attendee_email,
                    registration_status="confirmed",
                    event_id=event_id
                )
                session.add(registration)
                session.commit()
                print(f"{registration.attendee_name} your registration for {registration.event.event_name} was  successful!")
                break
            else:
                print("Invalid event ID. Please enter a valid ID.")
        except ValueError:
            print("Invalid input. Please enter a valid integer ID.")


def check_registration_status():
    attendee_email = get_required_input(
        "Enter your email to check registration status: ")
    registrations = session.query(Registration).filter(
        Registration.attendee_email == attendee_email).all()
    if registrations:
        print("Your registration status:")
        for registration in registrations:
            print(
                f"Event: {registration.event.event_name}, Status: {registration.registration_status}")
            if registration.registration_status == "confirmed":
                print("Your registration is confirmed.")
            elif registration.registration_status == "pending":
                print("Your registration is pending approval")
            elif registration.registration_status == "cancelled":
                print("Your registration has been cancelled")
            else:
                print("Unknown registration status")
    else:
        print("No registrations found for the provided email.")


def create_event(organiser, event_name, registration_deadline, event_date, location):
    registration_deadline_date = datetime.strptime(registration_deadline, "%Y-%m-%d").date()
    event_date_date = datetime.strptime(event_date, "%Y-%m-%d").date()
    # Check if the registration deadline is in the future
    if registration_deadline_date < datetime.now().date():
        print("Registration deadline must be in the future.")
        return
    # Check if the event date is in the future
    if event_date_date < datetime.now().date():
        print("Event date must be in the future.")
        return
    # Check if the event name is provided
    if not event_name:
        print("Event name is required.")
        return
    # Check if the location is provided
    if not location:
        print("Location is required.")
        return
    # Ensure that the registration deadline is before the event date
    if registration_deadline_date >= event_date_date:
        print("Registration deadline must be before the event date.")
        return

    # Create the new event
    print("Event created successfully.")
    new_event = Event(event_name=event_name, location=location,
                      registration_deadline=registration_deadline_date, date=event_date_date)
    new_event.organiser = organiser
    session.add(new_event)
    session.commit()


def manage_registrations(organiser):
    events = organiser.events

    if not events:
        print("You have no events.")
        return

    print("Your Events:")
    for event in events:
        print(f"{event.id}: {event.event_name} - {event.date}")

    try:
        event_id = int(
            input("Enter the ID of the event to manage registrations: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer ID.")
        return

    event = session.query(Event).filter(
        Event.id == event_id, Event.organiser_id == organiser.id).first()

    if not event:
        print("Invalid event ID or you do not have access to manage registrations for this event.")
        return

    registrations = event.registrations

    print("Registrations for", event.event_name)
    for registration in registrations:
        print(f"ID: {registration.id}, Attendee Name: {registration.attendee_name}, Status: {registration.registration_status}")

    try:
        registration_id = int(
            input("Enter the ID of the registration to manage (0 to cancel): "))
    except ValueError:
        print("Invalid input. Please enter a valid integer ID.")
        return

    if registration_id == 0:
        return

    registration = session.query(Registration).filter(
        Registration.id == registration_id).first()

    if not registration:
        print("Registration not found.")
        return

    new_status = input("Enter new status (confirmed/pending/cancelled): ")

    if new_status not in ['confirmed', 'pending', 'cancelled']:
        print("Invalid status. Please enter either 'confirmed', 'pending', or 'cancelled'.")
        return

    registration.registration_status = new_status
    session.commit()
    print("Registration status updated.")




def send_notification(organiser, event_id, message):
    event = session.query(Event).filter(
        Event.id == event_id, Event.organiser_id == organiser.id).first()
    if event:
        attendees = [
            registration.attendee_email for registration in event.registrations]
        print(f"{message}:", attendees)
        # Logic to send notification
    else:
        print("Event not found.")


def register_organiser():
    print("Please provide the following information to register an organiser:")

    # Get organiser name
    organiser_name = input("Organiser Name: ")

    # Validate organiser name
    if not organiser_name:
        print("Organiser name cannot be empty.")
        return

    # Get organiser email
    organiser_email = input("Organiser Email: ")

    # Validate organiser email
    if not organiser_email:
        print("Organiser email cannot be empty.")
        return

    # Check if organiser with provided email already exists
    existing_organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()
    if existing_organiser:
        print("An organiser with this email already exists.")
        return

    # Create the organiser object
    organiser = Organiser(
        organiser_name=organiser_name,
        organiser_email=organiser_email
    )

    try:
        # Add organiser to the session and commit
        session.add(organiser)
        session.commit()
        print("Organiser registration successful!")
    except Exception as e:
        # Handle exceptions during registration
        print("An error occurred during organiser registration:", e)
        session.rollback()


def view_events_by_organiser():
    organiser_email = input(
        "Enter the email of the organiser to view their events: ")

    # Validate organiser email
    if not organiser_email:
        print("Organiser email cannot be empty.")
        return

    # Check if organiser with provided email exists
    organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()
    if organiser:
        print(f"Events by {organiser.organiser_name}:")
        for event in organiser.events:
            print(f"{event.id}: {event.event_name} - {event.date}")
    else:
        print("Organiser not found.")


def update_event(organiser):
    events = organiser.events

    if not events:
        print("You have no events.")
        return

    print("Your Events:")
    for event in events:
        print(f"{event.id}: {event.event_name} - {event.date}")

    try:
        event_id = int(input("Enter the ID of the event to update: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer ID.")
        return

    event = session.query(Event).filter(
        Event.id == event_id, Event.organiser_id == organiser.id).first()

    if not event:
        print("Invalid event ID or you do not have access to update this event.")
        return

    print("Current Event Details:")
    print(f"Name: {event.event_name}")
    print(f"Location: {event.location}")
    print(f"Registration Deadline: {event.registration_deadline}")
    print(f"Event Date: {event.date}")

    # Prompt user for updated information
    event_name = input(
        "Enter updated event name (leave blank to keep current): ")
    location = input("Enter updated location (leave blank to keep current): ")
    registration_deadline = input(
        "Enter updated registration deadline in YYYY-MM-DD format (leave blank to keep current): ")
    event_date = input(
        "Enter updated event date in YYYY-MM-DD format (leave blank to keep current): ")

    # Update event if input provided
    if event_name.strip():
        event.event_name = event_name
    if location.strip():
        event.location = location
    if registration_deadline.strip():
        event.registration_deadline = datetime.strptime(
            registration_deadline, "%Y-%m-%d").date()
    if event_date.strip():
        event.date = datetime.strptime(event_date, "%Y-%m-%d").date()

    session.commit()
    print("Event updated successfully.")


def delete_event(organiser):
    events = organiser.events

    if not events:
        print("You have no events.")
        return

    print("Your Events:")
    for event in events:
        print(f"{event.id}: {event.event_name} - {event.date}")

    try:
        event_id = int(input("Enter the ID of the event to delete: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer ID.")
        return

    event = session.query(Event).filter(
        Event.id == event_id, Event.organiser_id == organiser.id).first()

    if not event:
        print("Invalid event ID or you do not have access to delete this event.")
        return

    confirm = input(
        f"Are you sure you want to delete event '{event.event_name}'? (yes/no): ").lower()

    if confirm == 'yes':
        session.delete(event)
        session.commit()
        print("Event deleted successfully.")
    else:
        print("Deletion cancelled.")



def exit_program():
    print("Have fun,Dont drink & drive")
    exit()
