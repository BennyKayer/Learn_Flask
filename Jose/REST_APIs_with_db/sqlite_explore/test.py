# SQLite is built in
import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

# user = (1, "pawel", "asdf")
insert_query = "INSERT INTO users VALUES(?, ?, ?)"
# cursor.execute(insert_query, user)

users = [(1, "pawel", "asdf"), (2, "rolf", "xyz"), (3, "edyy", "132")]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
