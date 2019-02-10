import RPi.GPIO as gpio
import smbus2
import time
import LED_control


# PWM declaration
PWM_A = 33
PWM_B = 32

# PIN declaration
PIN_BANK_0_INPUT = 11
PIN_BANK_0_OUTPUT = 12
PIN_BANK_1_INPUT = 24
PIN_BANK_1_OUTPUT = 26

# Switcher pins
SWITCHER_1 = 13 #2
SWITCHER_2 = 15 #3
SWITCHER_3 = 16 #4

# Button pins
BUTTON_A = 29
BUTTON_B = 31

# Rotaryswitcher pins
RT_SWITCHER_1 = 36
RT_SWITCHER_2 = 38
RT_SWITCHER_3 = 40
RT_SWITCHER_4 = 37

# Ultrasonic declaration
PIN_USS_L = [1, 1, 0]
PIN_USS_M = [1, 0, 0]
PIN_USS_R = [0, 1, 0]

#PIN_TRIGGER_L = [0, 0, 0]
#PIN_TRIGGER_M = [0, 0, 0]
#PIN_TRIGGER_R = [0, 0, 0]
#PIN_ECHO_L = [0, 0, 0]
#PIN_ECHO_M = [0, 0, 0]
#PIN_ECHO_R = [0, 0, 0]
# Servomotor
PIN_SERVO = [1, 1, 0]

# Linetracker declaration
PIN_LT_L = [1, 1, 1]
PIN_LT_R = [0, 1, 1]
n0 = [0, 0, 0]
n1 = [0, 0, 1]
n2 = [0, 1, 0]
n3 = [0, 1, 1]
n4 = [1, 0, 0]
n5 = [1, 0, 1]
n6 = [1, 1, 0]
n7 = [1, 1, 1]


# Drehzahlmesser declaration
PIN_DZM_L = 19
PIN_DZM_R = 18
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
MAX_SPEED = 100
MAX_MAX_SPEED = 150
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

# Setup Bank-Logic
gpio.setup(PIN_BANK_0_INPUT, gpio.IN)
gpio.setup(PIN_BANK_0_OUTPUT, gpio.OUT)
gpio.setup(PIN_BANK_1_INPUT, gpio.IN)
gpio.setup(PIN_BANK_1_OUTPUT, gpio.OUT)

# Setup Button-Logic
gpio.setup(BUTTON_A, gpio.IN)
gpio.setup(BUTTON_B, gpio.IN)

# Setup RT-Switcher
gpio.setup(RT_SWITCHER_1, gpio.IN)
gpio.setup(RT_SWITCHER_2, gpio.IN)
gpio.setup(RT_SWITCHER_3, gpio.IN)
gpio.setup(RT_SWITCHER_4, gpio.IN)

# Setup DZM-Logic
gpio.setup(PIN_DZM_L, gpio.IN)
gpio.setup(PIN_DZM_R, gpio.IN)

# Setup BWM
gpio.setup(PWM_A,gpio.OUT)
gpio.setup(PWM_B,gpio.OUT)

# PWM frequenzy setup
PIN_pwm_l = gpio.PWM(PWM_A,20)
PIN_pwm_r = gpio.PWM(PWM_B,20)

#Start PWM
PIN_pwm_l.start(0)
PIN_pwm_r.start(0)

# Setup i2c
#Set register as OUTPUT
BUS.write_i2c_block_data(0x20,0x06,[0])
BUS.write_i2c_block_data(0x20,0x07,[0])
BUS.write_i2c_block_data(0x21,0x06,[0])
BUS.write_i2c_block_data(0x21,0x07,[0])
#set everything "LOW"
BUS.write_i2c_block_data(0x20,0x02,[0b00000000])
BUS.write_i2c_block_data(0x20,0x03,[0b00000000])
BUS.write_i2c_block_data(0x21,0x02,[0b00000000])

#Set register as OUTPUT
BUS.write_i2c_block_data(0x21,0x07,[0b00000000])
#Give register the initi
BUS.write_i2c_block_data(0x21,0x03,[0b00000000])


# Setup USS IN/OUT-Pins
#gpio.setup(PIN_TRIGGER_L, gpio.OUT)
#gpio.setup(PIN_TRIGGER_M, gpio.OUT)
# gpio.setup(PIN_TRIGGER_R, gpio.OUT)
#gpio.setup(PIN_ECHO_L, gpio.IN)
#gpio.setup(PIN_ECHO_M, gpio.IN)
# gpio.setup(PIN_ECHO_R, gpio.IN)

# Set USS Trigger off
#gpio.output(PIN_TRIGGER_L, False)
#gpio.output(PIN_TRIGGER_M, False)
# gpio.output(PIN_TRIGGER_R, False)

# Setup GPIO_Motorcontrol
#gpio.setup(MOTOR_IN1, gpio.OUT)
#gpio.setup(MOTOR_IN2, gpio.OUT)
#gpio.setup(MOTOR_IN3, gpio.OUT)
#gpio.setup(MOTOR_IN4, gpio.OUT)
#gpio.setup(MOTOR_EN_A, gpio.OUT)
#gpio.setup(MOTOR_EN_B, gpio.OUT)

gpio.setup(SWITCHER_1, gpio.OUT)
gpio.setup(SWITCHER_2, gpio.OUT)
gpio.setup(SWITCHER_3, gpio.OUT)

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
time.sleep(1)
LED_control.startup()

# Setup i2c bus 1 --> Global
# BUS = smbus2.SMBus(1)

def switcher0(array):
    gpio.output(SWITCHER_3, array[0]) #4 - 9 -c
    gpio.output(SWITCHER_2, array[1]) #3 - 10 -b
    gpio.output(SWITCHER_1, array[2]) #2 - 11 - a

def switcher1(array):
    gpio.output(SWITCHER_3, array[0])
    gpio.output(SWITCHER_2, array[1])
    gpio.output(SWITCHER_1, array[2])
    
def read_switch():
    dig1 = gpio.input(RT_SWITCHER_1)
    dig2 = gpio.input(RT_SWITCHER_2)
    dig3 = gpio.input(RT_SWITCHER_3)
    dig4 = gpio.input(RT_SWITCHER_4)
    
    sum = dig4*1000+dig3*100+dig2*10+dig1
    #print(sum)
    sum = int(str(sum), 2)
    #print(sum)
    
    return sum
    
    
    
    