import mysql.connector
import pyclamd  # ClamAV integration
from datetime import datetime

class TDP:
    def __init__(self):
        # Database connection for logging
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql80",
            database="securefilemanagement"
        )
        self.cursor = self.db_connection.cursor()
        self.setup_tables()

        # Try setting up ClamAV client via network socket
        try:
            self.clamd = pyclamd.ClamdNetworkSocket()  # For network-based connection
            if not self.clamd.ping():
                raise Exception("ClamAV service is not available.")
        except Exception as e:
            self.clamd = None
            print("Error connecting to ClamAV:", str(e))

    def setup_tables(self):
        # Create tables if they do not exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS threat_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255),
                file_path VARCHAR(255),
                scanned_at DATETIME,
                threat_detected BOOLEAN,
                virus_name VARCHAR(255)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_access_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255),
                file_name VARCHAR(255),
                access_type VARCHAR(50),
                accessed_at DATETIME
            )
        """)
        self.db_connection.commit()

    def log_file_access(self, username, file_name, access_type):
        # Logs file access into the database
        query = """
            INSERT INTO file_access_logs (username, file_name, access_type, accessed_at)
            VALUES (%s, %s, %s, %s)
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(query, (username, file_name, access_type, timestamp))
        self.db_connection.commit()

    def scan_for_malware(self, file_path):
        # Check if ClamAV is available
        if not self.clamd:
            print("ClamAV is not available. Please ensure ClamAV is running.")
            return

        # Check if the file exists
        try:
            scan_result = self.clamd.scan_file(file_path)
        except Exception as e:
            print(f"Error scanning file {file_path}: {str(e)}")
            return

        # Logging the scan results in the database
        virus_name = None
        threat_detected = False
        if scan_result and file_path in scan_result and scan_result[file_path][0] == 'FOUND':
            virus_name = scan_result[file_path][1]
            threat_detected = True
            print(f"Virus detected: {virus_name} in file {file_path}")
        else:
            print(f"No threats detected in file {file_path}")

        # Log to MySQL database
        self.cursor.execute("""
            INSERT INTO threat_logs (file_name, file_path, scanned_at, threat_detected, virus_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (file_path.split('/')[-1], file_path, datetime.now(), threat_detected, virus_name))
        self.db_connection.commit()

        return threat_detected
