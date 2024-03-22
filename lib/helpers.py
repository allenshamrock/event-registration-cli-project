from models import Event,session,Registration


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
                    registration_status="pending",
                    event_id=event_id
                )
                session.add(registration)
                session.commit()
                print("Registration successful!")
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
                    registration_status="pending",
                    event_id=event_id
                )
                session.add(registration)
                session.commit()
                print("Registration successful!")
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

def exit_program():
    print("Goodbye!")
    exit()
