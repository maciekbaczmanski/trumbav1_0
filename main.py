import paho.mqtt.client as mqtt  # import the client1


############
def on_message(client, userdata, message):
    global messagereceived, message_str
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)


########################################
broker_address = "192.168.0.180"
client = mqtt.Client("Reciever")  # create new instance
client.on_message = on_message  # Przerwanie przy dostaniu wiadomosci
client.connect(broker_address)
client.loop_start()  # start the loop
client.subscribe("Akcelerometr")  # subskrypcja
input("press anything to stop")
client.loop_stop()  # stop the loop

client.publish("Akcelerometr", "ItsWorkingGuys")
client.disconnect(broker_address)
