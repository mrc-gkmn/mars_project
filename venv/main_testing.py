import RPi.GPIO as gpio
import smbus2
import time
import cv2
import numpy as np
import sys
import linecache

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


def setup():
    # Setup BCM-Logic
    gpio.setmode(gpio.BOARD)

    # Setup USS IN/OUT-Pins
    gpio.setup(PIN_TRIGGER_L, gpio.OUT)
    gpio.setup(PIN_TRIGGER_M, gpio.OUT)
    #gpio.setup(PIN_TRIGGER_R, gpio.OUT)
    gpio.setup(PIN_ECHO_L, gpio.IN)
    gpio.setup(PIN_ECHO_M, gpio.IN)
    #gpio.setup(PIN_ECHO_R, gpio.IN)

    # Set USS Trigger off
    gpio.output(PIN_TRIGGER_L, False)
    gpio.output(PIN_TRIGGER_M, False)
    #gpio.output(PIN_TRIGGER_R, False)

    # Setup LT Pins
    # debug here with additional argument pull_up_down = gpio.PUD_UP
    #gpio.setup(PIN_LT_L, gpio.IN, pull_up_down=gpio.PUD_UP)

    # Wait to settle
    time.sleep(2)

    # Setup i2c bus 1 --> Global
    # BUS = smbus2.SMBus(1)

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    msg = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print(msg)

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
    #USS_distance_r = USS_measure("right")

    return USS_distance_l, USS_distance_m#, USS_distance_r


def USS_measure(direction):
    """
    calculates distance for each USS and returns dependent direction
    :param direction: determines the asked for direction
    :return: returns just the value for the asked for direction (just left, just right, ...)
    """
    if direction is "left":
        pulse_start_l = 0
        pulse_end_l = 0

        gpio.output(PIN_TRIGGER_L, True)
        time.sleep(0.00001)
        gpio.output(PIN_TRIGGER_L, False)

        while gpio.input(PIN_ECHO_L) == 0:
            print(str(gpio.input(PIN_ECHO_L)))
            pulse_start_l = time.time()
        while gpio.input(PIN_ECHO_L) == 1:
            pulse_end_l = time.time()
            #print("WOOP")
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
    """
    Method to call methods to determine values for all linetracker (LT)
    :return: return the value for left and right LT
    """
    LT_status_l = LT_measure("left")
    LT_status_r = LT_measure("right")

    return LT_status_l, LT_status_r


def LT_measure(direction):
    """
    Method to calculate values for each LT (left, right)
    :param direction: determines the asked for direction
    :return: returns just the value for the asked for direction (just left, just right)
    """
    if direction is "left":
        return gpio.input(PIN_LT_L)

    if direction is "right":
        return gpio.input(PIN_LT_R)


# _____________________________#
# Objectrecognition(ObRec) Logic
# ____________________________#
def obj_rec(ticks):
    """
    Method to start object recognition for defined color-range (lower/upperBound)

    :param ticks: amount of loops needed to be done (measures for each loop and accumulates results)
    :return: pos_arr which is an array and contains arrays again - arrays are filled with x-/y-/width-/height-value
             of objects and the loop-number where the object was found
    """
    lowerBound = np.array([160, 100, 100])
    upperBound = np.array([179, 255, 255])

    cam = cv2.VideoCapture(0)
    if (cam.isOpened() == False):
        print("Camera unable to read feed - Remember sudo modprobe bcm2835-v4l2")
    #cv2.waitKey(1000);
    kernelOpen = np.ones((5, 5))
    kernelClose = np.ones((20, 20))

    #ret, img = cam.read()
    #img = cv2.resize(img, (340, 220))

    font = cv2.FONT_HERSHEY_SIMPLEX

    pos_arr = []
    
    #adding 10 extra ticks for camera to initialize
    ticks = ticks + 10

    for loop_number in range(ticks):
        ret, img = cam.read()
        
        cv2.waitKey(100)

        img = cv2.resize(img, (340, 220))

        # convert BGR to HSV
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # create the Mask
        mask = cv2.inRange(imgHSV, lowerBound, upperBound)
        # morphology
        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

        maskFinal = maskClose
        _, conts, h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        cv2.drawContours(img, conts, -1, (255, 0, 0), 3)
        
        if ticks > 10:
            for i in range(len(conts)):
                x, y, w, h = cv2.boundingRect(conts[i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # cv2.putText(img, str(i + 1), (x, y + h), font, (0, 255, 255))

                pos_arr.append([x, y, w, h, loop_number])

        # cv2.imshow("maskClose", maskClose)
        # cv2.imshow("maskOpen", maskOpen)
        # cv2.imshow("mask", mask)
        # cv2.imshow("cam", img)
        
    return pos_arr


def pic_logic(position_array):
    """
    Method applies logic to the given array of information from the detected objects
    :param position_array: array which contains x-/y-/width-/height-value
             of objects and the loop-number where the object was found
    :return: obj_list - an array with information where object was detected ("obj_leftside", "obj_rightside),
             the middle position (x-axis) and the covered area from the object (width*height)
    """
    obj_list = []

    if len(position_array) > 0:

        for each in position_array:
            # Image Size is 340*220

            x_pos = each[0]
            y_pos = each[1]
            width = each[2]
            height = each[3]
            loop_no = each[4]

            area = width * height
            middle_x_pos = (width + x_pos) / 2
            middle_y_pos = (height + y_pos) / 2

            if (area > 100):  # Just noise
                continue

            if (area <= 100):  # Detected Object
                if (middle_x_pos > 170):
                    # no return
                    obj_list.append(["obj_leftside", middle_x_pos, area])

                elif (middle_x_pos <= 170):
                    obj_list.append(["obj_rightside", middle_x_pos, area])
        print("Obj detected")

        # sort for highest area object
        sorted(obj_list, key=lambda arr: arr[2])
        print(obj_list)
        print("\n")

        return obj_list, True

    elif len(position_array) < 1:
        print("No Obj detected")
        return obj_list, False


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


# _____________________________#
# i2c BUS Logic
# ____________________________#
def read_i2c_byte(address):
    """
    Method to read byte from i2c-address
    :param address: i2c-address to read byte from
    :return: results stored on address
    """
    # Open i2c bus 1 and read one byte from address, offset 0
    b = BUS.read_byte(adress, 0)
    return b


def read_i2c_block(address, number):
    """
    Method to read block from i2c-address
    :param address: i2c-address to read block from
    :param number: number of parameters you want to read
    :return: block of numbers(int) bytes of adress, offset 0
    """
    # Read a block of number(int) bytes of address, offset 0
    # returning a list of number bytes
    block = BUS.read_i2c_block_data(address, 0, number)
    return block


def write_i2c_byte(address, data):
    """
    Method to write byte to i2c-adress
    :param address: i2c-address to write byte to
    :param data:  data you want to write
    :return: nothing
    """
    BUS.write_byte_data(address, 0, data)


def write_i2c_block(adress, offset, data):
    """
    Method to write block to i2c-adress
    :param adress: i2c-address to write block to
    :param offset: offset you want to consider
    :param data: data you want to wirte
    :return: nothing
    """
    BUS.write_i2c_block_data(adress, offset, data)


# _____________________________#
# Main Logic
# ____________________________#

def main():
    """
    Main Logic which loops when the raspberry is started
    :return: nothing
    """
    try:
        setup()

        obj_detected = False

        while True:
            #lt_right = LT_measure("right")
            #lt_left = LT_measure("left")
            
            dist_left = USS_measure("left")
            dist_middle = USS_measure("middle")
            #dist_right = USS_measure("right")
            print(str(dist_left) + " " + str(dist_middle) + "\n")
            
            position_array = obj_rec(2)
            logic_array, obj_detected = pic_logic(position_array)
            
            print(str(logic_array) + " " + str(obj_detected) + "\n \n")

            # No camera object detected
            if (obj_detected is False) and False:
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

        # camera object detected
        if (obj_detected is True) and False:
            # FORWARD
            # if (dist_left > 50 or dist_middle > 30 or dist_right > 50):
            #    ampl_fact_f = 5 * (dist_middle - DESIRED_DIST_M)
            #    SPEED = MAX_SPEED + ampl_fact_f
            #    motor_control("forward", 50, SPEED, SPEED)

            # RIGHT TURN
            if (dist_left < 20 or dist_middle > 30 or dist_right > 20) and logic_array[0][0] is "obj_leftside":
                # obj_position mittig entspricht obj_pos = 170
                # verstaerkung durch 170/5 = 32
                obj_position = logic_array[0][1]
                ampl_fact_r = 5 * (DESIRED_DIST_L - dist_left) + obj_position / 5
                SPEED_R = SPEED - ampl_fact_r
                SPEED_L = SPEED + ampl_fact_r
                motor_control("right", 50, SPEED_L, SPEED_R)

            # LEFT TURN
            elif (dist_left > 20 or dist_middle > 30 or dist_right < 20) and logic_array[0][0] is "obj_rightside":
                obj_position = logic_array[0][1]
                ampl_fact_l = 5 * (DESIRED_DIST_R - dist_right) + obj_position / 5
                SPEED_R = SPEED - ampl_fact_l
                SPEED_L = SPEED + ampl_fact_l
                motor_control("left", 50, SPEED_L, SPEED_R)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    except Exception as e:
        print("ERROR:" + str(e))
        PrintException()
    finally:
        print("clean up GPIO")
        gpio.cleanup()


if __name__ == "__main__":
    main()

