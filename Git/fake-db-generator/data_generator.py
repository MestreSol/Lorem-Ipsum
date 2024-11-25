import random
import uuid
from file_utils import load_json_file

def generate_inserts(config, num_inserts):
    inserts = []
    names = load_json_file('assets/names_list.json')["Names"]
    emails = load_json_file('assets/emails_list.json')["Emails"]
    usernames = load_json_file('assets/usernames_list.json')["UserNames"]

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