import psycopg2
from config import load_config
def connect():
    config = load_config()
    conn = psycopg2.connect(**config)
    conn.autocommit = True
    return conn
conn = connect()
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS phonebook(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20)
);
""")
cur.execute("""
CREATE OR REPLACE FUNCTION search_pattern(p_pattern TEXT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    WHERE phonebook.first_name ILIKE '%' || p_pattern || '%'
       OR phonebook.last_name ILIKE '%' || p_pattern || '%'
       OR phonebook.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;
""")
cur.execute("""
CREATE OR REPLACE PROCEDURE insert_or_update(p_first TEXT, p_last TEXT, p_phone TEXT)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_first AND last_name = p_last) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_first AND last_name = p_last;
    ELSE
        INSERT INTO phonebook(first_name, last_name, phone) VALUES (p_first, p_last, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;
""")
cur.execute("""
CREATE TEMP TABLE temp_users(
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone VARCHAR(20)
);
""")
cur.execute("""
CREATE OR REPLACE PROCEDURE insert_many()
AS $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN SELECT * FROM temp_users LOOP
        IF rec.phone ~ '^[0-9]+$' THEN
            INSERT INTO phonebook(first_name, last_name, phone)
            VALUES (rec.first_name, rec.last_name, rec.phone);
        ELSE
            RAISE NOTICE 'Invalid: % % %', rec.first_name, rec.last_name, rec.phone;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
""")
cur.execute("""
CREATE OR REPLACE FUNCTION get_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, first_name VARCHAR, last_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook
    ORDER BY id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
""")
cur.execute("""
CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value OR last_name = p_value OR phone = p_value;
END;
$$ LANGUAGE plpgsql;
""")
def add_user():
    f=input("First name: ")
    l=input("Last name: ")
    p=input("Phone: ")
    cur.execute("CALL insert_or_update(%s, %s, %s)", (f, l, p))
    print("User added/updated")
def add_many():
    n=int(input("How many users to add? "))
    cur.execute("DELETE FROM temp_users")
    for _ in range(n):
        f=input("First name: ")
        l=input("Last name: ")
        p=input("Phone: ")
        cur.execute("INSERT INTO temp_users VALUES (%s,%s,%s)", (f,l,p))
    cur.execute("CALL insert_many()")
def search():
    pattern=input("Pattern: ")
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)
def paginate():
    limit=int(input("Limit: "))
    offset=int(input("Offset: "))
    cur.execute("SELECT * FROM get_paginated(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)
def delete():
    val=input("Name, surname, or phone to delete: ")
    cur.execute("CALL delete_user(%s)",(val,))
    print("Deleted")
def show_all():
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows =cur.fetchall()
    if not rows:
        print("Table is empty")
    for row in rows:
        print(row)
while True:
    print("\nMENU")
    print("1 - Add/Update user")
    print("2 - Add many users")
    print("3 - Search")
    print("4 - Paginate")
    print("5 - Delete")
    print("6 - Show all users")
    print("0 - Exit")
    choice=input(">> ")
    if choice=="1":
        add_user()
    elif choice=="2":
        add_many()
    elif choice=="3":
        search()
    elif choice=="4":
        paginate()
    elif choice=="5":
        delete()
    elif choice=="6":
        show_all()
    elif choice=="0":
        break
cur.close()
conn.close()