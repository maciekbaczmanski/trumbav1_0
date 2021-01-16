import paho.mqtt.client as mqtt  # import the client1
import diodes
import battery
from threading import Thread
import time

############
def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    if message.topic == "trumba/charge":
        diodes.charge_to_diode(str(message.payload.decode("utf-8")))
        message_to_send = "Received charge: " + str(message.payload.decode("utf-8"))
        client.publish("trumba/charge_confirmation", message_to_send)
    if message.topic == "trumba/start":
        message_to_send = "Starting!"
        client.publish("trumba/output", message_to_send)
        BatteryThread.start()


########################################

diodes.GPIO_Setup()
# washerpwm = diodes.washerpwm #
diodes.gpioout(4, True)
diodes.gpioout(17, False)
diodes.gpioout(27, True)
diodes.gpioout(22, False)
broker_address = "192.168.0.180"
client = mqtt.Client("receiver_trumba")  # create new instance
client.on_message = on_message  # Przerwanie przy dostaniu wiadomosci
client.connect(broker_address)
client.loop_start()  # start the loop
client.subscribe("trumba/charge")  # subskrypcja

power = 100
#Create Class
battery_power = battery.battery()
# FiveSecond = Hello5Program()
#Create Thread
BatteryThread = Thread(target=battery_power.run)
#Start Thread
# BatteryThread.start()
client.subscribe("trumba/start")

while True:
    time.sleep(0.5)
    message_to_send = "Power: "+str(battery_power.power)
    client.publish("trumba/output", message_to_send)




# input("press anything to stop")

# client.publish("trumba/charge", "ItsWorkingGuys")


client.loop_stop()  # stop the loop
client.disconnect(broker_address)
