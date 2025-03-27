from AAC import AAC
from SFO import SFO
from TDP import TDP

def main():
    aac = AAC()
    sfo = SFO()
    tdp = TDP()

    while True:
        print("\n-- Secure File Management System --")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        option = input("Select an option: ")

        if option == "1":
            username = input("Username: ")
            password = input("Password: ")
            aac.register_user(username, password)
            print("Registration successful! Returning to main menu.")

        elif option == "2":
            username = input("Username: ")
            password = input("Password: ")
            if aac.login_user(username, password):
                print(f"Welcome, {username}! Select a file operation:")
                while True:
                    print("\n-- File Operations --")
                    print("1. Read File")
                    print("2. Write File")
                    print("3. Share File")
                    print("4. View File Metadata")
                    print("5. Scan File for Threats")
                    print("6. Delete File")
                    print("7. Logout")
                    file_option = input("Select an option: ")

                    if file_option == "1":
                        file_path = input("Enter file path to read: ")
                        sfo.read_file(file_path, username)

                    elif file_option == "2":
                        file_path = input("Enter file path to write: ")
                        content = input("Enter content to write: ")
                        sfo.write_file(file_path, content, username)


                    elif file_option == "3":

                        file_path = input("Enter file path to share: ")

                        recipient = input("Enter recipient username: ")

                        read_permission = input("Allow read access (1/0): ")

                        write_permission = input("Allow write access (1/0): ")

                        share_permission = input("Allow share access (1/0): ")

                        delete_permission = input("Allow delete access (1/0): ")

                        # Create a dictionary of permissions

                        permissions = {

                            "can_read": int(read_permission),

                            "can_write": int(write_permission),

                            "can_share": int(share_permission),

                            "can_delete": int(delete_permission)

                        }

                        # Pass the 'username' of the logged-in user to share_file

                        sfo.share_file(file_path, recipient, permissions, username)


                    elif file_option == "4":
                        file_path = input("Enter file path to view metadata: ")
                        sfo.view_metadata(file_path)

                    elif file_option == "5":
                        file_path = input("Enter file path to scan: ")
                        tdp.scan_for_malware(file_path)

                    elif file_option == "6":
                        file_path = input("Enter file path to delete: ")
                        sfo.delete_file(file_path, username)

                    elif file_option == "7":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Try again.")

        elif option == "3":
            print("Exiting the system.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
