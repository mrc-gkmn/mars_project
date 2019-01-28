import gpio
import smbus2
import time

# PIN decleration
PIN_TRIGGER_L = 0
PIN_TRIGGER_M = 0
PIN_TRIGGER_R = 0
PIN_ECHO_L = 0
PIN_ECHO_M = 0
PIN_ECHO_R = 0

PIN_LT_L = 0
PIN_LT_R = 0

BUS = smbus2.SMBus(1)
ENGINE_LEFT_ADD = 0x00
ENGINE_RIGHT_ADD = 0x00
GYRO_ADD = 0x00

I2C_MOTORDRIVER_ADD = 0x00

SPEED_LEFT = 0
SPEED_FORWAD = 130
SPEED_RIGHT = 0
MIN_SPEED = 10
MAX_SPEED = 200

DESIRED_DIST_L = 20
DESIRED_DIST_M = 30
DESIRED_DIST_R = 20


def setup():
    # Setup BCM-Logic
    gpio.setmode(gpio.BCM)

    # Setup USS IN/OUT-Pins
    gpio.setup(PIN_TRIGGER_L, gpio.OUT)
    gpio.setup(PIN_TRIGGER_M, gpio.OUT)
    gpio.setup(PIN_TRIGGER_R, gpio.OUT)
    gpio.setup(PIN_ECHO_L, gpio.IN)
    gpio.setup(PIN_ECHO_M, gpio.IN)
    gpio.setup(PIN_ECHO_R, gpio.IN)

    # Set USS Trigger off
    gpio.output(PIN_TRIGGER_L, False)
    gpio.output(PIN_TRIGGER_M, False)
    gpio.output(PIN_TRIGGER_R, False)

    # Setup LT Pins
    # debug here with additional argument pull_up_down = gpio.PUD_UP
    gpio.setup(PIN_LT_L, gpio.IN, pull_up_down=gpio.PUD_UP)

    # Wait to settle
    time.sleep(2)

    # Setup i2c bus 1 --> Global
    # BUS = smbus2.SMBus(1)


# _____________________________#
# Ultrasonicsensor (USS) Logic
# ____________________________#
def USS():
    USS_distance_l = USS_measure("left")
    USS_distance_m = USS_measure("middle")
    USS_distance_r = USS_measure("right")


def USS_measure(direction):
    if direction is "left":
        pulse_start_l = 0
        pulse_end_l = 0

        gpio.output(PIN_TRIGGER_L, True)
        time.sleep(0.00001)
        gpio.output(PIN_TRIGGER_L, False)

        while gpio.input(PIN_ECHO_L) == 0:
            pulse_start_l = time.time()
        while gpio.input(PIN_ECHO_L) == 1:
            pulse_end_l = time.time()
        pulse_duration_l = pulse_end_l - pulse_start_l
        distance_l = round(pulse_duration_l * 17150, 2)

        return distance_l

    if direction is "middle":
        gpio.output(PIN_TRIGGER_M, True)
        time.sleep(0.00001)
        gpio.output(PIN_TRIGGER_M, False)

        pulse_start_m = 0
        pulse_end_m = 0

        gpio.output(PIN_TRIGGER_M, True)
        time.sleep(0.00001)
        gpio.output(PIN_TRIGGER_M, False)

        while gpio.input(PIN_ECHO_M) == 0:
            pulse_start_m = time.time()
        while gpio.input(PIN_ECHO_M) == 1:
            pulse_end_m = time.time()
        pulse_duration_m = pulse_end_m - pulse_start_m
        distance_m = round(pulse_duration_m * 17150, 2)

        return distance_m

    if direction is "right":
        gpio.output(PIN_TRIGGER_R, True)
        time.sleep(0.00001)
        gpio.output(PIN_TRIGGER_R, False)

        pulse_start_r = 0
        pulse_end_r = 0

        gpio.output(PIN_TRIGGER_R, True)
        time.sleep(0.00001)
        gpio.output(PIN_TRIGGER_R, False)

        while gpio.input(PIN_ECHO_R) == 0:
            pulse_start_r = time.time()
        while gpio.input(PIN_ECHO_R) == 1:
            pulse_end_r = time.time()
        pulse_duration_r = pulse_end_r - pulse_start_r
        distance_r = round(pulse_duration_r * 17150, 2)

        return distance_r


# _____________________________#
# Linetracker(LT) Logic
# ____________________________#
def LT():
    LT_status_l = LT_measure("left")
    LT_status_r = LT_measure("right")


def LT_measure(direction):
    if direction is "left":
        return gpio.input(PIN_LT_L)

    if direction is "right":
        return gpio.input(PIN_LT_R)


def motor_control(direction, milliseconds, motorspeed_l, motorspeed_r):
    direct = ""

    if direction is "turnL":
        direct = 0b1001

    if direction is "turnR":
        direct = 0b0110

    if direction is "forward":
        direct = 0b1010

    if direction is "backward":
        direct = 0b0101

    if direction is "stop":
        direct = 0b0000

    # middle parameter with direct needed?
    write_i2c_block(I2C_MOTORDRIVER_ADD, direct, [motorspeed_l, motorspeed_r])

    # TODO Sleep hier reinpacken (IC2 Vorteile nutzen?)
    time.sleep(milliseconds / 1000.0)


# _____________________________#
# i2c BUS Logic
# ____________________________#
def read_i2c_byte(address):
    # Open i2c bus 1 and read one byte from address, offset 0
    b = BUS.read_byte(adress, 0)
    return b


def read_i2c_block(address, number):
    # Read a block of number(int) bytes of address, offset 0
    # returning a list of number bytes
    block = BUS.read_i2c_block_data(address, 0, number)
    return block


def write_i2c_byte(address, data):
    BUS.write_byte_data(address, 0, data)


def write_i2c_block(adress, offset, data):
    BUS.write_i2c_block_data(adress, offset, data)


# _____________________________#
# Main Logic
# ____________________________#

def main():



    while True:
        dist_left = USS_measure("left")
        dist_middle = USS_measure("middle")
        dist_right = USS_measure("right")

        # FORWARD
        if dist_left > 50 or dist_middle > 30 or dist_right > 50:
            ampl_fact_f = 5 * (dist_middle - DESIRED_DIST_M)
            SPEED = MAX_SPEED + ampl_fact_f
            motor_control("forward", 50, SPEED, SPEED)

        # RIGHT TURN
        elif dist_left < 20 or dist_middle > 30 or dist_right > 20:
            ampl_fact_r = 5 * (DESIRED_DIST_L - dist_left)
            SPEED_R = SPEED - ampl_fact_r
            SPEED_L = SPEED + ampl_fact_r
            motor_control("right", 50, SPEED_L, SPEED_R)

        # LEFT TURN
        elif dist_left > 20 or dist_middle > 30 or dist_right < 20:
            ampl_fact_l = 5 * (DESIRED_DIST_R - dist_right)
            SPEED_R = SPEED - ampl_fact_l
            SPEED_L = SPEED + ampl_fact_l
            motor_control("left", 50, SPEED_L, SPEED_R)


if __name__ == "__main__":
    main()
