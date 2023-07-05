import cv2
import numpy
import mss
import win32gui

window_name = "BlueStacks App Player"
hwnd = win32gui.FindWindow(None, window_name)
if not hwnd:
    raise Exception('Window not found: {}'.format(window_name))

window_rect = win32gui.GetWindowRect(hwnd)
w = window_rect[2] - window_rect[0]
h = window_rect[3] - window_rect[1]

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": w, "height": h}

    while "Screen capturing":
        img = numpy.array(sct.grab(monitor))
        cv2.imshow("OpenCV/Numpy normal", img)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
