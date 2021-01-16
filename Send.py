import paho.mqtt.client as mqtt #import the client1
broker_address="192.168.0.180"
client = mqtt.Client("Sender")
client.connect(broker_address)
client.publish("Akcelerometr","HelloThere")
client.disconnect(broker_address)
