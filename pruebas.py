import json


mensaje = b"""{ "comKey":"qtshdye826qhsg*", "chip":"1", "id":"1000000002", "operation":"getTemp", "d1":0, "d2":0, "d3":0 }"""
mensaje = mensaje.decode("utf-8")
data = json.loads(mensaje)
print (json.dumps(data, indent=4))

respuesta = data['comKey']

print('name', respuesta)