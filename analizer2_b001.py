import json
import random
import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime, date
import time
import serial

contador = 0
pedirDato = 1
enviarDatos = 0
tiempoParaLeer = 0
queMinutoLeido = -1
queMinutoLeido1 = -1
mensajeRecibido = 0
sensor_data = {'adae': 0, 'bdae': 0, 'cdae': 0}#donde se guardan los datos constantemente (Volatil)


conn = sqlite3.connect('datalog.sqlite')
cur = conn.cursor()
THINGSBOARD_HOST = 'clientes.egeo.co'
ACCESS_TOKEN = 'SSDBNI2aIyD3TkQwDM2n'
ser = serial.Serial('/dev/ttyS1', 230400, timeout = 0.1)
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)


# Crear parametros de la base de datos si no exixte
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
CREATE TABLE IF NOT EXISTS Temporales (
    nombre    TEXT UNIQUE,
    value	REAL
);
''')

cur.execute('''INSERT OR IGNORE INTO Temporales (nombre, value) 
	VALUES ( ?, ?)''', ('tempA1', 0) )
cur.execute('''INSERT OR IGNORE INTO Temporales (nombre, value) 
	VALUES ( ?, ?)''', ('tempB1', 0) )
cur.execute('''INSERT OR IGNORE INTO Temporales (nombre, value) 
	VALUES ( ?, ?)''', ('tempC1', 0) )
conn.commit()

def almacenarEnDatabase ():

	horaTomada = datetime.now().replace(year=1, second=0, microsecond=0)
	#Hacer la restar el valor anterior con el actual y guardarlo
	cur.execute('SELECT nombre, value FROM Temporales')
	rows = cur.fetchall()
	rows = dict(rows)
	print('recibido', rows)

	try:
		consumoTemporalA1 = sensor_data['adae'] - rows['tempA1']
		consumoTemporalB1 = sensor_data['bdae'] - rows['tempB1']
		consumoTemporalC1 = sensor_data['cdae'] - rows['tempC1']

		cur.execute('''INSERT OR REPLACE INTO Temporales (nombre, value) 
			VALUES ( ?, ?)''', ('tempA1', sensor_data['adae']) )
		cur.execute('''INSERT OR REPLACE INTO Temporales (nombre, value) 
			VALUES ( ?, ?)''', ('tempB1', sensor_data['bdae']) )
		cur.execute('''INSERT OR REPLACE INTO Temporales (nombre, value) 
			VALUES ( ?, ?)''', ('tempC1', sensor_data['cdae']) )
		
		cur.execute('''INSERT OR REPLACE INTO ConsumoA1 (timestampDato, value) 
			VALUES ( ?, ? )''', (horaTomada, sensor_data['adae']) )
		cur.execute('''INSERT OR REPLACE INTO ConsumoB1 (timestampDato, value) 
			VALUES ( ?, ? )''', (horaTomada, sensor_data['bdae']) )
		cur.execute('''INSERT OR REPLACE INTO ConsumoC1 (timestampDato, value) 
			VALUES ( ?, ? )''', (horaTomada, sensor_data['cdae']) )

		# print(horaTomada, sensor_data )
		enviarConsumoNube = {'consumoA1': consumoTemporalA1, 'consumoB1': consumoTemporalB1, 'consumoC1': consumoTemporalC1, 'consumoC1': consumoTemporalC1, "horaDeToma": str(horaTomada)}
		client.publish('v1/devices/me/telemetry', json.dumps(enviarConsumoNube), 1)

		# print("consumoA1", consumoTemporalA1 )
		# print("consumoB1", consumoTemporalB1 )
		# print("consumoC1", consumoTemporalC1 )

		
			# cur.execute('SELECT value FROM ConsumoA1 WHERE timestampDato = ? ', ('0001-06-16 10:09:00', ))
			# artist_id = cur.fetchone()[0]
			# print(artist_id)
		conn.commit()
	except KeyboardInterrupt:
		return
	except:
		pass

def enviarNube ():

	try:
		client.connect(THINGSBOARD_HOST, 1883, 60)
		client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
		print("Enviado a la NUBE")
	except:
		return


client.loop_start()

try:
	while True:

		leerMinuto = int(datetime.now().minute)
		if (((leerMinuto % 10) == 0) and (leerMinuto != queMinutoLeido)):
			almacenarEnDatabase ()
			queMinutoLeido = leerMinuto

		if (((leerMinuto % 1) == 0) and (leerMinuto != queMinutoLeido1) and (enviarDatos == 1)):
			enviarNube ()
			enviarDatos = 0
			queMinutoLeido1 = leerMinuto

		if time.time() >= tiempoParaLeer:
	            if mensajeRecibido == 0:
	            
	                print("pidiendo dato")
	                ser.flush()

	                if pedirDato == 1:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getADAE"}"""
	                    mensajeRecibido = 1
	                    ser.write(mensaje)
	               
	                elif pedirDato == 2:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getBDAE"}""" 
	                    mensajeRecibido = 1 
	                    ser.write(mensaje)

	                elif pedirDato == 3:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getCDAE"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)
	                

	                elif pedirDato == 4:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getFrequency"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 5:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getPowerA"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 6:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getPowerB"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 7:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getPowerC"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 8:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getVoltageA"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 9:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getVoltageB"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 10:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getVoltageC"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 11:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getCurrentA"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 12:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getCurrentB"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 13:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getCurrentC"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 14:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getTemp"}""" 
	                    mensajeRecibido = 1
	                    ser.write(mensaje)

	                elif pedirDato == 15:
	                    #print ("pedirDato???", pedirDato)
	                    mensaje = b"""{"chip": "1","operation": "getPowerT"}""" 
	                    mensajeRecibido = 1
	                    contador = 1
	                    ser.write(mensaje)

	                if contador == 1:
	                    tiempoParaLeer = time.time() + 35 #cada cuanto se piden los datos del PIC
	                    contador = 0

		if ser.inWaiting():
		            recibidoSerial = ser.readline()
		            print ("Respuesta recibida: ", recibidoSerial)
		            recibidoSerial = recibidoSerial.decode("utf-8")
		            data = json.loads(recibidoSerial)
		            pedirDato = pedirDato + 1
		            if pedirDato >= 16:
		                pedirDato = 1
		                enviarDatos = 1

		            if data['operation'] == "getADAE":
		                sensor_data['adae'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getBDAE":
		                sensor_data['bdae'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getCDAE":
		                sensor_data['cdae'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getFrequency":
		                sensor_data['frecuencia'] = (data['value']/100.0)
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getPowerA":
		                sensor_data['potenciaA'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getPowerB":
		                sensor_data['potenciaB'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getPowerC":
		                sensor_data['potenciaC'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getVoltageA":
		                sensor_data['voltajeA'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getVoltageB":
		                sensor_data['voltajeB'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getVoltageC":
		                sensor_data['voltajeC'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getCurrentA":
		                sensor_data['corrienteA'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getCurrentB":
		                sensor_data['corrienteB'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getCurrentC":
		                sensor_data['corrienteC'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getTemp":
		                sensor_data['temperature'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)

		            elif data['operation'] == "getPowerT":
		                sensor_data['potenciaTotal'] = data['value']
		                mensajeRecibido = 0
		                #print(sensor_data)
except KeyboardInterrupt:
	return
except:
	pass

client.loop_stop()
client.disconnect()
