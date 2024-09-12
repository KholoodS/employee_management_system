import mysql.connector
from mysql.connector import Error
from db_config import get_connection

def add_employee():
    """Add a new employee to the database."""
    name = input("Enter Employee Name: ")
    role = input("Enter Role (admin/employee): ")
    joining_date = input("Enter Joining Date (YYYY-MM-DD): ")
    
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO employees (name, role, joining_date) VALUES (%s, %s, %s)",
                           (name, role, joining_date))
            connection.commit()
            print("Employee added successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def request_leave():
    """Submit a leave request for the employee."""
    emp_id = input("Enter Your Employee ID: ")
    leave_start_date = input("Enter Leave Start Date (YYYY-MM-DD): ")
    leave_end_date = input("Enter Leave End Date (YYYY-MM-DD): ")
    
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO leave_request_status (emp_id, leave_start_date, leave_end_date, status) VALUES (%s, %s, %s, 'pending')", 
                           (emp_id, leave_start_date, leave_end_date))
            connection.commit()
            print("Leave request submitted.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def check_leave_status():
    """Check the status of the leave request for the employee."""
    emp_id = input("Enter Your Employee ID: ")
    
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT leave_start_date, leave_end_date, status FROM leave_request_status WHERE emp_id = %s", (emp_id,))
        requests = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if requests:
            print(f"Leave Request Details for Employee ID {emp_id}:")
            for request in requests:
                print(f"Start Date: {request['leave_start_date']}")
                print(f"End Date: {request['leave_end_date']}")
                print(f"Status: {request['status']}")
        else:
            print("No leave request found or request has been processed.")
    else:
        print("Failed to connect to the database.")

def employee_menu():
    while True:
        print("\nEmployee Menu")
        print("1. Add New Employee")
        print("2. Request Leave")
        print("3. Check Leave Status")
        print("4. Exit to Main Menu")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            request_leave()
        elif choice == '3':
            check_leave_status()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")
