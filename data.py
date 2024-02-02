import sqlite3

connection = sqlite3.connect('bookme.db')

#command = "SELECT name FROM sqlite_master WHERE type = 'table'"
command = "SELECT * FROM apidata"
result = connection.execute(command)

for row in result:
    key = row[0]
    host = row[1]
    print(row[0])