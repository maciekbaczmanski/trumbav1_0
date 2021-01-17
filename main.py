import paho.mqtt.client as mqtt  # import the client1
import diodes
import battery
from threading import Thread
import time
import distance


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
    if message.topic == "trumba/stop":
        message_to_send = "Stopping!"
        client.publish("trumba/output", message_to_send)
        battery_power.terminate()
        distance_measure.terminate()
        diodes.gpioout(21, True)
    if message.topic == "Akcelerometr/Down":
        battery_power.add_power(10)


########################################

diodes.GPIO_Setup()
# washerpwm = diodes.washerpwm #
diodes.a_dir(True)
diodes.b_dir(True)
broker_address = "192.168.0.180"
client = mqtt.Client("receiver_trumba")  # create new instance
client.on_message = on_message  # Przerwanie przy dostaniu wiadomosci
client.connect(broker_address)
client.loop_start()  # start the loop
client.subscribe("trumba/charge")  # subskrypcja

power = 100
# Create Class
battery_power = battery.battery()
distance_measure = distance.distance()
# FiveSecond = Hello5Program()
# Create Thread
BatteryThread = Thread(target=battery_power.run)
DistanceThread = Thread(target=distance_measure.run)
DistanceThread.start()
# Start Thread
client.subscribe("trumba/start")
client.subscribe("trumba/stop")
client.subscribe("Akcelerometr/Down")
diodes.gpioout(21,False)
while battery_power:
    print(battery_power.power)
    time.sleep(0.2)
    diodes.charge_to_diode(battery_power.power)
    message_to_send = str(battery_power.power)
    client.publish("trumba/power", message_to_send)
    if diodes.current_speed_a != battery_power.powertospeed:
        diodes.change_a_speed(battery_power.power)
    if diodes.current_speed_b != battery_power.powertospeed:
        diodes.change_b_speed(battery_power.power)
    if distance_measure.dist < 30:
        diodes.change_a_speed(0)
        diodes.change_b_speed(0)
        diodes.a_dir(False)
        diodes.change_a_speed(100)
        diodes.change_b_speed(100)
        time.sleep(3)
        diodes.a_dir(True)

# input("press anything to stop")

# client.publish("trumba/charge", "ItsWorkingGuys")

diodes.gpioout(21, True)
client.loop_stop()  # stop the loop
client.disconnect(broker_address)
