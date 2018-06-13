import os
import time
import sys
import serial
import paho.mqtt.client as mqtt
import json
import random

THINGSBOARD_HOST = 'clientes.egeo.co'
ACCESS_TOKEN = 'y5XV402DDK8TeQnpxBoA'
ser = serial.Serial('/dev/ttyS1', 230400, timeout = 0.1)
# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL = 15
pedirDato = 1
mensajeRecibido = 0

temperatura =random.randint(1,101)
humedad = random.randint(1,101)
acumuladoAD = random.randint(1,101)
acumuladoAI = random.randint(1,101)


next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()

try:
    while True:

        if mensajeRecibido == 0:
            if pedirDato == 1:
                mensaje = b"""{"chip": "1","operation": "getTemp"}"""
                mensajeRecibido = 1
           
            if pedirDato == 2:
                mensaje = b"""{"chip": "1","operation": "getADAE"}""" 
                mensajeRecibido = 1  

            if pedirDato == 3:
                mensaje = b"""{"chip": "1","operation": "getFrequency"}""" 
                mensajeRecibido = 1

            if pedirDato == 4:
                mensaje = b"""{"chip": "1","operation": "getTemp"}""" 
                mensajeRecibido = 1

            ser.write(mensaje)


        if ser.in_waiting: 
            recibidoSerial = ser.readline()
            print ("Respuesta recibida: ", recibidoSerial)
            recibidoSerial = recibidoSerial.decode("utf-8")
            data = json.loads(recibidoSerial)
            print (json.dumps(data, indent=4))
            mensajeRecibido = 0
            pedirDato = pedirDato +1
            if pedirDato >= 4:
                pedirDato = 0
            if data['operation'] == "getTemp":
                print('Temperatura:', data['value'])
                temperatura = data['value']
            elif data['operation'] == "getADAE":
                print('Acumulado:', data['value'])
                acumuladoAD = data['value']
            elif data['operation'] == "getFrequency":
                print('Frecuencia:', data['value'])
                voltaje = data['value']

            else:
                temperatura = -1
                acumuladoAD = -1
        else:
            temperatura = random.randint(-50,50)
            acumuladoAD = acumuladoAD + random.randint(1,10)
            voltaje = random.randint(114,122)

        
        humedad = random.randint(1,101)
        potencia = random.randint(0,400)
        acumuladoAI = acumuladoAI + random.randint(1,10)
        corriente = random.randint(1,101)
        sensor_data = {'temperature': temperatura, 'humidity': humedad, 'acumuladoActivoDirecto': acumuladoAD, 'acumuladoActivoInverso': acumuladoAI, 'potencia': potencia, 'voltaje': voltaje, 'corriente': corriente}
        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        print ("enviando")

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()