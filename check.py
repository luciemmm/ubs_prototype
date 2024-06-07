import sqlite3
def print_table_schema():
    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
    c = conn.cursor()
    c.execute("PRAGMA table_info(surveys)")
    schema = c.fetchall()
    print(schema)
    conn.close()

print_table_schema()


def list_tables():
    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    conn.close()
    print(tables)

list_tables()

import sqlite3

def print_table_contents():
    # Ensure the path to your database is correct
    conn = sqlite3.connect('/Users/moemmyat/Downloads/ubs_prototype/survey.db')
    c = conn.cursor()
    
    # Execute a SELECT query to retrieve all rows from the 'users' table
    c.execute("SELECT * FROM questions")
    rows = c.fetchall()
    print(rows)
    # Print the results
    for row in rows:
        print(row)
    
    # Close the connection
    conn.close()

print_table_contents()