import RPi.GPIO as gpio
import setup as s
import time
# _____________________________#
# Ultrasonicsensor (USS) Logic
# ____________________________#
def USS():
    """
    Method to call methods to determine distance via ultrasonic-sensor (USS)
    :return: Distance for left, middle and right USS
    """
    print("test")
    USS_distance_l = USS_measure("left")
    USS_distance_m = USS_measure("middle")
    USS_distance_r = USS_measure("right")

    return USS_distance_l, USS_distance_m , USS_distance_r


def USS_measure(direction):
    """
    calculates distance for each USS and returns dependent direction
    :param direction: determines the asked for direction
    :return: returns just the value for the asked for direction (just left, just right, ...)
    """
    pulse_start = 0
    pulse_end = 0

    if direction is "left":
        s.switcher0(s.PIN_USS_L)

    if direction is "middle":
        s.switcher0(s.PIN_USS_M)

    if direction is "right":
        s.switcher0(s.PIN_USS_R)

    gpio.output(s.PIN_BANK_0_OUTPUT, True)
    time.sleep(0.00001)
    gpio.output(s.PIN_BANK_0_OUTPUT, False)

    while gpio.input(s.PIN_BANK_0_INPUT) == 0:
        print(str(gpio.input(s.PIN_BANK_0_INPUT)))
        pulse_start = time.time()
    while gpio.input(s.PIN_BANK_0_INPUT) == 1:
        pulse_end = time.time()
        # print("WOOP")
    pulse_duration = pulse_end - pulse_start
    distance = round(pulse_duration * 17150, 2)

    return distance