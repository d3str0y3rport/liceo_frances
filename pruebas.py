import time
import serial
import json

mensajeBandera = False
mensajeRecibido = ""
leido = 1

ser = serial.Serial('/dev/ttyS1', 230400, timeout = 0.1)


while True:
	if leido == 1:
		ser.write(b"""{"chip": "1","operation": "getTemp"}""")
		print("enviado", time.time())
		leido = 0
		ser.flush()

	if ser.in_waiting:
		mensajerecibido = ser.readline()
		print ("recibido del serial: ", mensajerecibido)
		print(time.time())
		leido = 1
    

