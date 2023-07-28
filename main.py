from pyautogui import *
from time import time
import time
import cv2 as cv
import torch
from choose_action import ChooseAction
from rect_detection import detect_rectangle, get_rectangle
from text_detection import detect_text
from util import list_window_names, cv2_to_pil, pil_to_cv2, trim, compare_and_resize_images, match_template, \
    is_game_started, is_handle_found, delete_image, is_players_turn, draw_soccer_ball_rectangle, get_soccer_ball_click_point, calculate_target_point, perform_drag_action
from window_capture import WindowCapture
from object_detection import ObjectDetection
from save_element_screenshot import save_element_screenshot
from environment import Environment
from soccer_ball_detection import get_soccer_ball_position


class GameAnalyzer:
    def __init__(self, window_name, model):
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
        # self.obj_detc_ball = None
        self.player_goal_rectangle = None
        self.opponent_goal_rectangle = None
        self.player_goal_position = None
        self.opponent_goal_position = None
        self.red_rgb_code = (102, 102, 255)
        self.orange_rgb_code = (102, 178, 255)
        self.yellow_rgb_code = (102, 255, 255)
        self.green_rgb_code = (102, 255, 178)
        self.blue_rgb_code = (255, 178, 102)
        self.purple_rgb_code = (255, 102, 178)
        self.pink_rgb_code = (178, 102, 255)
        # self.player_turn_conf = (self.player_handle_image_path, 0.2, cv.TM_SQDIFF_NORMED, True)
        self.player_turn_conf = (0, 0, None, None)
        self.playground = (0, 0, 0, 0)
        self.get_state = True
        self.game_state = None
        self.opponent_radius = 0
        self.player_radius = 0
        self.ball_radius = 0
        self.radius = 0
        self.model = model

    def initialize(self):
        while True:
            if is_game_started():
                break
            else:
                print("Game has not started yet.")

        self.window_capture = WindowCapture(self.window_name)
        sc = self.window_capture.get_screenshot()
        x, y, w, h = get_rectangle(sc)
        self.playground = (x, y, w, h)

        self.obj_detc_player_goal = ObjectDetection('images/player_goal.jpg', self.method, self.purple_rgb_code)
        self.obj_detc_opponent_goal = ObjectDetection('images/opponent_goal.jpg', self.method, self.blue_rgb_code)

        self.player_goal_rectangle = self.obj_detc_player_goal.find_objects(sc, 0.7)
        self.opponent_goal_rectangle = self.obj_detc_opponent_goal.find_objects(sc, 0.7)

        self.player_goal_position = self.player_goal_rectangle[0]
        self.opponent_goal_position = self.opponent_goal_rectangle[0]

        self.init_players()

        self.obj_detc_player = ObjectDetection('images/player.jpg', self.method, self.green_rgb_code)
        self.obj_detc_opponent = ObjectDetection('images/opponent.jpg', self.method, self.red_rgb_code)

    def init_players(self):
        sc = self.window_capture.get_screenshot()

        pil_sc = cv2_to_pil(sc)
        trimmed_sc = trim(pil_sc)
        sc = pil_to_cv2(trimmed_sc)

        height, width, _ = sc.shape
        self.opponent_radius = save_element_screenshot(sc, "opponent", self.playground[0] + self.playground[2] // 2, self.playground[1], self.playground[2] // 2, self.playground[3])
        self.player_radius = save_element_screenshot(sc, "player", self.playground[0], self.playground[1], self.playground[2] // 2, self.playground[3])
        self.ball_radius = save_element_screenshot(sc, "ball", self.playground[0] + self.playground[2] // 2 - (self.playground[2] // 26), self.playground[1], self.playground[2] // 13, self.playground[3])

        self.radius = min(self.opponent_radius, self.player_radius)

        compare_and_resize_images(self.player_image_path, self.opponent_image_path)

    def run(self):
        self.initialize()

        count = 0

        while True:
            sc = self.window_capture.get_screenshot()

            # checking whether it is our player's turn or not
            height, width, _ = sc.shape
            area_x = self.playground[0]
            area_y = 0
            area_width = self.playground[2] // 3
            area_height = height // 4

            self.player_turn_conf = (area_x, area_y, area_width, area_height)
            if is_players_turn(sc, self.player_turn_conf):
                if self.get_state is True:
                    self.get_state = False
                    count += 1
                    print("getting game state ...")

                    player_rectangles = self.obj_detc_player.find_objects(sc, 0.7)
                    opponent_rectangles = self.obj_detc_opponent.find_objects(sc, 0.7)
                    # ball_rectangle = self.obj_detc_ball.find_objects(sc, 0.7)
                    ball_rectangle = get_soccer_ball_position(self.model, sc)

                    players_position = ObjectDetection.get_click_points(player_rectangles)
                    opponents_position = ObjectDetection.get_click_points(opponent_rectangles)
                    # ball_position = ObjectDetection.get_click_points(ball_rectangle)
                    ball_position = get_soccer_ball_click_point(ball_rectangle)

                    self.game_state = (players_position, opponents_position, ball_position, tuple(self.player_goal_position), tuple(self.opponent_goal_position), tuple(self.playground))

                    # Setup Environment
                    env = Environment(self.game_state, self.radius)
                    env.simulate()
                    w, h = env.playground[2] + 2 * env.playground[0], env.playground[3] + 2 * env.playground[1]
                    Environment.capture_screenshot(env.space, w, h, f"images/env_{count}.png")

                    # Choose Best Action
                    ca = ChooseAction(45, 80, 0.9, 0.5, 90, 10000, self.game_state, self.radius)
                    ca.search()
                    ca.save_action(count)

                    # Perform Action
                    player_id, angle, force = ca.best_action.action
                    start_x, start_y = players_position[player_id - 1]
                    target_x, target_y = calculate_target_point(start_x, start_y, angle, -force/100)
                    perform_drag_action(start_x, start_y, target_x, target_y)

                    output_image = self.obj_detc_player.draw_rectangles(sc, player_rectangles)
                    output_image = self.obj_detc_opponent.draw_rectangles(output_image, opponent_rectangles)
                    # output_image = self.obj_detc_ball.draw_rectangles(output_image, ball_rectangle)
                    output_image = draw_soccer_ball_rectangle(output_image, ball_rectangle, self.yellow_rgb_code)
                    output_image = self.obj_detc_player_goal.draw_rectangles(output_image, self.player_goal_rectangle)
                    output_image = self.obj_detc_opponent_goal.draw_rectangles(output_image, self.opponent_goal_rectangle)
                    output_image = detect_rectangle(output_image)
                    # ball_location, output_image = detect_ball(output_image)
            else:
                output_image = sc
                self.get_state = True

            cv.imshow('Matches', output_image)

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break

        print('Done.')


# list_window_names()
MODEL = torch.hub.load('yolov5', 'custom', path='YOLO Model/soccer_ball/best.pt', source='local')

game = GameAnalyzer("BlueStacks App Player", MODEL)
game.run()
