import click
from models import session,Organiser,Registration,Event
from datetime import datetime


def get_required_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip():
            return user_input
        else:
            click.echo("This field is required. Please provide a value.")

@click.command()
def register_attendee():
    click.echo("Please provide the following information to register for an event:")
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
                print(
                    f"{registration.attendee_name} your registration for {registration.event.event_name} was  successful!")
                break
            else:
                print("Invalid event ID. Please enter a valid ID.")
        except ValueError:
            print("Invalid input. Please enter a valid integer ID.")


@click.command()
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
                click.echo("Your registration has been cancelled")
            else:
                click.echo("Unknown registration status")
    else:
        click.echo("No registrations found for the provided email.")


@click.command()
def create_event():
    organiser_email = input("Enter organiser email: ")
    event_name = input("Event Name: ")
    event_date = input("Event Date (YYYY-MM-DD): ")
    location = input("Location: ")
    registration_deadline = input("Registration Deadline (YYYY-MM-DD): ")

    organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()

    if not organiser:
        click.echo("Organiser not found.")
        return

    registration_deadline_date = datetime.strptime(
        registration_deadline, "%Y-%m-%d").date()
    event_date_date = datetime.strptime(event_date, "%Y-%m-%d").date()

    # Check if the registration deadline is in the future
    if registration_deadline_date < datetime.now().date():
        click.echo("Registration deadline must be in the future.")
        return

    # Check if the event date is in the future
    if event_date_date < datetime.now().date():
        click.echo("Event date must be in the future.")
        return

    # Check if the event name is provided
    if not event_name:
        click.echo("Event name is required.")
        return

    # Check if the location is provided
    if not location:
        click.echo("Location is required.")
        return

    # Ensure that the registration deadline is before the event date
    if registration_deadline_date >= event_date_date:
        click.echo("Registration deadline must be before the event date.")
        return

    # Create the new event
    click.echo("Event created successfully.")
    new_event = Event(event_name=event_name, location=location,
                      registration_deadline=registration_deadline_date, date=event_date_date)
    new_event.organiser = organiser
    session.add(new_event)
    session.commit()


@click.command()
@click.option('--organiser_email', prompt="Enter organiser email:", help="Email of the organiser to manage registrations for.")
def manage_registrations(organiser_email):
    organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()

    if not organiser:
        click.echo("Organiser not found.")
        return

    events = organiser.events

    if not events:
        click.echo("You have no events.")
        return

    click.echo("Your Events:")
    for event in events:
        click.echo(f"{event.id}: {event.event_name} - {event.date}")

    try:
        event_id = int(
            input("Enter the ID of the event to manage registrations: "))
    except ValueError:
        click.echo("Invalid input. Please enter a valid integer ID.")
        return

    event = session.query(Event).filter(
        Event.id == event_id, Event.organiser_id == organiser.id).first()

    if not event:
        click.echo(
            "Invalid event ID or you do not have access to manage registrations for this event.")
        return

    registrations = event.registrations

    click.echo(f"Registrations for {event.event_name}")
    for registration in registrations:
        click.echo(
            f"ID: {registration.id}, Attendee Name: {registration.attendee_name}, Status: {registration.registration_status}")

    try:
        registration_id = int(
            input("Enter the ID of the registration to manage (0 to cancel): "))
    except ValueError:
        click.echo("Invalid input. Please enter a valid integer ID.")
        return

    if registration_id == 0:
        return

    registration = session.query(Registration).filter(
        Registration.id == registration_id).first()

    if not registration:
        click.echo("Registration not found.")
        return

    new_status = input("Enter new status (confirmed/pending/cancelled): ")

    if new_status not in ['confirmed', 'pending', 'cancelled']:
        click.echo(
            "Invalid status. Please enter either 'confirmed', 'pending', or 'cancelled'.")
        return

    registration.registration_status = new_status
    session.commit()
    click.echo("Registration status updated.")

@click.command()
def send_notification():
    organiser_email = input("Enter organiser email: ")
    event_id = int(input("Enter event ID: "))
    message = input("Enter message: ")

    organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()

    if organiser:
        event = session.query(Event).filter(
            Event.id == event_id, Event.organiser_id == organiser.id).first()

        if event:
            attendees = [
                registration.attendee_email for registration in event.registrations]
            attendees_str = ', '.join(attendees)
            click.echo(f"{message}: {attendees_str}")
            # Logic to send notification
        else:
            click.echo("Event not found.")
    else:
        click.echo("Organiser not found.")


@click.command()
def register_organiser():
    click.echo("Please provide the following information to register an organiser:")

    # Get organiser name
    organiser_name = input("Organiser Name: ")

    # Validate organiser name
    if not organiser_name:
        click.echo("Organiser name cannot be empty.")
        return

    # Get organiser email
    organiser_email = input("Organiser Email: ")

    # Validate organiser email
    if not organiser_email:
        click.echo("Organiser email cannot be empty.")
        return

    # Check if organiser with provided email already exists
    existing_organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()
    if existing_organiser:
        click.echo("An organiser with this email already exists.")
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
        click.echo("Organiser registration successful!")
    except Exception as e:
        # Handle exceptions during registration
        click.echo("An error occurred during organiser registration:", e)
        session.rollback()


@click.command()
def view_events_by_organiser():
    organiser_email = input(
        "Enter the email of the organiser to view their events: ")

    # Validate organiser email
    if not organiser_email:
        click.echo("Organiser email cannot be empty.")
        return

    # Check if organiser with provided email exists
    organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()
    if organiser:
        click.echo(f"Events by {organiser.organiser_name}:")
        for event in organiser.events:
            click.echo(f"{event.id}: {event.event_name} - {event.date}")
    else:
        click.echo("Organiser not found.")


@click.command()
def update_event():
    organiser_email = input("Enter your email: ")

    organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()

    if not organiser:
        click.echo("Organiser not found.")
        return

    events = organiser.events

    if not events:
        click.echo("You have no events.")
        return

    click.echo("Your Events:")
    for event in events:
        click.echo(f"{event.id}: {event.event_name} - {event.date}")

    try:
        event_id = int(input("Enter the ID of the event to update: "))
    except ValueError:
        click.echo("Invalid input. Please enter a valid integer ID.")
        return

    event = session.query(Event).filter(
        Event.id == event_id, Event.organiser_id == organiser.id).first()

    if not event:
        click.echo(
            "Invalid event ID or you do not have access to update this event.")
        return

    click.echo("Current Event Details:")
    click.echo(f"Name: {event.event_name}")
    click.echo(f"Location: {event.location}")
    click.echo(f"Registration Deadline: {event.registration_deadline}")
    click.echo(f"Event Date: {event.date}")

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
    click.echo("Event updated successfully.")

@click.command()
def delete_event():
    organiser_email = input("Enter your email: ")

    organiser = session.query(Organiser).filter(
        Organiser.organiser_email == organiser_email).first()

    if not organiser:
        click.echo("Organiser not found.")
        return

    events = organiser.events

    if not events:
        click.echo("You have no events.")
        return

    click.echo("Your Events:")
    for event in events:
        click.echo(f"{event.id}: {event.event_name} - {event.date}")

    try:
        event_id = int(input("Enter the ID of the event to delete: "))
    except ValueError:
        click.echo("Invalid input. Please enter a valid integer ID.")
        return

    event = session.query(Event).filter(
        Event.id == event_id, Event.organiser_id == organiser.id).first()

    if not event:
        click.echo(
            "Invalid event ID or you do not have access to delete this event.")
        return

    confirm = input(
        f"Are you sure you want to delete event '{event.event_name}'? (yes/no): ").lower()

    if confirm == 'yes':
        session.delete(event)
        session.commit()
        click.echo("Event deleted successfully.")
    else:
        click.echo("Deletion cancelled.")

@click.command
def exit_program():
    click.echo("Have fun,Dont drink & drive")
    exit()


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            register_attendee()
        elif choice == "2":
            check_registration_status()
        elif choice == "3":
            register_organiser()
        elif choice == "4":
            manage_registrations()
        elif choice == "5":
            view_events_by_organiser()
        elif choice == "6":
            send_notification()
        elif choice == "7":
            create_event()
        elif choice == "8":
            update_event()
        elif choice == "9":
            delete_event()
        else: 
           click.echo("Invalid choice")



def menu():
    click.echo("\nWelcome to Eventbrite  System\n")
    click.echo("0.Exit the program")
    click.echo("1.Register for an event")
    click.echo("2.Check registration status")
    click.echo("3.Register an Orgainiser")
    click.echo("4.Manage Registrations")
    click.echo("5.View events by Organiser")
    click.echo("6.Send Notifications")
    click.echo("7.Create event")
    click.echo("8.Update event")
    click.echo("9.Delete event")

if __name__ == "__main__":
    main()
