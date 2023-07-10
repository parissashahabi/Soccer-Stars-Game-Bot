import cv2
import numpy as np


def detect_and_save_players(image, file_name, x, y, width, height):

    # Crop the image to the specified area
    cropped_image = image[y:y+height, x:x+width]
    # cv2.imwrite(f'images/cropped_image_{file_name}.png', cropped_image)

    # Convert the cropped image to grayscale
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Apply Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=40)

    print(len(circles))
    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)  # Convert circle parameters to integers

        # Take a screenshot of the first circle found
        x_circle, y_circle, r_circle = circles[0]
        print(x_circle, y_circle, r_circle)
        # cv2.drawMarker(cropped_image, (x_circle, y_circle), (255, 255, 255), 10)
        screenshot = cropped_image[y_circle-r_circle:y_circle+r_circle, x_circle-r_circle:x_circle+r_circle]

        # Save the screenshot
        cv2.imwrite(f'images/{file_name}.jpg', screenshot)

    else:
        print("None.")

