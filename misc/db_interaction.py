import sqlite3

# Replace 'db.sqlite3' with your actual database file name if different
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(tables)

# Drop a specific table
cursor.execute("DROP TABLE IF EXISTS model_practice_person;")
conn.commit()

conn.close()