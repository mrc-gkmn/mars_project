import RPi.GPIO as gpio

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
        return gpio.input(s.PIN_LT_L)

    if direction is "right":
        return gpio.input(s.PIN_LT_R)
