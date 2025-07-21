# write a python code to enter and read into / from a given database
import sqlite3
def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn
def read_data(conn):
    """ read data from the database """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data_table")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)
# enter data / create one 
def insert_data(conn, data):
    """ insert data into the database """
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data_table (id,column1, column2) VALUES (?, ?, ?)", data)
        conn.commit()
        print("Data inserted successfully")
    except sqlite3.Error as e:
        print(e)
# main function to demonstrate the functionality
if __name__ == '__main__':
    database = "example.db"
    # create a database connection
    conn = create_connection(database)
    command = input()
    conn.execute('''CREATE TABLE IF NOT EXISTS data_table
                    (id NUMBER,
                    column1 CN NAME,
                    column2 EN NAME);''')
    if command == 'r':
        read_data(conn)
    elif command == 'i':
        data = input().split()
        insert_data(conn, (1, data[0], data[1]))