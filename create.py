import sqlite3

# Connect to the database (it will create the database if it doesn't exist)
conn = sqlite3.connect('user_network.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        domain TEXT CHECK(domain IN ('software', 'analytics', 'semiconductor')) NOT NULL
    )
''')

# Insert sample data (10 users)
cursor.executemany('''
    INSERT INTO users (name, domain) VALUES (?, ?)
''', [
    ('Alice Smith', 'software'),
    ('Bob Johnson', 'analytics'),
    ('Charlie Brown', 'semiconductor'),
    ('David Williams', 'software'),
    ('Eve Davis', 'analytics'),
    ('Frank Miller', 'semiconductor'),
    ('Grace Wilson', 'software'),
    ('Hank Moore', 'analytics'),
    ('Ivy Taylor', 'semiconductor'),
    ('Jack Anderson', 'software')
])

# Commit changes and close the connection
conn.commit()
conn.close()

print("Users table created and populated with sample data.")
