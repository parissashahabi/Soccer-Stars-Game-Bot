import cv2
import numpy as np


def detect_rectangle(image, line_color=(100, 50, 200), thickness=3):

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(largest_contour)

    cv2.rectangle(image, (x, y), (x + w, y + h), line_color, thickness)

    return image


