import diodes

diodes.GPIO_Setup()

while 1:
    x = input("Podaj percent")
    diodes.charge_to_diode(x)
