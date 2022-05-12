import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from enum import Enum;
import paho.mqtt.client as paho
import time

### MAIN ###
def main():
    while True:
        try:
            print('Place Tag')
            id, text = reader.read()
            print(id)
            print(text)
            sendRfidText(text)
            receive()
        finally:
            GPIO.cleanup()
            client.disconnect()

# Response Status
class Status(Enum):
    OK = 1
    BAD = 2
    ERORR = 3
    UNKOWN = 4

# MQTT Init
def on_message(client, userdata, msg):
    msgResponse = int(msg.payload)
    print(msg.topic+" "+str(msg.qos)+" "+ str(msgResponse))
    received(msgResponse)

mqttHost = "localhost"
client = paho.Client()
client.connect(mqttHost, 1883)
client.on_message = on_message
client.subscribe("SeQLock/respose")

# RFID Init
reader = SimpleMFRC522()

# LED Init
green = 15
yellow = 13
red = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)

# Send Request to Security Server
def sendRfidText(text):
    client.publish("SeQLock/verify", text)
    print('send')

# Receive Security Server Response
def receive():
    while (True):
        client.loop()

def received(status):
    if status == 1:
        GPIO.output(green,GPIO.HIGH)
    elif status == 2:
        GPIO.output(red,GPIO.HIGH)
    elif status == 3:
        GPIO.output(red,GPIO.HIGH)
        GPIO.output(yellow,GPIO.HIGH)
        GPIO.output(green,GPIO.HIGH)
    elif status == 4:
        GPIO.output(yellow,GPIO.HIGH)
    else:
        GPIO.output(yellow,GPIO.HIGH)
    time.sleep(5)
    GPIO.output(red,GPIO.LOW)
    GPIO.output(yellow,GPIO.LOW)
    GPIO.output(green,GPIO.LOW)

# Main Call
main()


GPIO.output(red,GPIO.HIGH)
GPIO.output(yellow,GPIO.HIGH)
GPIO.output(green,GPIO.HIGH)
GPIO.output(red,GPIO.LOW)
GPIO.output(yellow,GPIO.LOW)
GPIO.output(green,GPIO.LOW)
time.sleep(1)