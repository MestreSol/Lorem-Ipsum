import json
import os
import random
import sqlite3
import uuid
import sys
from tkinter import Tk, Label, Entry, Button

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def generate_inserts(config, num_inserts):
    inserts = []
    # Load all JSON files once
    with open('assets/names_list.json', 'r') as file:
        names = json.load(file)["Names"]
    print(f"Loaded {len(names)} names")
    with open('assets/emails_list.json', 'r') as file:
        emails = json.load(file)["Emails"]
    print(f"Loaded {len(emails)} emails")
    with open('assets/usernames_list.json', 'r') as file:
        usernames = json.load(file)["UserNames"]
    print(f"Loaded {len(usernames)} usernames")

    for _ in range(num_inserts):
        for table, columns in config.items():
            insert = f"INSERT INTO {table} ("
            values = "VALUES ("
            for key, value in columns.items():
                insert += f"{key}, "
                if value == 'GUID':
                    values += f"'{uuid.uuid4()}', "  # Using uuid4 to generate a GUID
                elif value == 'String':
                    if key == 'Name':
                        values += f"'{random.choice(names)}', "
                    elif key == 'Email':
                        values += f"'{random.choice(emails)}', "
                    elif key == 'Password':
                        values += f"'{random.choice(usernames)}', "
                    else:
                        values += f"'{random.choice(usernames)}', "  # Default for other strings
                elif value == 'Int':
                    values += f"{random.randint(0, 1000)}, "
                elif value == 'Float':
                    values += f"{random.uniform(0, 1000):.2f}, "
                elif value == 'Bool':
                    values += f"{random.choice([0, 1])}, "
            insert = insert[:-2] + ") " + values[:-2] + ");"
            inserts.append(insert)
    return inserts

def connect_to_db():
    def submit():
        conn = sqlite3.connect(entry.get())
        cursor = conn.cursor()
        for insert in inserts:
            cursor.execute(insert)
        conn.commit()
        conn.close()
        root.destroy()

    root = Tk()
    root.title("Database Connection")
    Label(root, text="Database Path:").grid(row=0)
    entry = Entry(root)
    entry.grid(row=0, column=1)
    Button(root, text="Submit", command=submit).grid(row=1, columnspan=2)
    root.mainloop()

if __name__ == "__main__":
    config_path = os.path.join('config', 'db.json')
    config = load_config(config_path)
    if '--qtd' in sys.argv:
        num_inserts = int(sys.argv[sys.argv.index('--qtd') + 1])
    else:
        num_inserts = 10  # Default value if not provided
    inserts = generate_inserts(config, num_inserts)

    if len(sys.argv) > 1 and sys.argv[1] == '--connect':
        connect_to_db()
    else:
        for insert in inserts:
            print(insert)
        # Output the inserts to a file
        with open('output.sql', 'w') as file:
            for insert in inserts:
                file.write(insert + '\n')
        print(f"Generated {len(inserts)} inserts")
