#------------------------------------------
#--- Author: Asinine Fatuity
#--- Date: 7th September 2021
#--- Version: 1.0
#--- Python Ver: 3.8
#------------------------------------------

import paho.mqtt.client as mqtt
from queue import Queue
from authenticate import topic_data_handler

my_payload_Queue=Queue()
global message_decoded

# MQTT Settings 
MQTT_Broker = "139.162.254.51"
MQTT_Port = 1883
MQTT_username=""
MQTT_password=""
Keep_Alive_Interval = 45
MQTT_Topic = "acc/s/#"

def queue_payload(msg):
	my_payload_Queue.put(msg.payload)
	while not my_payload_Queue.empty():
		message=my_payload_Queue.get()
		if message is not None:
			message_decoded=message.decode("utf-8","ignore")
			print(f"MQTT data received from topic: ",str(msg.topic))
			print(f"Data received: ",message_decoded)
			topic_data_handler(msg.topic,message_decoded)
		else:
			print("sipati picha")
			continue
def on_connect(mosq, userdata, flags,rc):
	client.subscribe(MQTT_Topic,0)
	my_payload_Queue.queue.clear()
def on_message(mosq, userdata, msg):
	if msg.retain==0:
		queue_payload(msg)
						
def on_subscribe(mosq, obj, mid, granted_qos):
    pass
def publish(topic,msg):
	client.publish(topic,msg)
client = mqtt.Client()
client.username_pw_set(MQTT_username,MQTT_password)

# Assign callback functions to created callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_subscribe = on_subscribe

# Connect
client.connect(MQTT_Broker, int(MQTT_Port),int(Keep_Alive_Interval))

# Continue the network loop so as to continually process the callback functions
client.loop_forever()