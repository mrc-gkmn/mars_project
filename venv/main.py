import RPi.GPIO as gpio
import smbus2
import time
import cv2
import numpy as np
import sys
import linecache

# scripts
import setup
import motor_control
import USS
#import LT
import camera
import DZM
import LED_control


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

        #setup.PIN_pwm_r.stop()
        #setup.PIN_pwm_l.stop()
        #motor_control.GPIO_motor_control()
                
        motor_control.motor_control("stop", 5, 0, 0)
        print(setup.BUS.read_i2c_block_data(0x20,0x02,1))
        print("Lets go")
        
        first_loop = 1

        while True:

            #lt_right = LT.LT_measure("right")
            #lt_left = LT.LT_measure("left")

            dist_left = USS.USS_measure("left")
            dist_middle = USS.USS_measure("middle")
            dist_right = USS.USS_measure("right")
            print(str(dist_left) + " " + str(dist_middle) + " " + str(dist_right) + "\n")

            #position_array = camera.obj_rec(2)
            #logic_array, obj_detected = camera.pic_logic(position_array)

            #print(str(logic_array) + " " + str(obj_detected) + "\n \n")

            #button_A = i2c.read_i2c_block(setup.BUTTON_A, 1)
            button_A = gpio.input(setup.BUTTON_A)
            print(" Button A:" + str(button_A))
            
            button_B = gpio.input(setup.BUTTON_B)
            print(" Button B:" + str(button_B))
            
            
            
            if button_A == 0:
                driving_time = 1
                break_time = 0.1
                #switcher = i2c.read_i2c_block(SWITCH_ADDRESS, 1)
                switcher = gpio
                switcher = 3
                switcher = setup.read_switch()
                print("switchter: " + str(switcher))
                
                button_B = gpio.input(setup.BUTTON_B)
                
                while (button_B == 1):
                    button_B = gpio.input(setup.BUTTON_B)
                    
                    if switcher == 0 or switcher == 1:  # track 1 and 2
                        if switcher == 0:
                            SPEED = setup.MAX_SPEED

                        else:  # track2
                            SPEED = setup.MAX_SPEED / 1.7                    
                            
                        if first_loop == 1:
                            first_loop = 0
                            motor_control.motor_control("forward", 50, SPEED, SPEED)
                            
                        #time.sleep(driving_time)
                        #motor_control.motor_control("stop", 50 , 0, 0)
                        #time.sleep(break_time)

                    if switcher == 2:  # track 3
                        
                        LT_left, LT_right = LT.LT()
                        print("LT_left: "+ str(LT_left) + " LT_right " + str(LT_right) + "\n")
                        print(LT_array)
                        
                        SLOW_SIDE = 10
                        FAST_SIDE = 250

                        if (LT_left == 0 and LT_right == 0):
                            if first_loop == 1:
                                motor_control.motor_control("forward", 10, 150, 150)
                                first_loop = 0

                        elif (LT_left == 1):
                            print("+++++++++++++++++++++++++++LT_left: "+ str(LT_left) + " LT_right " + str(LT_right) + "\n")
                            first_loop = 1
                            SPEED_L = SLOW_SIDE
                            SPEED_R = FAST_SIDE
                            motor_control.motor_control("forward", 10, SPEED_L, SPEED_R)

                        elif (LT_right == 1):
                            print("___________________________LT_left: "+ str(LT_left) + " LT_right " + str(LT_right) + "\n")
                            first_loop = 1
                            SPEED_L = FAST_SIDE
                            SPEED_R = SLOW_SIDE
                            motor_control.motor_control("forward", 10, SPEED_L, SPEED_R)

                    if switcher == 3:  # track 4
                        driving_direction = "forward"
                        driving_time = 1
                        waiting_time = 10
                        motor_control.motor_control("stop", 5, 0, 0)
                        time.sleep(2)
                        max_dist_l = 20
                        max_dist_m = 50
                        max_dist_m_reverse = 10
                        max_dist_r = 20


                        #gpio.add_event_detect(setup.PIN_DZM_L, gpio.RISING)
                        #gpio.add_event_detect(setup.PIN_DZM_R, gpio.RISING)

                        USS_l, USS_m, USS_r = USS.USS()

                        position_array = camera.obj_rec(2)
                        logic_array, obj_detected = camera.pic_logic(position_array)
                        print(str(logic_array) + " " + str(obj_detected) + "\n \n")

                        SPEED_L = setup.MAX_SPEED
                        SPEED_R = setup.MAX_SPEED


                        # Assign Camera-Data and Process Camera Data (left/right-Factor)
                        if len(logic_array) is not 0:
                            first_obj_side = logic_array[0][0]
                            first_x_avg_pos = logic_array[0][1]
                            first_y_avg_pos = logic_array[0][2]
                            first_y_pos = logic_array[0][3]
                            first_area = logic_array[0][4]

                            if first_obj_side is "obj_leftside":
                                SPEED_L = SPEED_L + 0.25 * (first_x_avg_pos)
                                SPEED_R = SPEED_R - 0.25 * (first_x_avg_pos)

                            elif first_obj_side is "obj_rightside":
                                SPEED_L = SPEED_L - 0.25 * first_x_avg_pos-(first_x_avg_pos%170)
                                SPEED_R = SPEED_R + 0.25 * first_x_avg_pos-(first_x_avg_pos%170)

                        # Driving Direction via Ultrasonicsensor
                        if USS_l > max_dist_l and USS_m > max_dist_m and USS_r > max_dist_r:
                            # drive forward
                            driving_direction = "forward"

                        elif USS_l < max_dist_l and USS_m > max_dist_m and USS_r > max_dist_r:
                            # drive right
                            driving_direction = "forward"
                            SPEED_L = SPEED_L
                            SPEED_R = SPEED_R - 2*(max_dist_l-USS_l)

                        elif USS_l > max_dist_l and USS_m > max_dist_m and USS_r < max_dist_r:
                            # drive left
                            driving_direction = "forward"
                            SPEED_L = SPEED_L - 2*(max_dist_l-USS_r)
                            SPEED_R = SPEED_R

                        elif USS_l > max_dist_l and USS_m < max_dist_m_reverse and USS_r > max_dist_r:
                            # drive slow
                            driving_direction = "stop"
                            SPEED_L = SPEED_L - 2*(max_dist_l-USS_m)
                            SPEED_R = SPEED_R - 2*(max_dist_l-USS_m)

                        # Consider Drehzahlmesser
                        max_dz_difference = 4
                        DZM_faktor = 5

                        DZ_dif = setup.DZ_L - setup.DZ_R

                        if abs(DZ_dif) > max_dz_difference:
                            if DZ_dif > 0:
                                # orientate left
                                SPEED_L = SPEED_L - DZM_faktor * DZ_dif
                                SPEED_R = SPEED_R + DZM_faktor * DZ_dif

                            if DZ_sum < 0:
                                # orientate right
                                SPEED_L = SPEED_L + DZM_faktor * DZ_dif
                                SPEED_R = SPEED_R - DZM_faktor * DZ_dif

                        # Maxspeed check
                        if SPEED_L > setup.MAX_MAX_SPEED:
                            SPEED_L = setup.MAX_MAX_SPEED

                        if SPEED_R > setup.MAX_MAX_SPEED:
                            SPEED_R = setup.MAX_MAX_SPEED

                        # Minspeed check
                        if SPEED_L < 0:
                            SPEED_L = 0
                        if SPEED_R < 0:
                            SPEED_R = 0
                            

                        #gpio.add_event_callback(setup.PIN_DZM_L, DZM.DZM_l(driving_direction))
                        #gpio.add_event_callback(setup.PIN_DZM_R, DZM.DZM_r(driving_direction))
                        print("Speed L:" + str(SPEED_L)+"Speed R:" +str(SPEED_R))
                        motor_control.motor_control(driving_direction, 50, SPEED_L, SPEED_R)

                        time.sleep(driving_time)
                        motor_control.motor_control("stop", 5, 0, 0)
                        time.sleep(waiting_time)
                    
                    #button_A = gpio.input(setup.BUTTON_A)
                    if (button_B == 0):
                        motor_control.motor_control("stop", 5, 0, 0)
                        first_loop = 1


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