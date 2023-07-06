import cv2
import numpy as np


def detect_ball(image, minRadius, maxRadius, line_color=(255, 255, 255), thickness=2):

    # Convert image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

    # Apply Hough Circle Transform
    circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, 1, 50, 30, 100, minRadius, maxRadius)

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
