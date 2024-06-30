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

# Usage
database_name = '/Users/moemmyat/Downloads/ubs_prototype/forum.db'  # Update this to your database file
drop_all_tables(database_name)

def create_db():
    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/forum.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            profile_image_url TEXT,
            fun_fact TEXT,
            gender TEXT,
            hobbies TEXT
        )
    ''')
    c.execute("""CREATE TABLE IF NOT EXISTS registrations (
                    event_id integer NOT NULL,
                    user_name text NOT NULL,
                    user_email text NOT NULL,
                    FOREIGN KEY (event_id) REFERENCES events (id)
                )""")
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user TEXT NOT NULL,
            profile_image_url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            comment TEXT NOT NULL,
            user TEXT NOT NULL,
            profile_image_url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS upvotes (
            id INTEGER PRIMARY KEY,
            post_id INTEGER,
            user TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id)
        )
    ''')

    conn.commit()
    conn.close()

create_db()


