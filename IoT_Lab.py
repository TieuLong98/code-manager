from django.contrib.sites import requests

print("Xin chào ThingsBoard")
import paho.mqtt.client as mqttclient
import time
import json
import requests
from requests import get

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "jsc3EqiuI10DZsvfj7oe"

def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light_intensity = 100
counter = 0
longitude = 0
latitude = 0

while True:
    ip = get("http://api.ipify.org").text
    print(ip)
    response = requests.get("http://ip-api.com/json/" + ip).json()
    collect_data = {'temperature': temp, 'humidity': humi, 'light':light_intensity,'longitude':longitude,'latitude':latitude}
    temp += 1
    humi += 1
    light_intensity += 1
    longitude = response['lon']
    latitude = response['lat']
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(10)
