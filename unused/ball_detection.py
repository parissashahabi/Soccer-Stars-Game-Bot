import cv2
import numpy as np


def detect_ball(image, line_color=(255, 255, 255), thickness=2):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    blurred_image = cv2.GaussianBlur(binary, (17, 17), 0)

    circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, 1.2, 100, 100, 30, 10, 40)

    location = None

    if circles is not None and len(circles) <= 10:
        circles = np.round(circles[0, :]).astype(int)
        lowest_radius_circle = min(circles, key=lambda circle: circle[2])

        center_x = lowest_radius_circle[0]
        center_y = lowest_radius_circle[1]
        radius = lowest_radius_circle[2]

        cv2.circle(image, (center_x, center_y), radius, line_color, thickness)
        location = (center_x, center_y)

    return location, image
