import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM hanviet")
rows = cursor.fetchall()
dict_hv = dict((row[0], row[1]) for row in rows)
# for row in rows:
#     print(row[0])
    #print(row[1])
print(dict_hv)
conn.close()