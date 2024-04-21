import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import json

load_dotenv() # Load all sensitive data from environment variables (and .env file)

# Influx
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_DATABASE = os.getenv("INFLUXDB_DATABASE")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_PASSWORD")
# MQTT
MQTT_URL = os.getenv("MQTT_URL")
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")

client = InfluxDBClient(url=INFLUXDB_URL, token=f"{INFLUXDB_DATABASE}:{INFLUXDB_PASSWORD}", org="-", ssl_ca_cert="./ca.pem")
influxHealth = client.health()
print(influxHealth)
if influxHealth.status == "fail":
    print("Connection to InfluxDB failed. Exiting.")
    exit(1)

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # Subscribing to all topics, with all possible sub-topics, i.e. for all deviceMACs
    client.subscribe("device/+/device_status", qos=2)
    client.subscribe("device/+/soil", qos=2)
    print("Subscribed to all topics")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    topic_structure = msg.topic.split("/")
    device_mac = topic_structure[1]
    measurement_name = topic_structure[2]
    p = Point(measurement_name)
    if len(topic_structure) == 3: # Measurements on Device Level
        p = p.tag("device_mac", device_mac)
        payload = json.loads(msg.payload) # Extracting JSON
        for key in payload: # writing all fields of the JSON as a InfluxField
            p = p.field(f"{measurement_name}_{key}", payload[key])

        print(f"Writing {p} into Influx")
        write_api.write(record=p, bucket=INFLUXDB_DATABASE)
    else:
        print("Can't handle incoming message")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=MQTT_CLIENT_ID)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqttc.tls_set(ca_certs='./emqxsl-ca.crt')
mqttc.connect(MQTT_URL, 8883, 60) 
mqttc.loop_forever()