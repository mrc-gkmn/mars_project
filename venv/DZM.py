import RPi.GPIO as gpio
import setup


def DZM_l(direction):
    DZ_l = setup.DZ_L

    if (direction == "forward"):
        DZ_l = DZ_l + 1
    if (direction == "left"):
        DZ_l = DZ_l - 1
    if (direction == "right"):
        DZ_l = DZ_l + 1
    if (direction == "stop"):
        DZ_l = DZ_l + 1

    setup.DZ_L = DZ_l


def DZM_r(direction):
    DZ_r = setup.DZ_R

    if (direction == "forward"):
        DZ_r = DZ_r + 1
    if (direction == "left"):
        DZ_r = DZ_r + 1
    if (direction == "right"):
        DZ_r = DZ_r - 1
    if (direction == "stop"):
        DZ_r = DZ_r + 1

    setup.DZ_R = DZ_r