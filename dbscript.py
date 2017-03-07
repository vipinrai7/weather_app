import csv
import sqlite3

conn = sqlite3.connect('test.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS test""")
cur.execute("""CREATE TABLE test
            (id integer, temp float, humidity float)""")

cur.execute("""INSERT INTO test VALUES (1,23.5,45.7)""")

conn.commit()
conn.close()
