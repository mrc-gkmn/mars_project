import RPi.GPIO as gpio
import smbus2
import time

# PIN declaration
# Ultrasonic declaration
PIN_TRIGGER_L = 11
PIN_TRIGGER_M = 15
PIN_TRIGGER_R = 0
PIN_ECHO_L = 24
PIN_ECHO_M = 26
PIN_ECHO_R = 0
# Linetracker declaration
PIN_LT_L = 0
PIN_LT_R = 0
# Drehzahlmesser declaration
PIN_DZM_L = 0
PIN_DZM_R = 0
DZ_L = 0
DZ_R = 0

# I2C declaration
BUS = smbus2.SMBus(1)
ENGINE_LEFT_ADD = 0x00
ENGINE_RIGHT_ADD = 0x00
GYRO_ADD = 0x00
I2C_MOTORDRIVER_ADD = 0x00

# MOTOR-CONTROL parameter
# Speed
SPEED_LEFT = 0
SPEED_FORWAD = 130
SPEED_RIGHT = 0
MIN_SPEED = 10
MAX_SPEED = 200
# Direction-Optimum
DESIRED_DIST_L = 20
DESIRED_DIST_M = 30
DESIRED_DIST_R = 20

# GPIO MOTORCONTROL
MOTOR_IN1 = 37
MOTOR_IN2 = 38
MOTOR_IN3 = 35
MOTOR_IN4 = 36
MOTOR_EN_A = 13
MOTOR_EN_B = 12


# Setup BCM-Logic
gpio.setmode(gpio.BOARD)

# Setup USS IN/OUT-Pins
gpio.setup(PIN_TRIGGER_L, gpio.OUT)
gpio.setup(PIN_TRIGGER_M, gpio.OUT)
# gpio.setup(PIN_TRIGGER_R, gpio.OUT)
gpio.setup(PIN_ECHO_L, gpio.IN)
gpio.setup(PIN_ECHO_M, gpio.IN)
# gpio.setup(PIN_ECHO_R, gpio.IN)

# Set USS Trigger off
gpio.output(PIN_TRIGGER_L, False)
gpio.output(PIN_TRIGGER_M, False)
# gpio.output(PIN_TRIGGER_R, False)

# Setup GPIO_Motorcontrol
gpio.setup(MOTOR_IN1, gpio.OUT)
gpio.setup(MOTOR_IN2, gpio.OUT)
gpio.setup(MOTOR_IN3, gpio.OUT)
gpio.setup(MOTOR_IN4, gpio.OUT)
gpio.setup(MOTOR_EN_A, gpio.OUT)
gpio.setup(MOTOR_EN_B, gpio.OUT)

# Define Motoroutputs
# gpio.output(MOTOR_IN1, gpio.LOW)
# gpio.output(MOTOR_IN2, gpio.LOW)
# gpio.output(MOTOR_IN3, gpio.LOW)
# gpio.output(MOTOR_IN4, gpio.LOW)
# gpio.output(MOTOR_EN_A, gpio.LOW)
# gpio.output(MOTOR_EN_B, gpio.LOW)

# Setup LT Pins
# debug here with additional argument pull_up_down = gpio.PUD_UP
# gpio.setup(PIN_LT_L, gpio.IN, pull_up_down=gpio.PUD_UP)

# Wait to settle
time.sleep(2)

# Setup i2c bus 1 --> Global
# BUS = smbus2.SMBus(1)
