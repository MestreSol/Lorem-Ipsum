from mysql.connector import Error, connect

def connect_to_db(inserts, db_path=None):
    def submit():
        try:
            connection = connect(
                host='localhost',
                database='your_database',
                user='your_username',
                password='your_password'  # Add your password here
            )
            cursor = connection.cursor()
            for insert in inserts:
                cursor.execute(insert)
            connection.commit()
        except Error as e:
            print(f"Database error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            if db_path is None:
                root.destroy()

    if db_path is None:
        from tkinter import Tk, Label, Entry, Button
        root = Tk()
        root.title("Database Connection")
        Label(root, text="Database Path:").grid(row=0)
        entry = Entry(root)
        entry.grid(row=0, column=1)
        Button(root, text="Submit", command=submit).grid(row=1, columnspan=2)
        root.mainloop()
    else:
        submit()

def create_tables(config, connection):
    cursor = connection.cursor()
    for table, columns in config.items():
        create_table = f"CREATE TABLE IF NOT EXISTS {table} ("
        for key, value in columns.items():
            if value == 'GUID':
                value = 'VARCHAR(36)'
            elif value == 'String':
                value = 'VARCHAR(255)'
            elif value == 'Int':
                value = 'INT'
            elif value == 'Float':
                value = 'FLOAT'
            elif value == 'Bool':
                value = 'BOOLEAN'
            create_table += f"{key} {value}, "
        create_table = create_table[:-2] + ");"
        cursor.execute(create_table)
    cursor.close()