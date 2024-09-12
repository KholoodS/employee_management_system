from admin import admin_menu
from employee import employee_menu

def main_menu():
    while True:
        print("Welcome to the Employee Management System")
        print("1. Admin Side")
        print("2. Employee Side")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            admin_menu()
        elif choice == '2':
            employee_menu()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
