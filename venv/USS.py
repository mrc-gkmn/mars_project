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
    if direction is "left":
        pulse_start_l = 0
        pulse_end_l = 0

        gpio.output(s.PIN_TRIGGER_L, True)
        time.sleep(0.00001)
        gpio.output(s.PIN_TRIGGER_L, False)

        while gpio.input(s.PIN_ECHO_L) == 0:
            print(str(gpio.input(s.PIN_ECHO_L)))
            pulse_start_l = time.time()
        while gpio.input(s.PIN_ECHO_L) == 1:
            pulse_end_l = time.time()
            # print("WOOP")
        pulse_duration_l = pulse_end_l - pulse_start_l
        distance_l = round(pulse_duration_l * 17150, 2)

        return distance_l

    if direction is "middle":
        gpio.output(s.PIN_TRIGGER_M, True)
        time.sleep(0.00001)
        gpio.output(s.PIN_TRIGGER_M, False)

        pulse_start_m = 0
        pulse_end_m = 0

        gpio.output(s.PIN_TRIGGER_M, True)
        time.sleep(0.00001)
        gpio.output(s.PIN_TRIGGER_M, False)

        while gpio.input(s.PIN_ECHO_M) == 0:
            pulse_start_m = time.time()
        while gpio.input(s.PIN_ECHO_M) == 1:
            pulse_end_m = time.time()
        pulse_duration_m = pulse_end_m - pulse_start_m
        distance_m = round(pulse_duration_m * 17150, 2)

        return distance_m

    if direction is "right":
        gpio.output(s.PIN_TRIGGER_R, True)
        time.sleep(0.00001)
        gpio.output(s.PIN_TRIGGER_R, False)

        pulse_start_r = 0
        pulse_end_r = 0

        gpio.output(s.PIN_TRIGGER_R, True)
        time.sleep(0.00001)
        gpio.output(s.PIN_TRIGGER_R, False)

        while gpio.input(s.PIN_ECHO_R) == 0:
            pulse_start_r = time.time()
        while gpio.input(s.PIN_ECHO_R) == 1:
            pulse_end_r = time.time()
        pulse_duration_r = pulse_end_r - pulse_start_r
        distance_r = round(pulse_duration_r * 17150, 2)

        return distance_r