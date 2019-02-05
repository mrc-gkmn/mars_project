import RPi.GPIO as gpio
import smbus2
import time
import cv2
import numpy as np
import sys
import linecache

# scripts
import i2c
import motor_control
import setup
import USS
import LT
import camera


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
# Main Logic
# ____________________________#

def main():
    
    """
    Main Logic which loops when the raspberry is started
    :return: nothing
    """
    try:

        obj_detected = False

        print("Go")

        motor_control.GPIO_motor_control()

        print("Lets go")

        while True:

            # lt_right = LT.LT_measure("right")
            # lt_left = LT.LT_measure("left")

            dist_left = USS.USS_measure("left")
            dist_middle = USS.USS_measure("middle")
            # dist_right = USS.USS_measure("right")
            print(str(dist_left) + " " + str(dist_middle) + "\n")

            position_array = camera.obj_rec(2)
            logic_array, obj_detected = camera.pic_logic(position_array)

            print(str(logic_array) + " " + str(obj_detected) + "\n \n")

            button_A = i2c.read_i2c_block(BUTTON_ADDRESS, 1)

            if button_A == 1:
                switcher = i2c.read_i2c_block(SWITCH_ADDRESS, 1)


                while (i2c.read_i2c_block(button_B, 1) is not True):

                    if switcher == 0 or switcher == 1: # track 1 and 2
                        if switcher==0:
                            SPEED = setup.MAX_SPEED

                        else: #track2
                            SPEED = setup.MAX_SPEED/2

                        motor_control.motor_control("forward", 50, SPEED, SPEED)

                    if switcher == 2: # track 3
                        LT_left, LT_right = LT.LT()

                        SLOW_SIDE = 10
                        FAST_SIDE = 250

                        if (LT_left == False and LT_right == False):
                            motor_control.motor_control("forward", 10, 150, 150)

                        elif (LT_left == True):
                            SPEED_L = SLOW_SIDE
                            SPEED_R = FAST_SIDE
                            motor_control.motor_control("turnL", 10, SPEED_L, SPEED_R)

                        elif (LT_right == True):
                            SPEED_L = FAST_SIDE
                            SPEED_R = SLOW_SIDE
                            motor_control.motor_control("turnR", 10, SPEED_L, SPEED_R)

                    if switcher == 3: # track 4
                        driving_time = 3
                        motor_control.motor_control("stop", 50, 0, 0)
                        max_dist_l = 20
                        max_dist_m = 50
                        max_dist_r = 20

                        gpio.add_event_detect(setup.PIN_DZM_L, gpio.RISING)
                        gpio.add_event_detect(setup.PIN_DZM_R, gpio.RISING)

                        USS_l, USS_m, USS_r = USS.USS_measure()

                        position_array = camera.obj_rec(2)
                        logic_array, obj_detected = camera.pic_logic(position_array)


                        if USS_l > max_dist_l and USS_m > max_dist_m and USS_r > max_dist_r:
                            # Fahrt vorwaerts
                            driving_direction = "forward"

                            SPEED = setup.MAX_SPEED
                            motor_control.motor_control(driving_direction, 50, SPEED, SPEED)
                            gpio.add_event_callback(setup.PIN_DZM_L, DZM.DZM_l(driving_direction))
                            gpio.add_event_callback(setup.PIN_DZM_R, DZM.DZM_r(driving_direction))

                        if USS_l > max_dist_l and USS_m > max_dist_m and USS_r > max_dist_r:
                            pass


                        time.sleep(driving_time)
                        motor_control.motor_control("stop", 50, 0, 0)

















            # No camera object detected
            if (obj_detected is False) and False:
                # FORWARD
                if dist_left > 50 or dist_middle > 30 or dist_right > 50:
                    ampl_fact_f = 5 * (dist_middle - DESIRED_DIST_M)
                    SPEED = MAX_SPEED + ampl_fact_f
                    motor_control.motor_control("forward", 50, SPEED, SPEED)

                # RIGHT TURN
                elif dist_left < 20 or dist_middle > 30 or dist_right > 20:
                    ampl_fact_r = 5 * (DESIRED_DIST_L - dist_left)
                    SPEED_R = SPEED - ampl_fact_r
                    SPEED_L = SPEED + ampl_fact_r
                    motor_control.motor_control("right", 50, SPEED_L, SPEED_R)

                # LEFT TURN
                elif dist_left > 20 or dist_middle > 30 or dist_right < 20:
                    ampl_fact_l = 5 * (DESIRED_DIST_R - dist_right)
                    SPEED_R = SPEED - ampl_fact_l
                    SPEED_L = SPEED + ampl_fact_l
                    motor_control.motor_control("left", 50, SPEED_L, SPEED_R)

        # camera object detected
        if (obj_detected is True) and False:
            # FORWARD
            # if (dist_left > 50 or dist_middle > 30 or dist_right > 50):
            #    ampl_fact_f = 5 * (dist_middle - DESIRED_DIST_M)
            #    SPEED = MAX_SPEED + ampl_fact_f
            #    motor_control.motor_control("forward", 50, SPEED, SPEED)

            # RIGHT TURN
            if (dist_left < 20 or dist_middle > 30 or dist_right > 20) and logic_array[0][0] is "obj_leftside":
                # obj_position mittig entspricht obj_pos = 170
                # verstaerkung durch 170/5 = 32
                obj_position = logic_array[0][1]
                ampl_fact_r = 5 * (DESIRED_DIST_L - dist_left) + obj_position / 5
                SPEED_R = SPEED - ampl_fact_r
                SPEED_L = SPEED + ampl_fact_r
                motor_control.motor_control("right", 50, SPEED_L, SPEED_R)

            # LEFT TURN
            elif (dist_left > 20 or dist_middle > 30 or dist_right < 20) and logic_array[0][0] is "obj_rightside":
                obj_position = logic_array[0][1]
                ampl_fact_l = 5 * (DESIRED_DIST_R - dist_right) + obj_position / 5
                SPEED_R = SPEED - ampl_fact_l
                SPEED_L = SPEED + ampl_fact_l
                motor_control.motor_control("left", 50, SPEED_L, SPEED_R)
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
