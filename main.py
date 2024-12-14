import pandas as pd
import sqlite3
import time
import getpass
from hashlib import sha256

# ================= Constants ===================
DB_PATH = "health_centres.db"
TABLE_NAME = "health_centres"
INACTIVITY_TIMEOUT = 120  # seconds
ADMIN_PASSWORD_HASH = sha256("admin123".encode()).hexdigest()

# =================== for initialize database ==============
def initialize_database(csv_file_path):
    """Load CSV data into an SQLite database."""
    df = pd.read_csv(csv_file_path)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    conn.close()

# =================== for query data ====================
def query_data(query, params=()):
    """Execute a SQL query and return the results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# ==================== for execute query ===================
def execute_query(query, params=()):
    """Execute a SQL query without returning results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

# ==================== for user interface ===================
def user_interface():
    start_time = time.time()

    while True:
        if time.time() - start_time > INACTIVITY_TIMEOUT:
            print("\nSession timed out due to inactivity. Returning to the main menu.\n")
            break

        print("\nWelcome to the HSE information Kisok\nChoose from the selection presented")
        print('\nGeneral Site Search')
        print("1. By town")
        print("2. By site")

        print('\nSpecific searches')
        print('3. Phone number search')
        print('4. Location Search')
        print('5. Role Search')

        choice = input("Selection: ")

        if choice == "1":
            search_query = input("Which town?: ")

            results = query_data(
                f"SELECT * FROM {TABLE_NAME} WHERE Town LIKE ?",
                ('%' + search_query + '%',)  # Make sure this is a tuple
            )

            if results:
                for row in results:
                    print('-------------------------------')
                    print(
                        f"ID            : {row[0]}\n"
                        f"Hospital Name : {row[1]}\n"
                        f"Latitude      : {row[2]}\n"
                        f"Longitude     : {row[3]}\n"
                        f"Address       : {row[4]}\n"
                        f"Town          : {row[5]}\n"
                        f"Eircode       : {row[6]}\n"
                        f"Role          : {row[7]}\n"
                        f"Phone         : {row[8]}\n"
                    )
                    print('-------------------------------')
            else:
                print("\nNo results found.")
        elif choice == "2":
            print("\nImplementation in-progress\n")
            break
        elif choice == "3":
            search_query = input("Which hospital or location?: ")
            results = query_data(
                f"SELECT * FROM {TABLE_NAME} WHERE Town LIKE ? OR `Hospital name` LIKE ?",
                (f"%{search_query}%", f"%{search_query}%")
            )

            if results:
                for row in results:
                    print("---------------------------------")
                    print(
                        f"Hospital Name   : {row[1]}\n" 
                        f"Phone           : {row[8]}"
                    )
                    print("---------------------------------")
            else:
                print("\nNo results found.")

            break
        elif choice == "4":
            search_query = input("Which area?: ")
            results = query_data(
                f"SELECT * FROM {TABLE_NAME} WHERE `Hospital name` LIKE ?",
                ('%' + search_query + '%',)
            )

            if results:
                for row in results:
                    print("---------------------------------")
                    print(
                        f"Hospital Name   : {row[1]}\n"
                        f"Latitude        : {row[2]}\n"
                        f"Logitude        : {row[3]}\n"
                        f"Address         : {row[4]}\n"
                        f"Eircode         : {row[6]}"
                    )
                    print("---------------------------------")
            else:
                print("\nNo results found.")

            break
        elif choice == "5":
            search_query = input("Which hospital or location?: ")
            results = query_data(
                f"SELECT * FROM {TABLE_NAME} WHERE Town LIKE ? OR `Hospital name` LIKE ?",
                (f"%{search_query}%", f"%{search_query}%")
            )

            if results:
                for index, row in enumerate(results, start=1):
                    print(f"{index}. {row[7]}")
            else:
                print("\nNo results found.")

            break
        else:
            print("\nInvalid choice. Please try again.\n")

        start_time = time.time()


# =============== for admin interface ======================
def admin_interface():
    while True:
        password = getpass.getpass("Enter admin password: ")
        if sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
            break
        print("Incorrect password. Try again.")

    while True:
        print("\nAdmin Interface")
        print("1. Add a new health centre")
        print("2. Edit an existing health centre")
        print("3. Delete a health centre")
        print("4. Exit to main menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            id_ = input("Enter ID: ")
            name = input("Enter hospital name: ")
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            address = input("Enter address: ")
            town = input("Enter town: ")
            eircode = input("Enter eircode: ")
            role = input("Enter role: ")
            phone = input("Enter phone: ")

            execute_query(f"INSERT INTO {TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                          (id_, name, latitude, longitude, address, town, eircode, role, phone))
            print("Health centre added successfully.")

        elif choice == "2":
            id_ = input("Enter ID of the health centre to edit: ")
            column = input("Enter the column to edit: ")
            new_value = input("Enter the new value: ")
            execute_query(f"UPDATE {TABLE_NAME} SET {column} = ? WHERE ID = ?", (new_value, id_))
            print("Health centre updated successfully.")

        elif choice == "3":
            id_ = input("Enter ID of the health centre to delete: ")
            execute_query(f"DELETE FROM {TABLE_NAME} WHERE ID = ?", (id_,))
            print("Health centre deleted successfully.")

        elif choice == "4":
            print("\nExiting to main menu.\n")
            break

        else:
            print("Invalid choice. Please try again.")

# ================ main function ===================
def main():
    # ================= initialize database
    initialize_database("ireland_health_centres.csv")

    while True:
        print("Welcome to the HSE Health Centre Kiosk\n")
        print("1. User")
        print("2. Admin")
        print("3. Exit")

        choice = input("Selection: ")

        if choice == "1":
            # ============= for user interface
            user_interface()
        elif choice == "2":
            # ============= for admin interface
            admin_interface()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # =============== call main function
    main()
