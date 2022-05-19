import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import time
import math
import uuid
from mfrc522 import SimpleMFRC522
#from enum import Enum;
from datetime import datetime

### MAIN ###
def main():
    try:
        while True:
            chipinfo = readRfid()
            sendVerificationRequest(chipinfo)
            #test user: max.mustermann:&FXkv[\W8PCM9!vY
            #sendVerificationRequest("bWF4Lm11c3Rlcm1hbm46JkZYa3ZbXFc4UENNOSF2WQ==")
            receiveVerification()
    finally:
        GPIO.cleanup()
        client.disconnect()

# MQTT Init
def on_message(client, userdata, msg):
    global messageReceived
    global unixtime
    messageReceived = True
    client.unsubscribe(responseTopic + "/" + str(unixtime))
    msgResponse = int(msg.payload)
    print("Response received on topic " + msg.topic + ": " + str(msgResponse))
    processResponse(msgResponse)

mqttHost = "localhost"
userid = str(uuid.uuid4())
responseTopic = "SeQLock/response/user" + userid
requestTopic = "SeQLock/verify"
client = paho.Client()
client.connect(mqttHost, 1883)
client.on_message = on_message

# RFID Init
reader = SimpleMFRC522()

# LED Init
ledDuration = 3
green = 13
yellow = 15
red = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)

# Read Rfid Chip
def readRfid():
    print('Waiting for input...')
    id, text = reader.read()
    print(id)
    print(text)
    return text

# Send Request to Security Server
def sendVerificationRequest(body):
    global unixtime
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    unixtime = math.floor(ts)
    
    client.subscribe(responseTopic + "/" + str(unixtime))
    print("Subscribed to topic " + responseTopic + "/" + str(unixtime) + " at host " + mqttHost)
    
    msg = "{\"basic\":\""+body+"\",\"timestamp\":\""+str(unixtime)+ "\",\"userid\":\"" + userid + "\"}"
    client.publish(requestTopic, msg)
    print("Send: " + msg + " to topic " + requestTopic)
    
# Receive Security Server Response
def receiveVerification():
    global messageReceived
    messageReceived = False
    while (messageReceived == False):
        client.loop()

# Received Security Server Response
def processResponse(status):
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
    time.sleep(ledDuration)
    GPIO.output(red,GPIO.LOW)
    GPIO.output(yellow,GPIO.LOW)
    GPIO.output(green,GPIO.LOW)

# Main Call
main()
