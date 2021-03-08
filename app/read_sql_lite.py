import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("players_stats_cache.sqlite")

cur = con.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT * FROM responses;'):
    print(row)

# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute('SELECT * FROM urls;'):
    print(row)

# Be sure to close the connection
con.close()