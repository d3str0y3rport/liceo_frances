import time
import serial
import json

mensajeBandera = False
mensajeRecibido = ""

ser = serial.Serial('/dev/ttyS1', 230400, timeout = 0.1)


while True:
	ser.write(b"""{"chip": "1","operation": "getTemp"}""")
	ser.flush()

if ser.in_waiting: 
    print ("recibido del serial: " , ser.readline())
    

