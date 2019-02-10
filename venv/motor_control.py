import RPi.GPIO as gpio
import math
import time
import LED_control
import setup as s

s.PIN_pwm_l.start(0)
s.PIN_pwm_r.start(0)

def motor_control(direction,milliseconds,motorspeed_l, motorspeed_r):
       
    PWM_l = int(motorspeed_l /255*100)
    PWM_r = int(motorspeed_r /255*100)
    print("PWM_l: {} PWM_r: {}".format(PWM_l, PWM_r))
    
    
    if (direction == "turnL"):
        s.BUS.write_i2c_block_data(0x20,0x03,[0b00000000])
        LED_control.led_control(7,1)
        
        print("---------turnL")
        motor_direction_l(0)
        motor_direction_r(1)
        s.PIN_pwm_l.ChangeDutyCycle(PWM_l)
        s.PIN_pwm_r.ChangeDutyCycle(PWM_r)
        
        
    if (direction == "turnR"):
        s.BUS.write_i2c_block_data(0x20,0x03,[0b00000000])
        LED_control.led_control(5,1)
        
        print("---------turnR")
        motor_direction_l(1)
        motor_direction_r(0)
        s.PIN_pwm_l.ChangeDutyCycle(PWM_l)
        s.PIN_pwm_r.ChangeDutyCycle(PWM_r)
        
    if (direction == "forward"):
        s.BUS.write_i2c_block_data(0x20,0x03,[0b00000000])
        LED_control.allOFF()
        LED_control.led_control(3,1)
        print("---------forward")
        motor_direction_l(1)
        motor_direction_r(1)
        s.PIN_pwm_l.ChangeDutyCycle(PWM_l)
        s.PIN_pwm_r.ChangeDutyCycle(PWM_r)
        
    if (direction == "backward"):
        s.BUS.write_i2c_block_data(0x20,0x03,[0b00000000])
        LED_control.led_control(1,1)
        print("---------backward")
        motor_direction_l(0)
        motor_direction_r(0)
        s.PIN_pwm_l.ChangeDutyCycle(PWM_l)
        s.PIN_pwm_r.ChangeDutyCycle(PWM_r)
        
    if (direction == "stop"):
        s.BUS.write_i2c_block_data(0x20,0x03,[0b00000000])
        LED_control.allOFF()
        LED_control.led_control(7,1)
        LED_control.led_control(6,1)
        LED_control.led_control(5,1)
        print("---------stop")
        s.PIN_pwm_l.ChangeDutyCycle(0)
        s.PIN_pwm_r.ChangeDutyCycle(0)
    
    
def motor_direction_l(direction):
    #Motor 0 & Motor 2
    #direction 0/1
    offset = s.BUS.read_i2c_block_data(0x20,0x03,1)
    print('offset motor l: {}'.format(bin(offset[0])))
    if (direction == 1):
        direct = 0b00000011 + offset[0]
        
    else:
        direct = 0b00000000 + offset[0]
    
    s.BUS.write_i2c_block_data(0x20,0x02,[0b00000000])
    s.BUS.write_i2c_block_data(0x20,0x03,[direct]) #direction
    s.BUS.write_i2c_block_data(0x21,0x02,[0b00000000])
    print('motor_direction_l: {}'.format(bin(direct)))

def motor_direction_r(direction):
    offset = s.BUS.read_i2c_block_data(0x20,0x03,1)
    print('offset motor r: {}'.format(bin(offset[0])))
    
    if (direction == 1):
        direct = 0b00011000 + offset[0]
        print('motor_direction_r berechnung: {}'.format(bin(direct)))
    else:
        direct = 0b00000000 + offset[0]
    
    s.BUS.write_i2c_block_data(0x20,0x02,[0b00000000])
    s.BUS.write_i2c_block_data(0x20,0x03,[direct])
    s.BUS.write_i2c_block_data(0x21,0x02,[0b00000000])
    print('motor_direction_r: {}'.format(bin(direct)))
    

