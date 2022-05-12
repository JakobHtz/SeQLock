import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import paho.mqtt.client as paho
import time

mqttHost = "localhost"
reader = SimpleMFRC522()
client = paho.Client()
client.connect(mqttHost, 1883)

def sendRfid(text):
	client.publish("test", text)
	print('send')

while True:
	try:
		choice = input('R/W:')
		if(choice == 'R' or choice == 'r'):
			print('Place Tag')
			id, text = reader.read()
			print(id)
			print(text)
			sendRfid(text)
		elif(choice == 'W' or choice == 'w'):
			text = input('New Data:')
			print("Place Tag")
			reader.write(text)
			print("Written")
	finally:
		GPIO.cleanup()
		client.disconnect()
