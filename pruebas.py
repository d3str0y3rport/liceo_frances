import time
import serial
import json

mensajeBandera = False
mensajeRecibido = ""
leido = 1

ser = serial.Serial('/dev/ttyS1', 230400, timeout = 0.1)


while True:
	if leido = 1:
		ser.write(b"""{"chip": "1","operation": "getTemp"}""")
		print("enviado")
		ser.flush()

	if ser.in_waiting:
		mensajerecibido = ser.readline()
		print ("recibido del serial: ", mensajerecibido)
		leido = 1
    

