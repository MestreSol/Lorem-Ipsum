import json
import os
import random
import sqlite3
import sys
from tkinter import Tk, Label, Entry, Button

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def generate_inserts(config, num_inserts):
    inserts = []
    # transform all types on the config to a list in smallcase
    for key in config:
        config[key] = [x.lower() for x in config[key]]
    # Load all JSON files once
    with open('assets/names_list.json', 'r') as file:
        names = json.load(file)["Names"]
    print(f"Loaded {len(names)} names")
    with open('assets/emails_list.json', 'r') as file:
        emails = json.load(file)["Emails"]
    print(f"Loaded {len(emails)} emails")
    with open('assets/phones_list.json', 'r') as file:
        phones = json.load(file)["Phones"]
    print(f"Loaded {len(phones)} phones")
    with open('assets/addresses_list.json', 'r') as file:
        addresses = json.load(file)["Addresses"]
    print(f"Loaded {len(addresses)} addresses")
    with open('assets/cities_list.json', 'r') as file:
        cities = json.load(file)["Cities"]
    print(f"Loaded {len(cities)} cities")
    with open('assets/states_list.json', 'r') as file:
        states = json.load(file)["States"]
    print(f"Loaded {len(states)} states")
    with open('assets/zips_list.json', 'r') as file:
        zips = json.load(file)["ZipCodes"]
    print(f"Loaded {len(zips)} zips")
    with open('assets/countries_list.json', 'r') as file:
        countries = json.load(file)["Countries"]
    print(f"Loaded {len(countries)} countries")
    with open('assets/ustates_list.json', 'r') as file:
        ustates = json.load(file)["UState"]
    print(f"Loaded {len(ustates)} ustates")
    with open('assets/usernames_list.json', 'r') as file:
        usernames = json.load(file)["UserNames"]
    print(f"Loaded {len(usernames)} usernames")

    for _ in range(num_inserts):
        insert = "INSERT INTO table_name ("
        values = "VALUES ("
        for key in config:
            insert += f"{key}, "
            if config[key][0] == 'int':
                values += f"{random.randint(int(config[key][1]), int(config[key][2]))}, "
            elif config[key][0] == 'float':
                values += f"{random.uniform(float(config[key][1]), float(config[key][2]))}, "
            elif config[key][0] == 'str':
                values += f"'{random.choice(config[key][1:])}', "
            elif config[key][0] == 'bool':
                values += f"{random.choice([True, False])}, "
            elif config[key][0] == 'date':
                values += f"'{random.randint(int(config[key][1]), int(config[key][2]))}-{random.randint(1, 12)}-{random.randint(1, 28)}', "
            elif config[key][0] == 'name':
                values += f"'{random.choice(names)}', "
            elif config[key][0] == 'email':
                values += f"'{random.choice(emails)}', "
            elif config[key][0] == 'phone':
                values += f"'{random.choice(phones)}', "
            elif config[key][0] == 'address':
                values += f"'{random.choice(addresses)}', "
            elif config[key][0] == 'city':
                values += f"'{random.choice(cities)}', "
            elif config[key][0] == 'state':
                values += f"'{random.choice(states)}', "
            elif config[key][0] == 'zip':
                values += f"'{random.choice(zips)}', "
            elif config[key][0] == 'country':
                values += f"'{random.choice(countries)}', "
            elif config[key][0] == 'ustate':
                values += f"'{random.choice(ustates)}', "
            elif config[key][0] == 'username':
                values += f"'{random.choice(usernames)}', "
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
