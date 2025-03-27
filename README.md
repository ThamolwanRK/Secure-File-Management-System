Secure File Management System

Overview:
The Secure File Management System (SFMS) is a project designed to allow users to securely manage their files. This system implements features such as user authentication, secure file sharing, permission-based access, file metadata management, and malware detection using ClamAV integration. The project is built using Python and MySQL for database management.


Features:

User Authentication:
-Register new users with secure password hashing.
-Login system for authentication of existing users.

File Operations:
-Read files (based on permission).
-Write to files (based on permission).
-Share files with other users by granting specific permissions.
-View file metadata.
-Delete files (based on permission).

Threat Detection:
-Scan files for potential malware using ClamAV.
-Permissions Management:
-Assign and modify file permissions (read, write, share, delete) for different users.


Installation:

1. Clone the Repository:
git clone https://github.com/your-username/secure-file-management-system.git
cd secure-file-management-system

2. Set Up Virtual Environment (Optional but recommended):
python -m venv .venv
source .venv/bin/activate    # On Windows, use `.venv\Scripts\activate`

3. Install Required Dependencies:
pip install -r requirements.txt

4. Set Up MySQL Database
-Install and run MySQL on your local machine.
-Create a database named securefilemanagement.
-Inside MySQL, create the necessary tables. These will be automatically created by the code when you first run the project.

5. ClamAV Installation (for Malware Detection)
-To use the malware detection functionality, ClamAV must be installed and running on your system.
-Install ClamAV (ClamAV installation guide).
-Ensure the ClamAV daemon is running so that files can be scanned.


Usage:
-Run the main program using the following command:
python main.py
-The program will prompt users to log in or register. Once authenticated, users can perform various file operations such as reading, writing, sharing, and scanning files for malware. The system applies permission checks before each operation.


Modules:

1. Authentication & Access Control Module (AAC):
Manages user registration and login with hashed passwords using MySQL as the backend database.

2. Secure File Operations Module (SFO):
Handles all file-related operations, including reading, writing, sharing, and deleting files. Permission checks are applied before each operation.

3. Threat Detection & Prevention Module (TDP):
Integrates ClamAV for malware scanning and logs all file accesses and threats.


Technologies Used:

-Programming Language: Python

-Database: MySQL

-Threat Detection: ClamAV


Future Improvements:

-Implement email notifications for important file operations.
-Enhance the malware scanning module for real-time file scanning.
