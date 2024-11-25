import json
import os

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def load_db_path():
    con_path = os.path.join('config', 'connection.json')
    if os.path.exists(con_path):
        with open(con_path, 'r') as file:
            return json.load(file).get('db_path')
    return None