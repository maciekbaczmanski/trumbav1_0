import paho.mqtt.client as mqtt  # import the client1
import diodes


############
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    if message.topic == "trumba/charge":
        diodes.charge_to_diode(str(message.payload.decode("utf-8")))
        message_to_send = "Received charge: " + str(message.payload.decode("utf-8"))
        client.publish("trumba/charge_confirmation", message_to_send)


########################################

diodes.GPIO_Setup()
washerpwm = diodes.washerpwm #
washerpwm.start(100.0)
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
