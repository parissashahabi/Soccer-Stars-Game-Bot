from pyautogui import *
from time import time
import time
import cv2 as cv
from rect_detection import detect_rectangle
from text_detection import detect_text
from utils import list_window_names, cv2_to_pil, pil_to_cv2, trim, compare_and_resize_images, match_template, \
    is_game_started, is_handle_found, delete_image
from window_capture import WindowCapture
from object_detection import ObjectDetection
from save_element_screenshot import save_element_screenshot


class GameAnalyzer:
    def __init__(self, window_name):
        self.methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
        self.method = self.methods[1]
        self.window_name = window_name
        self.player_image_path = "images/player.jpg"
        self.opponent_image_path = 'images/opponent.jpg'
        self.player_handle_image_path = "images/player_handle.jpg"   # "images/paris.jpg"
        self.window_capture = None
        self.obj_detc_player = None
        self.obj_detc_opponent = None
        self.obj_detc_opponent_goal = None
        self.obj_detc_player_goal = None
        self.obj_detc_ball = None
        self.red_rgb_code = (102, 102, 255)
        self.orange_rgb_code = (102, 178, 255)
        self.yellow_rgb_code = (102, 255, 255)
        self.green_rgb_code = (102, 255, 178)
        self.blue_rgb_code = (255, 178, 102)
        self.purple_rgb_code = (255, 102, 178)
        self.pink_rgb_code = (178, 102, 255)
        self.player_turn_conf = (self.player_handle_image_path, 0.2, cv.TM_SQDIFF_NORMED, True)

    def initialize(self):
        delete_image(self.player_handle_image_path)
        while True:
            if is_game_started():
                break
            else:
                print("Game has not started yet.")

        self.window_capture = WindowCapture(self.window_name)
        self.init_players()

        self.obj_detc_player = ObjectDetection('images/player.jpg', self.method, self.green_rgb_code)
        self.obj_detc_opponent = ObjectDetection('images/opponent.jpg', self.method, self.red_rgb_code)
        self.obj_detc_player_goal = ObjectDetection('images/player_goal.jpg', self.method, self.purple_rgb_code)
        self.obj_detc_opponent_goal = ObjectDetection('images/opponent_goal.jpg', self.method, self.blue_rgb_code)
        self.obj_detc_ball = ObjectDetection('images/ball.jpg', self.method, self.yellow_rgb_code)

        while not is_handle_found(self.player_handle_image_path):
            print("Image file does not exist.")
            # time.sleep(1.5)
            sc = self.window_capture.get_screenshot()
            result = detect_text(sc, self.player_handle_image_path)
            print("OCR Results:", result['text'])

    def init_players(self):
        sc = self.window_capture.get_screenshot()

        pil_sc = cv2_to_pil(sc)
        trimmed_sc = trim(pil_sc)
        sc = pil_to_cv2(trimmed_sc)

        height, width, _ = sc.shape
        save_element_screenshot(sc, "opponent", width // 2, 0, width // 2, height)
        save_element_screenshot(sc, "player", 0, 0, width // 2, height)
        # save_element_screenshot(sc, "ball", width // 2 - 25, 0, 55, height)

        compare_and_resize_images(self.player_image_path, self.opponent_image_path)

    def run(self):
        self.initialize()

        i = 0
        # loop_time = time()
        while True:
            sc = self.window_capture.get_screenshot()

            # checking whether it is our player's turn or not
            if match_template(sc, self.player_turn_conf):
                print(i, "Your turn.")
                i += 1

            # screenshot = cv.imread('images/soccer stars.png', cv.IMREAD_UNCHANGED)
            # cv.imshow('Computer Vision', screenshot)

            player_rectangles = self.obj_detc_player.find_objects(sc, 0.7)
            opponent_rectangles = self.obj_detc_opponent.find_objects(sc, 0.7)
            ball_rectangle = self.obj_detc_ball.find_objects(sc, 0.5)
            player_goal_rectangle = self.obj_detc_player_goal.find_objects(sc, 0.7)
            opponent_goal_rectangle = self.obj_detc_opponent_goal.find_objects(sc, 0.7)

            output_image = self.obj_detc_player.draw_rectangles(sc, player_rectangles)
            output_image = self.obj_detc_opponent.draw_rectangles(output_image, opponent_rectangles)
            output_image = self.obj_detc_ball.draw_rectangles(output_image, ball_rectangle)
            output_image = self.obj_detc_player_goal.draw_rectangles(output_image, player_goal_rectangle)
            output_image = self.obj_detc_opponent_goal.draw_rectangles(output_image, opponent_goal_rectangle)
            output_image = detect_rectangle(output_image)
            # ball_location, output_image = detect_ball(output_image)

            cv.imshow('Matches', output_image)

            # print('FPS {}'.format(1 / (time() - loop_time)))
            # loop_time = time()

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

        print('Done.')


# list_window_names()
game = GameAnalyzer("BlueStacks App Player")
game.run()
