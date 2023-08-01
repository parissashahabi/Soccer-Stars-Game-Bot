from rect_detection import detect_rectangle, get_rectangle
from object_detection import ObjectDetection
from soccer_ball_detection import get_soccer_ball_position
from util import get_soccer_ball_click_point, draw_soccer_ball_rectangle
import torch
import sys
import cv2 as cv
from environment import Environment


def get_state(sc, model, status):
    obj_detc_player_goal = ObjectDetection(f'images/player_goal.jpg', 'cv.TM_CCOEFF_NORMED', (255, 102, 178))
    obj_detc_opponent_goal = ObjectDetection(f'images/opponent_goal.jpg', 'cv.TM_CCOEFF_NORMED', (255, 102, 178))
    obj_detc_player = ObjectDetection('images/player.jpg', 'cv.TM_CCOEFF_NORMED', (255, 102, 178))
    obj_detc_opponent = ObjectDetection('images/opponent.jpg', 'cv.TM_CCOEFF_NORMED', (255, 102, 178))

    player_goal_rectangle = obj_detc_player_goal.find_objects(sc, 0.7)
    opponent_goal_rectangle = obj_detc_opponent_goal.find_objects(sc, 0.7)

    player_goal_position = player_goal_rectangle[0]
    opponent_goal_position = opponent_goal_rectangle[0]

    height, width, _ = sc.shape

    player_rectangles = obj_detc_player.find_objects(sc, 0.7)
    opponent_rectangles = obj_detc_opponent.find_objects_rotate(sc, 0.7)
    ball_rectangle = get_soccer_ball_position(model, sc)

    players_position = ObjectDetection.get_click_points(player_rectangles)
    opponents_position = ObjectDetection.get_click_points(opponent_rectangles)
    ball_position = get_soccer_ball_click_point(ball_rectangle)

    output_image = obj_detc_opponent_goal.draw_rectangles(sc, opponent_goal_rectangle)

    x, y, w, h = get_rectangle(output_image)
    playground = (x, y, w, h)

    game_state = (players_position, opponents_position, ball_position, tuple(player_goal_position), tuple(opponent_goal_position), tuple(playground))

    original_stdout = sys.stdout
    with open(f'simulation/state_{status}.txt', 'w') as f:
        sys.stdout = f
        print(f"Game State: {game_state}")
        sys.stdout = original_stdout

    e = Environment(game_state, 20)
    e.simulate()
    e.visualize(1, 20, 4500)


MODEL = torch.hub.load('yolov5', 'custom', path='YOLO Model/soccer_ball/best.pt', source='local')

# image_before = cv.imread("images/before.png")
# get_state(image_before, MODEL, "before")

image_after = cv.imread("images/after.png")
get_state(image_after, MODEL, "after")
