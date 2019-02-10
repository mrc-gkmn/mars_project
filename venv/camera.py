import time
import cv2
import numpy as np

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
    # cv2.waitKey(1000);
    kernelOpen = np.ones((5, 5))
    kernelClose = np.ones((20, 20))

    # ret, img = cam.read()
    # img = cv2.resize(img, (340, 220))

    font = cv2.FONT_HERSHEY_SIMPLEX

    pos_arr = []

    # adding 10 extra ticks for camera to initialize
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

            # filter objects with small area
            if (area > 100):  # Just noise
                continue

            # filter objects with high y-coordinate
            elif (y_pos < 90):
                continue

            elif (area <= 100):  # Detected Object
                if (middle_x_pos > 170):
                    # no return
                    obj_list.append(["obj_leftside", middle_x_pos, middle_y_pos, y_pos, area])

                elif (middle_x_pos <= 170):
                    obj_list.append(["obj_rightside", middle_x_pos, middle_y_pos, y_pos, area])
        print("Obj detected")

        # sort for highest area object
        sorted(obj_list, key=lambda arr: arr[4])
        print(obj_list)
        print("\n")

        return obj_list, True

    elif len(position_array) < 1:
        print("No Obj detected")
        return obj_list, False
