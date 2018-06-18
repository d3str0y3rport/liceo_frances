import sqlite3
import json
from datetime import datetime, date


conn = sqlite3.connect('testDatalog.sqlite')
cur = conn.cursor()

tiempoLeido = 0
queMinutoLeido = -1


# Make some fresh tables using executescript()
cur.executescript('''
CREATE TABLE IF NOT EXISTS ConsumoA1 (
    timestampDato    TEXT UNIQUE,
    value 	REAL
);
CREATE TABLE IF NOT EXISTS ConsumoB1 (
    timestampDato    TEXT UNIQUE,
    value 	REAL
);
CREATE TABLE IF NOT EXISTS ConsumoC1 (
    timestampDato    TEXT UNIQUE,
    value	REAL
);
''')


cur.execute("SELECT * FROM ConsumoA1")
rows = cur.fetchall()

print('recibido', dict(rows))
	

# cur.execute('''INSERT OR REPLACE INTO ConsumoA1 (timestampDato, value) 
# 	VALUES ( ?, ?)''', ( '0001-06-18 20:33:00', 4.232) )

# cur.execute('''INSERT OR REPLACE INTO ConsumoA1 (timestampDato, value) 
# 	VALUES ( ?, ? )''', ( 'Pablo', 11) )
print("hi")

# cur.execute('SELECT value FROM ConsumoA1 WHERE timestampDato = ? ', ('0001-06-16 10:09:00', ))
# artist_id = cur.fetchone()[0]
# print(artist_id)
conn.commit()