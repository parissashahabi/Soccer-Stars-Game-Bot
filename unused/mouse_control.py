import pyautogui
from pyautogui import *
import time

confidence = 0.5
duration = 1

# Mouse Control
for _ in range(5):
    time.sleep(10)
    if pyautogui.locateOnScreen('images/player.png', confidence) is not None:
        player_loc = pyautogui.locateOnScreen('images/player.png', confidence)
        player_point = pyautogui.center(player_loc)
        player_x, player_y = player_point
        pyautogui.click(player_x, player_y)
        pyautogui.dragRel(100, 100, duration)
        time.sleep(0.5)
    else:
        print("can't find object.")
        time.sleep(0.5)
