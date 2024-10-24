import cv2
import numpy as np

def detect_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color mask
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Blue color mask
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # Green color mask
    lower_green = np.array([36, 25, 25])
    upper_green = np.array([70, 255, 255])
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

    return red_mask, blue_mask, green_mask
