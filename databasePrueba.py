import sqlite3
from datetime import datetime, date


conn = sqlite3.connect('datalog.sqlite')
cur = conn.cursor()

tiempoLeido = 0
queMinutoLeido = -1

horaTomada = datetime.now().replace(year=1, second=0, microsecond=0)

vector = [1,2,3]

print(horaTomada)

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

print(vector)
while True:

	leerMinuto = int(datetime.now().minute)

	if (((leerMinuto % 1) == 0) and (leerMinuto != queMinutoLeido)):

		horaTomada = datetime.now().replace(year=1, second=0, microsecond=0)

		cur.execute('''INSERT OR REPLACE INTO ConsumoA1 (timestampDato, value) 
			VALUES ( ?, ?)''', ( horaTomada, 1.232) )

		# cur.execute('''INSERT OR REPLACE INTO ConsumoA1 (timestampDato, value) 
		# 	VALUES ( ?, ? )''', ( 'Pablo', 11) )
		queMinutoLeido = leerMinuto
		print("hi")

		# cur.execute('SELECT value FROM ConsumoA1 WHERE timestampDato = ? ', ('0001-06-16 10:09:00', ))
		# artist_id = cur.fetchone()[0]
		# print(artist_id)


		tiempoLeido = datetime.now().minute + 1
		conn.commit()




