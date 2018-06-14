import os
import time
import sys
import serial
import paho.mqtt.client as mqtt
import json
import random

THINGSBOARD_HOST = 'clientes.egeo.co'
ACCESS_TOKEN = 'y5XV402DDK8TeQnpxBoA'
ser = serial.Serial('/dev/ttyS1', 230400, timeout = 0.05)

pedirDato = 1
mensajeRecibido = 0
enviarDatos = 0
tiempoParaLeer = 0
contador = 0

sensor_data = {'frecuencia': 0, 'temperature': 0, 'totalPower': 0,'adae': 0, 'bdae': 0, 'cdae': 0, 'potenciaA': 0, 'potenciaB': 0, 'potenciaC': 0, 'voltaje': 0, 'corrienteA': 0, 'corrienteB': 0, 'corrienteC': 0}


next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

#client.loop_start()

try:
    while True:

        if time.time() >= tiempoParaLeer:
            if mensajeRecibido == 0:
            
                print("pidiendo dato")
                ser.flush()

                if pedirDato == 1:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getADAE"}"""
                    mensajeRecibido = 1
                    ser.write(mensaje)
               
                elif pedirDato == 2:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getBDAE"}""" 
                    mensajeRecibido = 1 
                    ser.write(mensaje)

                elif pedirDato == 3:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getCDAE"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)
                    contador = 1

                elif pedirDato == 4:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getFrequency"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 5:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getPowerA"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 6:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getPowerB"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 7:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getPowerC"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 8:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getVoltageA"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 9:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getCurrentA"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 10:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getCurrentB"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 11:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getCurrentC"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)

                elif pedirDato == 12:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getTemp"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)getPowerT

                elif pedirDato == 13:
                    print ("pedirDato???", pedirDato)
                    mensaje = b"""{"chip": "1","operation": "getPowerT"}""" 
                    mensajeRecibido = 1
                    ser.write(mensaje)


                if contador == 1:
                    tiempoParaLeer = time.time() + 5
                    contador = 0

                time.sleep(1)
            
            
        if ser.inWaiting():
            recibidoSerial = ser.readline()
            print ("Respuesta recibida: ", recibidoSerial)
            recibidoSerial = recibidoSerial.decode("utf-8")
            data = json.loads(recibidoSerial)
            pedirDato = pedirDato + 1
            if pedirDato >= 14:
                pedirDato = 1
                enviarDatos = 1

            if data['operation'] == "getADAE":
                value = data['value']
                sensor_data = {'adae': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)


            elif data['operation'] == "getBDAE":
                value = data['value']
                sensor_data = {'bdae': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getCDAE":
                value = data['value']
                sensor_data = {'cdae': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getFrequency":
                value = data['value']
                value = value/100.0
                sensor_data = {'frecuencia': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getPowerA":
                value = data['value']
                sensor_data = {'potenciaA': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getPowerB":
                value = data['value']
                sensor_data = {'potenciaB': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getPowerC":
                value = data['value']
                sensor_data = {'potenciaC': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getVoltageA":
                value = data['value']
                sensor_data = {'voltaje': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getCurrentA":
                value = data['value']
                sensor_data = {'corrienteA': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getCurrentB":
                value = data['value']
                sensor_data = {'corrienteB': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getCurrentC":
                value = data['value']
                sensor_data = {'corrienteC': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getTemp":
                value = data['value']
                sensor_data = {'temperature': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)

            elif data['operation'] == "getPowerT":
                value = data['value']
                sensor_data = {'totalPower': value}
                client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
                mensajeRecibido = 0
                print(value)


        

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