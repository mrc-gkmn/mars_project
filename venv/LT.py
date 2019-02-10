import RPi.GPIO as gpio
import setup as s
import time

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
    #LT_status_all = LT_measure("all")


    return LT_status_l, LT_status_r


def LT_measure(direction):
    """
    Method to calculate values for each LT (left, right)
    :param direction: determines the asked for direction
    :return: returns just the value for the asked for direction (just left, just right)
    """
    if direction is "right":
        s.switcher1([0,1,1])
        time.sleep(0.05)
        return gpio.input(s.PIN_BANK_1_INPUT)

    if direction is "left":
        s.switcher1([1,1,1])
        time.sleep(0.05)
        return gpio.input(s.PIN_BANK_0_INPUT)
    
    if direction is "all":
        array = []
        s.switcher0(s.n0)
        array.append(gpio.input(s.n0))
        
        s.switcher0(s.n1)
        array.append(gpio.input(s.n1))
        
        s.switcher0(s.n2)
        array.append(gpio.input(s.n2))
        
        s.switcher0(s.n3)
        array.append(gpio.input(s.n3))
        
        s.switcher0(s.n4)
        array.append(gpio.input(s.n4))
        
        s.switcher0(s.n5)
        array.append(gpio.input(s.n5))
        
        s.switcher0(s.n6)
        array.append(gpio.input(s.n6))
        
        s.switcher0(s.n7)
        array.append(gpio.input(s.n7))
        
        print(str(array))
        
        #return array
        
while(True):        
    l, r = LT()
    print("Links: " + str(l))
    print("Rechts: " + str(r))
