import RPi.GPIO as gpio
import setup as s

def GPIO_motor_control():
    gpio.output(s.MOTOR_IN1, gpio.HIGH)
    gpio.output(s.MOTOR_IN2, gpio.LOW)
    gpio.output(s.MOTOR_IN3, gpio.HIGH)
    gpio.output(s.MOTOR_IN4, gpio.LOW)
    gpio.output(s.MOTOR_EN_A, gpio.HIGH)
    gpio.output(s.MOTOR_EN_B, gpio.HIGH)


def motor_control(direction, milliseconds, motorspeed_l, motorspeed_r):
    """
    Method to control the motors in terms of direction and speed.
    :param direction: Symbolize the direction where you want to go to ("turnL", "forward", ...)
    :param milliseconds: time how long you want to go into that direction
    :param motorspeed_l: speed of the left motors
    :param motorspeed_r: speed of the right motors
    :return: nothing
    """
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
