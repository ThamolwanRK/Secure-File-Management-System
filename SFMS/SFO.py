import mysql.connector
from datetime import datetime
import os


class SFO:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",  # Your MySQL host
            user="root",  # Your MySQL username
            password="mysql80",  # Your MySQL password
            database="securefilemanagement"  # Your database name
        )
        self.cursor = self.db.cursor()
        self.setup_tables()

    def setup_tables(self):
        # Create tables if they do not exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255),
                file_path VARCHAR(255),
                owner VARCHAR(255),
                created_at DATETIME
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_permissions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_id INT,
                user VARCHAR(255),
                can_read BOOLEAN DEFAULT 0,
                can_write BOOLEAN DEFAULT 0,
                can_share BOOLEAN DEFAULT 0,
                can_delete BOOLEAN DEFAULT 0,
                FOREIGN KEY (file_id) REFERENCES files(id)
            )
        """)
        self.db.commit()

    def add_file(self, file_name, file_path, owner):
        # Insert file metadata into the files table
        self.cursor.execute("""
            INSERT INTO files (file_name, file_path, owner, created_at)
            VALUES (%s, %s, %s, %s)
        """, (file_name, file_path, owner, datetime.now()))
        self.db_connection.commit()

        file_id = self.cursor.lastrowid

        # Grant full permissions to the owner
        self.cursor.execute("""
            INSERT INTO file_permissions (file_id, user, can_read, can_write, can_share, can_delete)
            VALUES (%s, %s, 1, 1, 1, 1)
        """, (file_id, owner))
        self.db_connection.commit()

    def check_permissions(self, file_name, username, permission):
        # Check if the user has the requested permission for the file
        self.cursor.execute("""
            SELECT fp.{permission}
            FROM files f
            JOIN file_permissions fp ON f.id = fp.file_id
            WHERE f.file_name = %s AND fp.user = %s
        """.format(permission=permission), (file_name, username))
        result = self.cursor.fetchone()
        return result and result[0] == 1

    def read_file(self, file_path, username):
        file_name = os.path.basename(file_path)

        # Check if the user has read permission
        if self.check_permissions(file_name, username, 'can_read'):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    print(f"File Content:\n{content}")
            except FileNotFoundError:
                print("File not found.")
        else:
            print(f"{username} does not have permission to read this file.")

    def write_file(self, file_name, content, username):
        # Check if the file already exists in the database
        self.cursor.execute("SELECT id, owner FROM files WHERE file_name = %s", (file_name,))
        file_info = self.cursor.fetchone()

        if file_info:
            file_id, owner = file_info
            # Check if the user has permission to write to the file
            self.cursor.execute("""
                SELECT can_write FROM file_permissions 
                WHERE file_id = %s AND user = %s
            """, (file_id, username))
            permission = self.cursor.fetchone()

            if permission and permission[0] == 1:
                # User has write permission, proceed to write to the file
                with open(file_name, 'w') as file:
                    file.write(content)
                print(f"File {file_name} written successfully.")
            else:
                print(f"{username} does not have permission to write to this file.")
        else:
            # File doesn't exist, create it and give full permissions to the owner
            self.add_file(file_name, file_name, username)
            with open(file_name, 'w') as file:
                file.write(content)
            print(f"New file {file_name} created and written successfully with full permissions for {username}.")

    def share_file(self, file_name, recipient, permissions, username):
        # Check if the user has permission to share the file
        if self.check_permissions(file_name, username, 'can_share'):
            # Retrieve the file ID from the database
            file_id = self.get_file_id(file_name)

            if file_id:
                self.cursor.execute("""
                    INSERT INTO file_permissions (file_id, user, can_read, can_write, can_share, can_delete)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE can_read=%s, can_write=%s, can_share=%s, can_delete=%s
                """, (file_id, recipient, permissions['can_read'], permissions['can_write'],
                      permissions['can_share'], permissions['can_delete'],
                      permissions['can_read'], permissions['can_write'],
                      permissions['can_share'], permissions['can_delete']))
                self.db.commit()
                print(f"File {file_name} shared successfully with {recipient}.")
            else:
                print(f"File {file_name} not found.")
        else:
            print(f"{username} does not have permission to share this file.")

    def get_file_id(self, file_name):
        # Query the database to get the file ID based on the file name
        self.cursor.execute("SELECT id FROM files WHERE file_name = %s", (file_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Return the file ID
        else:
            return None  # Return None if the file is not found

    def delete_file(self, file_path, username):
        file_name = os.path.basename(file_path)

        # Check if the user has delete permission
        if self.check_permissions(file_name, username, 'can_delete'):
            try:
                os.remove(file_path)
                print(f"File {file_path} deleted.")

                # Remove file entry from database
                self.cursor.execute("DELETE FROM files WHERE file_name = %s", (file_name,))
                self.cursor.execute(
                    "DELETE FROM file_permissions WHERE file_id = (SELECT id FROM files WHERE file_name = %s)",
                    (file_name,))
                self.db_connection.commit()
            except FileNotFoundError:
                print("File not found.")
        else:
            print(f"{username} does not have permission to delete this file.")
