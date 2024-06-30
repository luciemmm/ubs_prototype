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

database_name = '/Users/moemmyat/Downloads/ubs_prototype/assessment.db'  # Update this to your database file
drop_all_tables(database_name)

def create_db():
    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/assessment.db')
    c = conn.cursor()
    # Create a table for surveys
    c.execute("""
        CREATE TABLE IF NOT EXISTS surveys (
            survey_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            reminder TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            survey_id INTEGER,
            question TEXT NOT NULL,
            option1 TEXT,
            score1 INTEGER,
            option2 TEXT,
            score2 INTEGER,
            option3 TEXT,
            score3 INTEGER,
            option4 TEXT,
            score4 INTEGER,
            FOREIGN KEY (survey_id) REFERENCES surveys(survey_id)
        )
    """)
    conn.commit()
    conn.close()

create_db()