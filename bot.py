from pyautogui import *
import time
import pyautogui
import cv2 as cv
from utils import list_window_names
from window_capture import WindowCapture

# Window Capture
wincap = WindowCapture('BlueStacks App Player')
list_window_names()

while True:
    screenshot = wincap.get_screenshot()
    cv.imshow('Computer Vision', screenshot)
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')

# Mouse Control
for _ in range(5):
    time.sleep(10)
    if pyautogui.locateOnScreen('images/player.png', confidence=0.5) is not None:
        player_loc = pyautogui.locateOnScreen('images/player.png', confidence=0.5)
        player_point = pyautogui.center(player_loc)
        player_x, player_y = player_point
        pyautogui.click(player_x, player_y)
        pyautogui.dragRel(100, 100, duration=1)
        time.sleep(0.5)
    else:
        print("can't find object.")
        time.sleep(0.5)
