import cv2
import numpy as np


def save_element_screenshot(image, output_image_image, x, y, width, height):

    cropped_image = image[y:y + height, x:x + width]
    cv2.imwrite(f'images/cropped_image_{output_image_image}.png', cropped_image)

    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=37)

    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)

        x_circle, y_circle, r_circle = circles[0]

        # cv2.drawMarker(cropped_image, (x_circle, y_circle), (255, 255, 255), 10)
        screenshot = cropped_image[y_circle - r_circle:y_circle + r_circle, x_circle - r_circle:x_circle + r_circle]

        cv2.imwrite(f'images/{output_image_image}.jpg', screenshot)
        return r_circle

    else:
        print("None.")

