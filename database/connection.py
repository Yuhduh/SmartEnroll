import mysql.connector
from mysql.connector import Error
from database.config import ACTIVE_CONFIG

class DatabaseConnection:
    def __init__(self):
        self.config = ACTIVE_CONFIG

    def get_connection(self):
        """Returns a raw MySQL connection"""
        try:
            return mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
        except Error as e:
            print(f"Database Connection Error: {e}")
            return None

    def test_connection(self):
        """Test if the database is accessible"""
        conn = self.get_connection()
        if conn:
            conn.close()
            return True
        return False