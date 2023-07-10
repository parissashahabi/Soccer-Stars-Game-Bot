import cv2
import numpy as np


def detect_ball(image, line_color=(255, 255, 255), thickness=2):

    # Convert image to grayscale
    image_org = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image_org = cv2.threshold(image_org, 200, 255, cv2.THRESH_BINARY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(image_org, (17, 17), 0)

    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, 1.2, 100, 100, 30, 10, 40)

    if circles is not None and len(circles) <= 10:
        circles = np.round(circles[0, :]).astype(int)  # Convert circle parameters to integers

        # Select the circle with the lowest radius
        lowest_radius_circle = min(circles, key=lambda circle: circle[2])

        # Get the circle parameters
        center_x = lowest_radius_circle[0]
        center_y = lowest_radius_circle[1]
        radius = lowest_radius_circle[2]

        # Draw the detected circle
        cv2.circle(image, (center_x, center_y), radius, line_color, thickness)

    loc = (center_x, center_y)
    return loc, image