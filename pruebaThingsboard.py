import os
import time
import sys
import serial
import paho.mqtt.client as mqtt
import json
import random

THINGSBOARD_HOST = 'clientes.egeo.co'
ACCESS_TOKEN = 'y5XV402DDK8TeQnpxBoA'
ser = serial.Serial('/dev/ttyS1', 230400, timeout = 0.05, write_timeout = 0.05)

pedirDato = 1
mensajeRecibido = 0
enviarDatos = 0
tiempoParaLeer = 0

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

#client.loop_start()

try:
    while True:

        if mensajeRecibido == 0:
            if time.time() >= tiempoParaLeer:
            
                print("pidiendo dato")

                if pedirDato == 1:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getTemp"}"""
                    mensajeRecibido = 1
                    ser.write(mensaje)
               
                elif pedirDato == 2:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getADAE"}""" 
                    mensajeRecibido = 1 
                    ser.write(mensaje)

                elif pedirDato == 3:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getFrequency"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 4:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getTemp"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                time.sleep(0.5)
                tiempoParaLeer = time.time() + 5

            
        if ser.inWaiting():
            recibidoSerial = ser.readline()
            print ("Respuesta recibida: ", recibidoSerial)
            recibidoSerial = recibidoSerial.decode("utf-8")
            data = json.loads(recibidoSerial)
            print (json.dumps(data, indent=4))
            pedirDato = pedirDato + 1
            if pedirDato >= 4:
                pedirDato = 1
                enviarDatos = 1

            if data['operation'] == "getTemp":
                print('Temperatura:', data['value'])
                temperatura = data['value']
                mensajeRecibido = 0
                sensor_data = {'temperature': temperatura}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                print("temp enviada")

            elif data['operation'] == "getADAE":
                print('Acumulado:', data['value'])
                mensajeRecibido = 0
                sensor_data = {'acumuladoActivoDirecto': data['value']}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                print("ADAE enviada")

            elif data['operation'] == "getFrequency":
                print('Frecuencia:', data['value'])
                voltaje = data['value']
                mensajeRecibido = 0
                sensor_data = {'voltaje': data['value']}
                print("Frecuencia enviada")


        # if enviarDatos == 1 :
        #     humedad = random.randint(1,101)
        #     potencia = random.randint(0,400)
        #     acumuladoAI = acumuladoAI + random.randint(1,10)
        #     corriente = random.randint(1,101)
        #     sensor_data = {'temperature': temperatura, 'humidity': humedad, 'acumuladoActivoDirecto': acumuladoAD, 'acumuladoActivoInverso': acumuladoAI, 'potencia': potencia, 'voltaje': voltaje, 'corriente': corriente}
        #     # Sending humidity and temperature data to ThingsBoard
        #     client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        #     print ("enviando")
        #     enviarDatos = 0
        

except KeyboardInterrupt:
    pass

#client.loop_stop()
client.disconnect()