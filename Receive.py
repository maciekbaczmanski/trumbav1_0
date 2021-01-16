import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
########################################
broker_address="192.168.0.180"
client = mqtt.Client("Reciever") #create new instance
client.on_message=on_message #Przerwanie przy dostaniu wiadomosci
client.connect(broker_address)
client.loop_start() #start the loop
client.subscribe("Akcelerometr") #subskrypcja
time.sleep(100) # wait
client.loop_stop() #stop the loop
