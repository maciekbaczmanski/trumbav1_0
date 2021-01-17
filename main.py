import paho.mqtt.client as mqtt  # import the client1
import diodes
import battery
from threading import Thread
import time
import distance


def on_message(client, userdata, message):
    global sportmode, automode
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    if message.topic == "trumba/charge":
        diodes.charge_to_diode(str(message.payload.decode("utf-8")))
        message_to_send = "Received charge: " + str(message.payload.decode("utf-8"))
        client.publish("trumba/charge_confirmation", message_to_send)
    if message.topic == "Mode/Sport":
        message_to_send = "Starting!"
        client.publish("trumba/output", message_to_send)
        diodes.gpioout(21, False)
        battery_power.power = 100
        battery_power.count = True
        automode = False
        sportmode = True

    if message.topic == "Mode/Auto":
        message_to_send = "Starting!"
        client.publish("trumba/output", message_to_send)
        diodes.gpioout(21, False)
        sportmode = False
        automode = True

    if message.topic == "Mode/Quit":
        message_to_send = "Stopping!"
        client.publish("trumba/output", message_to_send)
        diodes.change_a_speed(0)
        diodes.change_b_speed(0)
        battery_power.count = False
        automode = False
        sportmode = False
        # battery_power.terminate()
        # distance_measure.terminate()
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
BatteryThread.start()
# Start Thread
client.subscribe("trumba/start")
client.subscribe("trumba/stop")
client.subscribe("Akcelerometr/Down")
client.subscribe("Mode/Quit")
client.subscribe("Mode/Sport")
client.subscribe("Mode/Auto")

message_to_send = str(battery_power.power)
client.publish("trumba/power", message_to_send)
lastpower = battery_power.power
sportmode = False
automode = False
lastdist = distance_measure.dist
while battery_power:
    # print(battery_power.power)
    print(distance_measure.dist)
    time.sleep(0.05)
    diodes.charge_to_diode(battery_power.power)
    if sportmode:
        if battery_power.power != lastpower:
            message_to_send = str(battery_power.power)
            client.publish("trumba/power", message_to_send)
            lastpower = battery_power.power

        if diodes.current_speed_a != battery_power.powertospeed:
            diodes.change_a_speed(battery_power.power)
        if diodes.current_speed_b != battery_power.powertospeed:
            diodes.change_b_speed(battery_power.power)
        if distance_measure.dist < 30 and abs(lastdist - distance_measure.dist) < 10:
            diodes.change_a_speed(0)
            diodes.change_b_speed(0)
            diodes.a_dir(False)
            diodes.change_a_speed(100)
            diodes.change_b_speed(100)
            time.sleep(3)
            diodes.a_dir(True)
            lastdist = distance_measure.dist
    if automode:
        diodes.change_a_speed(100)
        diodes.change_b_speed(100)
        if distance_measure.dist < 30 and abs(lastdist - distance_measure.dist) < 10:
            diodes.change_a_speed(0)
            diodes.change_b_speed(0)
            diodes.a_dir(False)
            diodes.change_a_speed(100)
            diodes.change_b_speed(100)
            time.sleep(3)
            diodes.a_dir(True)
            lastdist = distance_measure.dist

# input("press anything to stop")

# client.publish("trumba/charge", "ItsWorkingGuys")

diodes.gpioout(21, True)
client.loop_stop()  # stop the loop
client.disconnect(broker_address)
