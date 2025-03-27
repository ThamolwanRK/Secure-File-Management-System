import mysql.connector
import hashlib

class AAC:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql80",
            database="securefilemanagement"
        )
        self.cursor = self.db_connection.cursor()
        self.setup_tables()

    def setup_tables(self):
        # Create table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            )
        """)
        self.db_connection.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        hashed_password = self.hash_password(password)

        # Insert into MySQL database
        self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                            (username, hashed_password))
        self.db_connection.commit()

        print(f"User {username} registered.")
        return True

    def login_user(self, username, password):
        self.cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        record = self.cursor.fetchone()
        if record and record[0] == self.hash_password(password):
            print("Login successful!")
            return True
        else:
            print("Invalid username or password.")
            return False
