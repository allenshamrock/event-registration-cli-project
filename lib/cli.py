from helpers import (
    exit_program,
    register_attendee,
    check_registration_status,
    create_event,
    manage_registrations,
    send_notification,
    register_organiser,
    view_events_by_organiser,
    update_event,
    delete_event
   
)
from models import session,Organiser
from datetime import datetime


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
            organiser_email = input("Enter organiser email: ")
            organiser = session.query(Organiser).filter(
            Organiser.organiser_email == organiser_email).first()
            if organiser:
                manage_registrations(organiser)
        elif choice == "5":
            view_events_by_organiser()
        elif choice == "6":
            organiser_email = input("Enter organiser email: ")
            organiser = session.query(Organiser).filter(
            Organiser.organiser_email == organiser_email).first()
            if organiser:
                event_id = int(input("Enter event ID: "))
                message = input("Enter message: ")
                send_notification(organiser, event_id, message)
            else:
                print("Organiser not found.")

        elif choice == "7":
            organiser_email = input("Enter organiser email: ")
            organiser = session.query(Organiser).filter(
            Organiser.organiser_email == organiser_email).first()
            if organiser:
                event_name = input("Event Name: ")
                event_date = input("Event Date (YYYY-MM-DD): ")
                location = input("Location: ")
                registration_deadline = input(
                    "Registration Deadline (YYYY-MM-DD): ")
                create_event(organiser, event_name,
                             registration_deadline, event_date, location)
            else:
                print("Organiser not found.")
        elif choice == "8":
                    organiser_email = input("Enter your email: ")
                    organiser = session.query(Organiser).filter(Organiser.organiser_email == organiser_email).first()

                    if not organiser:
                        print("Organiser not found.")
                        return
                    update_event(organiser)
        elif choice == "9":
                organiser_email = input("Enter your email: ")
                organiser = session.query(Organiser).filter(Organiser.organiser_email == organiser_email).first()

                if not organiser:
                        print("Organiser not found.")
                        return
                delete_event(organiser)
        else: 
           print("Invalid choice")


def menu():
    print("\nWelcome to  System\n")
    print("0.Exit the program")
    print("1.Register for an event")
    print("2.Check registration status")
    print("3.Register an Orgainiser")
    print("4.Manage Registrations")
    print("5.View events by Organiser")
    print("6.Send Notifications")
    print("7.Create event")
    print("8.Update event")
    print("9.Delete event")

if __name__ == "__main__":
    main()
