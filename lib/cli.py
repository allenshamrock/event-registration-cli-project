from helpers import (
    exit_program,
    register_attendee,
    check_registration_status
   
)


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
        else: 
           print("Invalid choice")


def menu():
    print("\nWelcome to Event Registration System\n")
    print("0. Exit the program")
    print("1. Register for an event")
    print("2. Check registration status")
    print("3. Exit")


if __name__ == "__main__":
    main()
