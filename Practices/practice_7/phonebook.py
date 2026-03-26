import psycopg2
import csv
from config import config


def create_tables():
    """Create the phonebook table"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS phonebook (
            contact_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            phone_number VARCHAR(20) UNIQUE NOT NULL
        )
        """,
    )
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("Table created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_from_console():
    """Insert data via console input"""
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone = input("Enter phone number: ")

    sql = """INSERT INTO phonebook(first_name, last_name, phone_number)
             VALUES(%s, %s, %s) RETURNING contact_id;"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (first_name, last_name, phone))
        contact_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print(f"Contact added with ID: {contact_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def upload_from_csv(file_path):
    """Insert data from a CSV file"""
    sql = "INSERT INTO phonebook(first_name, last_name, phone_number) VALUES(%s, %s, %s)"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header safely
            for row in reader:
                if len(row) == 3:
                    cur.execute(sql, row)

        conn.commit()
        cur.close()
        print("Data uploaded from CSV successfully.")
    except FileNotFoundError:
        print("CSV file not found.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def show_all_contacts():
    """Show all contacts"""
    sql = "SELECT * FROM phonebook ORDER BY contact_id"

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        if rows:
            print("\n--- ALL CONTACTS ---")
            for row in rows:
                print(row)
        else:
            print("No contacts found.")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_contact(phone_number, new_first_name=None, new_phone=None):
    """Update first name or phone number by current phone number"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        if new_first_name:
            cur.execute(
                "UPDATE phonebook SET first_name = %s WHERE phone_number = %s",
                (new_first_name, phone_number)
            )

        if new_phone:
            cur.execute(
                "UPDATE phonebook SET phone_number = %s WHERE phone_number = %s",
                (new_phone, phone_number)
            )

        conn.commit()
        print(f"Updated {cur.rowcount} row(s).")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def query_contacts(filter_type, value):
    """Query data with different filters"""
    allowed_filters = ['first_name', 'last_name', 'phone_number']

    if filter_type not in allowed_filters:
        print("Invalid filter type.")
        return

    sql = f"SELECT * FROM phonebook WHERE {filter_type} ILIKE %s"

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (f'%{value}%',))
        rows = cur.fetchall()

        if rows:
            print("\n--- SEARCH RESULTS ---")
            for row in rows:
                print(row)
        else:
            print("No matching contacts found.")

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_contact(identifier):
    """Delete contact by first_name OR phone_number"""
    sql = "DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s"
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (identifier, identifier))
        conn.commit()
        print(f"Deleted {cur.rowcount} row(s).")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def menu():
    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Upload from CSV")
        print("4. Show all contacts")
        print("5. Search contacts")
        print("6. Update contact")
        print("7. Delete contact")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_tables()

        elif choice == "2":
            insert_from_console()

        elif choice == "3":
            file_path = input("Enter CSV file path: ")
            upload_from_csv(file_path)

        elif choice == "4":
            show_all_contacts()

        elif choice == "5":
            print("Search by: first_name / last_name / phone_number")
            filter_type = input("Enter filter type: ")
            value = input("Enter search value: ")
            query_contacts(filter_type, value)

        elif choice == "6":
            phone_number = input("Enter current phone number of contact: ")
            new_first_name = input("Enter new first name (or press Enter to skip): ")
            new_phone = input("Enter new phone number (or press Enter to skip): ")

            if new_first_name == "":
                new_first_name = None
            if new_phone == "":
                new_phone = None

            update_contact(phone_number, new_first_name, new_phone)

        elif choice == "7":
            identifier = input("Enter first name OR phone number to delete: ")
            delete_contact(identifier)

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    menu()