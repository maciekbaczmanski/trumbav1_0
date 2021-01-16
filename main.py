import paho.mqtt.client as mqtt  # import the client1
import diodes

############
def on_message(client, userdata, message):
    global messagereceived, message_str
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    diodes.charge_to_diode(str(message.payload.decode("utf-8")))
    client.publish("trumba/charge", ("Received charge: ",str(message.payload.decode("utf-8"))))


########################################

diodes.GPIO_Setup()
broker_address = "192.168.0.180"
client = mqtt.Client("receiver_trumba")  # create new instance
client.on_message = on_message  # Przerwanie przy dostaniu wiadomosci
client.connect(broker_address)
client.loop_start()  # start the loop
client.subscribe("trumba/charge")  # subskrypcja
input("press anything to stop")


# client.publish("trumba/charge", "ItsWorkingGuys")























client.loop_stop()  # stop the loop
client.disconnect(broker_address)
