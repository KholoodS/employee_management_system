import mysql.connector
from mysql.connector import Error
from db_config import get_connection

def view_employees():
    """Fetch and display all employees and their assigned managers from the employee_managers table."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT e.emp_id, e.name, e.joining_date, e.role, em.manager_name
            FROM employees e
            LEFT JOIN employee_managers em ON e.emp_id = em.emp_id
            ORDER BY e.emp_id
        """
        cursor.execute(query)
        employees = cursor.fetchall()
        cursor.close()
        connection.close()

        if not employees:
            print("\n|----------------------|")
            print("| No employees found.  |")
            print("|----------------------|\n")
        else:
            print("\n| Employee List |")
            print("|--------------------------------------------------|")
            print("| ID  | Name           | Role        | Joining Date | Manager       |")
            print("|-----|----------------|-------------|--------------|---------------|")
            for emp in employees:
                manager = emp['manager_name'] if emp['manager_name'] else "No manager assigned"
                print(f"| {emp['emp_id']:<4} | {emp['name']:<14} | {emp['role']:<11} | {emp['joining_date']}  | {manager:<13} |")
            print("|-----------------------------------------------|\n")
    else:
        print("Failed to connect to the database.")

def view_leave_requests():
    """Fetch and display all leave requests and their status."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT emp_id, leave_start_date, leave_end_date, status
            FROM leave_request_status
        """
        cursor.execute(query)
        requests = cursor.fetchall()
        cursor.close()
        connection.close()

        if not requests:
            print("\n|--------------------------|")
            print("| No leave requests found.  |")
            print("|--------------------------|\n")
        else:
            print("\n| Leave Requests |")
            print("|--------------------------------------------------|")
            print("| Emp ID | Start Date | End Date   | Status        |")
            print("|--------|------------|------------|---------------|")
            for req in requests:
                print(f"| {req['emp_id']:<6} | {req['leave_start_date']} | {req['leave_end_date']} | {req['status']:<8} |")
            print("|---------------------------------------------------------------|\n")
    else:
        print("Failed to connect to the database.")

def assign_manager():
    """Assign a manager to an employee based on Employee ID."""
    emp_id = input("\nEnter Employee ID to assign a manager: ")
    manager_name = input("Enter Manager Name: ")

    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Update or insert the manager information
            cursor.execute(
                """
                INSERT INTO employee_managers (emp_id, manager_name)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE manager_name = VALUES(manager_name)
                """,
                (emp_id, manager_name)
            )
            connection.commit()

            # Check how many rows were updated
            rows_affected = cursor.rowcount
            if rows_affected > 0:
                print("\n|-------------------------------------|")
                print("| Manager assigned successfully.      |")
                print("|-------------------------------------|\n")
            else:
                print("\n|------------------------------------------|")
                print("| No employee found with the given ID.     |")
                print("|------------------------------------------|\n")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def handle_leave_request():
    """Approve or decline a leave request."""
    emp_id = input("\nEnter Employee ID: ")
    leave_start_date = input("Enter Leave Start Date (YYYY-MM-DD): ")
    leave_end_date = input("Enter Leave End Date (YYYY-MM-DD): ")
    action = input("Enter 'approve' to approve or 'decline' to decline the leave request: ").strip().lower()

    if action not in ['approve', 'decline']:
        print("Invalid action. Please enter 'approve' or 'decline'.")
        return

    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            status = 'approved' if action == 'approve' else 'declined'
            cursor.execute(
                "UPDATE leave_request_status SET status = %s WHERE emp_id = %s AND leave_start_date = %s AND leave_end_date = %s",
                (status, emp_id, leave_start_date, leave_end_date)
            )
            connection.commit()
            print(f"\n|----------------------------------|")
            print(f"| Leave request {status.capitalize()} successfully. |")
            print(f"|----------------------------------|\n")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def admin_menu():
    while True:
        print("\n|--------------------------|")
        print("|        Admin Menu        |")
        print("|--------------------------|")
        print("| 1. View Employee List     |")
        print("| 2. View Leave Requests    |")
        print("| 3. Assign Manager         |")
        print("| 4. Handle Leave Request   |")
        print("| 5. Exit to Main Menu      |")
        print("|--------------------------|")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            view_employees()
        elif choice == '2':
            view_leave_requests()
        elif choice == '3':
            assign_manager()
        elif choice == '4':
            handle_leave_request()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    admin_menu()
