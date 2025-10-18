import sqlite3
import os

DB_TEMPLATE = "squirrel_db_template.db"


if os.path.exists(DB_TEMPLATE):
    os.remove(DB_TEMPLATE)


connection = sqlite3.connect(DB_TEMPLATE)
cursor = connection.cursor()


cursor.execute("""
    CREATE TABLE squirrels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        size TEXT NOT NULL
    )
""")

connection.commit()
connection.close()

print(f"Created!")
print("Run tests with: pytest --spec")