import RPi.GPIO as gpio
import math
import time
import setup as s

LED_list = [0,0,0,0,0,0,0,0]
                         
def led_control(num_led,status,liste=LED_list):      
        liste[num_led] = status
        #calculation of the Outputpins for LED
        bin_LED_liste = (int(liste[0] * math.pow(2,7) +liste[1] * math.pow(2,6) +liste[2] * math.pow(2,5) +liste[3] * math.pow(2,4) +liste[4] * math.pow(2,3) +liste[5] * math.pow(2,2) +liste[6] * math.pow(2,1) +liste[7] * math.pow(2,0))) 
        s.BUS.write_i2c_block_data(0x21,0x03,[int(bin_LED_liste)])
        LED_list = liste
        
def allOFF():
    led_control(0,0)
    led_control(1,0)
    led_control(2,0)
    led_control(3,0)
    led_control(4,0)
    led_control(5,0)
    led_control(6,0)
    led_control(7,0)

def allON():
    led_control(0,1)
    led_control(1,1)
    led_control(2,1)
    led_control(3,1)
    led_control(4,1)
    led_control(5,1)
    led_control(6,1)
    led_control(7,1)

def shutdown():
    for i in range(0,4):
        allON()
        time.sleep(0.3)
        allOFF()
        time.sleep(0.3)

def startup():    
    led_control(0,1)
    time.sleep(0.2)
    led_control(1,1)
    time.sleep(0.2)
    led_control(2,1)
    time.sleep(0.2)
    led_control(3,1)
    time.sleep(0.2)
    led_control(4,1)
    time.sleep(0.2)
    led_control(5,1)
    time.sleep(0.2)
    led_control(6,1)
    time.sleep(0.2)
    led_control(7,1)
    time.sleep(0.2)
         
    led_control(0,0)
    time.sleep(0.2)
    led_control(1,0)
    time.sleep(0.2)
    led_control(2,0)
    time.sleep(0.2)
    led_control(3,0)
    time.sleep(0.2)
    led_control(4,0)
    time.sleep(0.2)
    led_control(5,0)
    time.sleep(0.2)
    led_control(6,0)
    time.sleep(0.2)
    led_control(7,0)
    time.sleep(0.2)