import os
import sys
import time
from file_utils import load_config, load_db_path
from data_generator import generate_inserts
from db_utils import connect_to_db, create_tables
from mysql.connector import connect, Error

def generate_and_insert_continuously(config, delay):
    print(f"Generating and inserting data every {delay}ms")
    print(f"Generate tables: {config.keys()}")
    db_path = load_db_path()

    connection_config_path = os.path.join('config', 'connection.json')
    connection_config = load_config(connection_config_path)
    connection = connect(
        host=connection_config['host'],
        database=connection_config['database'],
        user=connection_config['user'],
        password=connection_config.get('password')
    )
    try:
        print("Trying to connect to MySQL...")
        if connection.is_connected():
            print("Connected to MySQL")
            create_tables(config, connection)
            cursor = connection.cursor()
            while True:
                inserts = generate_inserts(config, 1)
                for insert in inserts:
                    cursor.execute(insert)
                connection.commit()
                time.sleep(delay / 1000.0)
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    config_path = os.path.join('config', 'db.json')
    config = load_config(config_path)
    num_inserts = int(sys.argv[sys.argv.index('--qtd') + 1]) if '--qtd' in sys.argv else 10
    print(f"Generating {num_inserts} inserts")
    if num_inserts == 0:
        delay = int(sys.argv[sys.argv.index('--delay') + 1]) if '--delay' in sys.argv else 1000
        generate_and_insert_continuously(config, delay)
    else:
        inserts = generate_inserts(config, num_inserts)
        db_path = load_db_path()
        if db_path or (len(sys.argv) > 1 and sys.argv[1] == '--connect'):
            connect_to_db(inserts, db_path)
        else:
            with open('output.sql', 'w') as file:
                for insert in inserts:
                    file.write(insert + '\n')
            print(f"Generated {len(inserts)} inserts")