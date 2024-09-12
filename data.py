import mysql.connector
from mysql.connector import Error
from db_config import get_connection

def view_employees():
    """Fetch and display all employees from the database."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if not employees:
            print("No employees found.")
        else:
            for emp in employees:
                print(f"ID: {emp['emp_id']}, Name: {emp['name']}")
    else:
        print("Failed to connect to the database.")

def add_employee(emp_id, name):
    """Add a new employee to the database."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO employees (emp_id, name) VALUES (%s, %s)", (emp_id, name))
            connection.commit()
            print("Employee added successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def approve_request(emp_id):
    """Approve a leave request for an employee."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE leave_requests SET status = 'approved' WHERE emp_id = %s", (emp_id,))
            connection.commit()
            print(f"Leave request for employee {emp_id} approved.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def decline_request(emp_id):
    """Decline a leave request for an employee."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE leave_requests SET status = 'declined' WHERE emp_id = %s", (emp_id,))
            connection.commit()
            print(f"Leave request for employee {emp_id} declined.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def delete_employee(emp_id):
    """Delete an employee from the database."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
            connection.commit()
            print("Employee data deleted.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def request_leave(emp_id, leave_request):
    """Submit a leave request for an employee."""
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO leave_requests (emp_id, request_details) VALUES (%s, %s)", (emp_id, leave_request))
            connection.commit()
            print("Leave request submitted.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")
