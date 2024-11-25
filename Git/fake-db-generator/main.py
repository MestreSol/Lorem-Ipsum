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

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_inserts(config, num_inserts):
    inserts = []
    names = load_json_file('assets/names_list.json')["Names"]
    emails = load_json_file('assets/emails_list.json')["Emails"]
    usernames = load_json_file('assets/usernames_list.json')["UserNames"]

    print(f"Loaded {len(names)} names")
    print(f"Loaded {len(emails)} emails")
    print(f"Loaded {len(usernames)} usernames")

    for _ in range(num_inserts):
        for table, columns in config.items():
            insert = f"INSERT INTO {table} ("
            values = "VALUES ("
            for key, value in columns.items():
                insert += f"{key}, "
                if value == 'GUID':
                    values += f"'{uuid.uuid4()}', "
                elif value == 'String':
                    values += f"'{random.choice(names if key == 'Name' else emails if key == 'Email' else usernames)}', "
                elif value == 'Int':
                    values += f"{random.randint(0, 1000)}, "
                elif value == 'Float':
                    values += f"{random.uniform(0, 1000):.2f}, "
                elif value == 'Bool':
                    values += f"{random.choice([0, 1])}, "
            insert = insert[:-2] + ") " + values[:-2] + ");"
            inserts.append(insert)
    return inserts

def connect_to_db(inserts):
    def submit():
        try:
            conn = sqlite3.connect(entry.get())
            cursor = conn.cursor()
            for insert in inserts:
                cursor.execute(insert)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
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
    num_inserts = int(sys.argv[sys.argv.index('--qtd') + 1]) if '--qtd' in sys.argv else 10
    inserts = generate_inserts(config, num_inserts)

    if len(sys.argv) > 1 and sys.argv[1] == '--connect':
        connect_to_db(inserts)
    else:
        with open('output.sql', 'w') as file:
            for insert in inserts:
                file.write(insert + '\n')
        print(f"Generated {len(inserts)} inserts")
