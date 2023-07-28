from pyautogui import *
import time
import cv2 as cv
from window_capture import WindowCapture


window_capture = WindowCapture("BlueStacks App Player")
count = 1000

while True:
    sc = window_capture.get_screenshot()
    cv.imwrite(f'dataset/sample_image_{count}.png', sc)
    cv.imshow('Samples', sc)
    count += 1
    time.sleep(1)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
