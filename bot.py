from pyautogui import *
from time import time
import cv2 as cv
from rect_detection import detect_rectangle
from utils import list_window_names, cv2_to_pil, pil_to_cv2, trim, compare_and_resize_images, is_player_turn
from window_capture import WindowCapture
from object_detection import ObjectDetection
from save_element_screenshot import save_players_screenshot

METHODS = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
METHOD = METHODS[1]
WINDOW_NAME = "BlueStacks App Player"
PLAYER_HANDLE_IMAGE_PATH = "images/paris.jpg"

# list_window_names()

wincap = WindowCapture(WINDOW_NAME)
screenshot = wincap.get_screenshot()

screenshot = pil_to_cv2(trim(cv2_to_pil(screenshot)))

height, width, _ = screenshot.shape
save_players_screenshot(screenshot, "opponent", width // 2, 0, width // 2, height)
save_players_screenshot(screenshot, "player", 0, 0, width // 2, height)
# save_players_screenshot(screenshot, "ball", width // 2 - 25, 0, 55, height)

# result = filter_image_for_ocr(screenshot, PLAYER_HANDLE_IMAGE_PATH)
# print("OCR Results:", result['text'])

player_image_path = 'images/player.jpg'
opponent_image_path = 'images/opponent.jpg'
compare_and_resize_images(player_image_path, opponent_image_path)

obj_detc_player = ObjectDetection('images/player.jpg', METHOD, (0, 255, 0))
obj_detc_opponent = ObjectDetection('images/opponent.jpg', METHOD, (255, 0, 0))
obj_detc_opponent_goal = ObjectDetection('images/opponent_goal.jpg', METHOD, (0, 255, 255))
obj_detc_player_goal = ObjectDetection('images/player_goal.jpg', METHOD, (255, 255, 0))
obj_detc_ball = ObjectDetection('images/ball.jpg', METHOD, (255, 255, 255))

loop_time = time()
i = 0
while True:
    screenshot = wincap.get_screenshot()
    # if is_player_turn(screenshot, PLAYER_HANDLE_IMAGE_PATH):
    #     print(i, "Your turn.")
    #     i += 1

    # screenshot = cv.imread('images/soccer stars.png', cv.IMREAD_UNCHANGED)
    # cv.imshow('Computer Vision', screenshot)

    player_rectangles = obj_detc_player.find_objects(screenshot, 0.7)
    opponent_rectangles = obj_detc_opponent.find_objects(screenshot, 0.7)
    ball_rectangle = obj_detc_ball.find_objects(screenshot, 0.5)
    player_goal_rectangle = obj_detc_player_goal.find_objects(screenshot, 0.7)
    opponent_goal_rectangle = obj_detc_opponent_goal.find_objects(screenshot, 0.7)

    output_image = obj_detc_player.draw_rectangles(screenshot, player_rectangles)
    output_image = obj_detc_opponent.draw_rectangles(output_image, opponent_rectangles)
    output_image = obj_detc_ball.draw_rectangles(output_image, ball_rectangle)
    output_image = obj_detc_player_goal.draw_rectangles(output_image, player_goal_rectangle)
    output_image = obj_detc_opponent_goal.draw_rectangles(output_image, opponent_goal_rectangle)
    output_image = detect_rectangle(output_image)
    # ball_location, output_image = detect_ball(output_image)

    cv.imshow('Matches', output_image)

    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')

