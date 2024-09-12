import mysql.connector
from mysql.connector import Error

def get_connection():
    """Establish and return a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            user='root',       
            password='password', 
            database='employee_management' 
        )
        if connection.is_connected():
            print("Connection to the database established successfully.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
