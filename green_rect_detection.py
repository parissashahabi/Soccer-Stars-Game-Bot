import cv2
import numpy as np


def detect_green_rectangle(image, line_color=(100, 50, 200), thickness=3):

    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper thresholds for green color in HSV
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    # Create a binary mask of the green region
    mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Perform morphological operations (optional)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Find the bounding rectangle around the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Draw the bounding rectangle on the original image
    cv2.rectangle(image, (x, y), (x + w, y + h), line_color, thickness)

    return image


