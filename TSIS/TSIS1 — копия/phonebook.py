import json, csv
from connect import connect

conn = connect()
cur = conn.cursor()
PAGE_SIZE = 5


def get_or_create_group(name):
    cur.execute("SELECT id FROM groups WHERE name=%s", (name,))
    g = cur.fetchone()
    if g:
        return g[0]
    cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (name,))
    return cur.fetchone()[0]


def add_contact():
    first_name = input("Name: ")
    last_name = input("Last name: ")
    email = input("Email: ") or None
    birthday = input("Birthday (YYYY-MM-DD): ") or None
    group = input("Group: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    gid = get_or_create_group(group)
    cur.execute("""
        INSERT INTO contacts (first_name, last_name, email, birthday, group_id, phone, phone_type, group_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (first_name, last_name, email, birthday, gid, phone, phone_type, group))
    
    cid = cur.fetchone()[0]
    conn.commit()
    print(f"✅ Контакт {first_name} {last_name} добавлен с ID: {cid}")


def add_phone():
    name, phone, ptype = input("Name: "), input("Phone: "), input("Type: ")
    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
    conn.commit()


def show_all():
    # Исправленный запрос - убран GROUP BY c.id, g.name и добавлено корректное объединение
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name,
               STRING_AGG(p.phone || '(' || COALESCE(p.type,'?') || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.id
    """)
    results = cur.fetchall()
    if not results:
        print("No contacts found.")
        return
    
    print("\n" + "="*80)
    for r in results:
        print(f"Name: {r[0]}")
        print(f"Email: {r[1] if r[1] else 'N/A'}")
        print(f"Birthday: {r[2] if r[2] else 'N/A'}")
        print(f"Group: {r[3] if r[3] else 'No group'}")
        print(f"Phones: {r[4] if r[4] else 'No phones'}")
        print("-"*40)


def search():
    try:
        query = input("Query: ")
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        results = cur.fetchall()
        if not results:
            print("No results found.")
            return
        
        print("\n" + "="*80)
        for r in results:
            print(f"Name: {r[0]}, Email: {r[1]}, Phone: {r[2]}, Type: {r[3]}, Group: {r[4]}")
    except Exception as e:
        print(f"Search error: {e}")


def filter_by_group():
    group_name = input("Group: ")
    cur.execute("""
        SELECT c.name, c.email, STRING_AGG(p.phone, ', ')
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name=%s 
        GROUP BY c.id, c.name, c.email
    """, (group_name,))
    results = cur.fetchall()
    if not results:
        print(f"No contacts in group '{group_name}'")
        return
    
    print(f"\n=== Contacts in group '{group_name}' ===")
    for r in results:
        print(f"Name: {r[0]}, Email: {r[1]}, Phones: {r[2] if r[2] else 'No phones'}")


def search_by_email():
    keyword = input("Email keyword: ")
    cur.execute(
        "SELECT name, email FROM contacts WHERE email ILIKE %s",
        (f"%{keyword}%",)
    )
    results = cur.fetchall()
    if not results:
        print("No contacts found with that email pattern.")
        return
    
    for r in results:
        print(f"Name: {r[0]}, Email: {r[1]}")


def sort_filter():
    g = input("Group (blank=all): ")
    sort_type = input("Sort (name/birthday/date): ").lower()
    
    sort_map = {"name": "c.name", "birthday": "c.birthday", "date": "c.created_at"}
    sort = sort_map.get(sort_type, "c.name")
    
    q = """SELECT c.name, c.email, c.birthday, g.name 
           FROM contacts c 
           LEFT JOIN groups g ON c.group_id = g.id"""
    params = []
    
    if g:
        q += " WHERE g.name = %s"
        params.append(g)
    
    cur.execute(q + f" ORDER BY {sort}", params)
    results = cur.fetchall()
    
    if not results:
        print("No contacts found.")
        return
    
    print("\n" + "="*80)
    for r in results:
        print(f"Name: {r[0]}, Email: {r[1]}, Birthday: {r[2]}, Group: {r[3] if r[3] else 'None'}")


def pagination():
    page = 0
    while True:
        cur.execute("""
            SELECT c.name, c.email, c.birthday, g.name 
            FROM contacts c 
            LEFT JOIN groups g ON c.group_id = g.id 
            ORDER BY c.id 
            LIMIT %s OFFSET %s
        """, (PAGE_SIZE, page * PAGE_SIZE))
        rows = cur.fetchall()
        
        if not rows and page == 0:
            print("No contacts found.")
            break
            
        print(f"\n-- Page {page+1} --")
        for r in rows:
            print(f"Name: {r[0]}, Email: {r[1]}, Birthday: {r[2]}, Group: {r[3] if r[3] else 'None'}")
        
        cmd = input("next/prev/quit: ").lower()
        if cmd == "next" and rows:
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        elif cmd == "quit":
            break


def move_to_group():
    name = input("Name: ")
    group = input("Group: ")
    cur.execute("CALL move_to_group(%s,%s)", (name, group))
    conn.commit()


def delete_contact():
    name = input("Name: ")
    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
    conn.commit()
    print(f"Deleted {cur.rowcount} contact(s).")


def export_json():
    try:
        # Исправленный запрос для JSON экспорта
        cur.execute("""
            SELECT 
                c.name, 
                c.email, 
                c.birthday::TEXT, 
                g.name as group_name,
                COALESCE(
                    (SELECT JSON_AGG(JSON_BUILD_OBJECT('phone', p.phone, 'type', p.type))
                     FROM phones p 
                     WHERE p.contact_id = c.id),
                    '[]'::json
                ) as phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
        """)
        
        results = cur.fetchall()
        data = []
        for r in results:
            contact = {
                "name": r[0],
                "email": r[1],
                "birthday": r[2],
                "group": r[3],
                "phones": r[4] if r[4] else []
            }
            data.append(contact)
        
        with open("contacts.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Exported {len(data)} contacts to contacts.json")
    except Exception as e:
        print(f"Export error: {e}")


def import_json():
    try:
        filename = input("File (contacts.json): ") or "contacts.json"
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return

    for item in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (item["name"],))
        existing = cur.fetchone()
        
        if existing:
            choice = input(f"{item['name']} exists — skip/overwrite? (s/o): ").lower()
            if choice != "o":
                continue
            cur.execute("DELETE FROM contacts WHERE id=%s", (existing[0],))

        gid = get_or_create_group(item.get("group")) if item.get("group") else None
        cur.execute(
            "INSERT INTO contacts(name, email, birthday, group_id) VALUES(%s, %s, %s, %s) RETURNING id",
            (item["name"], item.get("email"), item.get("birthday"), gid)
        )
        cid = cur.fetchone()[0]
        
        for p in item.get("phones", []):
            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES(%s, %s, %s)", 
                (cid, p.get("phone"), p.get("type", "mobile"))
            )
    
    conn.commit()
    print("Import done.")


def import_csv():
    import traceback
    
    try:
        filename = input("CSV file (contacts.csv): ") or "contacts.csv"

        with open(filename, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            print("CSV columns detected:", reader.fieldnames)  # 👈 покажет заголовки CSV

            for row in reader:
                # --- 1. Определяем имя (поддержка 2 форматов CSV) ---
                if "name" in row:
                    full_name = row["name"]
                else:
                    first = row.get("first_name", "")
                    last = row.get("last_name", "")
                    full_name = f"{first} {last}".strip()

                if not full_name:
                    print("Skip row without name:", row)
                    continue

                # --- 2. Проверяем существует ли контакт ---
                cur.execute("SELECT id FROM contacts WHERE name=%s", (full_name,))
                if cur.fetchone():
                    print(f"Skip (exists): {full_name}")
                    continue

                # --- 3. Работа с группой ---
                group_name = row.get("group") or "Other"
                gid = get_or_create_group(group_name)

                # --- 4. Создаем контакт ---
                cur.execute(
                    """
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES(%s,%s,%s,%s) RETURNING id
                    """,
                    (
                        full_name,
                        row.get("email"),
                        row.get("birthday"),
                        gid
                    )
                )
                cid = cur.fetchone()[0]

                # --- 5. Добавляем телефон ---
                phone = row.get("phone")
                phone_type = row.get("phone_type") or row.get("type") or "mobile"

                if phone:
                    cur.execute(
                        "INSERT INTO phones(contact_id, phone, type) VALUES(%s,%s,%s)",
                        (cid, phone, phone_type)
                    )

        conn.commit()
        print("\n✅ CSV IMPORT SUCCESS")

    except FileNotFoundError:
        print("❌ File not found.")
    except Exception:
        print("\n💥 FULL ERROR TRACE:")
        traceback.print_exc()

        conn.commit()
        print("CSV import done.")

    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Import error: {e}")


MENU = {
    "1":  ("Add contact",     add_contact),
    "2":  ("Add phone",       add_phone),
    "3":  ("Show all",        show_all),
    "4":  ("Search",          search),
    "5":  ("Filter by group", filter_by_group),
    "6":  ("Search by email", search_by_email),
    "7":  ("Sort + filter",   sort_filter),
    "8":  ("Pagination",      pagination),
    "9":  ("Move to group",   move_to_group),
    "10": ("Delete",          delete_contact),
    "11": ("Export JSON",     export_json),
    "12": ("Import JSON",     import_json),
    "13": ("Import CSV",      import_csv),
}

while True:
    print("\n" + "="*40)
    print("PHONEBOOK MENU")
    print("="*40)
    for k, v in MENU.items():
        print(f"{k}. {v[0]}")
    print("0. Exit")
    print("-"*40)
    
    choice = input("> ").strip()
    
    if choice == "0":
        print("Goodbye!")
        break
    
    if choice in MENU:
        try:
            MENU[choice][1]()
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
    else:
        print("Invalid choice. Please try again.")

cur.close()
conn.close()
