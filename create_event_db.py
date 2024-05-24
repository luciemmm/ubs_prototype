import sqlite3

def drop_all_tables(database_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    # Retrieve a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Drop each table
    for table_name in tables:
        try:
            cursor.execute(f"DROP TABLE {table_name[0]}")
            print(f"Dropped table {table_name[0]}")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()

database_name = '/Users/moemmyat/Downloads/ubs_prototype/calendar.db'  # Update this to your database file
drop_all_tables(database_name)

def create_db():
    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/calendar.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS events (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        start text NOT NULL,
                                        end text NOT NULL,
                                        avenue text
                )"""
                )
    conn.commit()
    conn.close()

create_db()