import paho.mqtt.client as mqtt #import the client1
broker_address="192.168.0.180"
client = mqtt.Client()
client.username_pw_set(“username”, “password”)
client.connect(broker_address)
client.publish("Akcelerometr","HelloThere",qos=1,retain=True)
client.disconnect(broker_address)
