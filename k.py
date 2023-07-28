import math


# def calculate_target_point(start_x, start_y, angle_deg, force):
#     # Convert angle from degrees to radians
#     angle_rad = math.radians(angle_deg)
#
#     # Calculate horizontal and vertical components of the force
#     force_horizontal = force * math.cos(angle_rad)
#     force_vertical = force * math.sin(angle_rad)
#
#     # Calculate target position based on the starting position and components
#     target_x = start_x + force_horizontal
#     target_y = start_y - force_vertical  # Negative sign because the y-axis is inverted in screen coordinates
#
#     return target_x, target_y
#
# # Example usage: Replace start_x, start_y, angle_deg, and force with your values
# start_x = 555
# start_y = 555
# angle_deg = 47
# force = 2500/100
#
# target_x, target_y = calculate_target_point(start_x, start_y, angle_deg, force)
# print("Target Position:", target_x, target_y)
# ------------------------------------------------------------------------------------------------
import pyautogui
import math
import time

def calculate_target_point(start_x, start_y, angle_deg, force):
    # Convert angle from degrees to radians
    angle_rad = math.radians(angle_deg)

    # Calculate impulse components (x_impulse and y_impulse)
    x_impulse = math.cos(angle_rad)
    y_impulse = -math.sin(angle_rad)  # Negative sign because the y-axis is inverted in screen coordinates

    # Calculate target position based on the starting position and impulse components
    target_x = start_x + force * x_impulse
    target_y = start_y + force * y_impulse

    return target_x, target_y

def perform_drag_action(start_x, start_y, target_x, target_y, duration=2.5):
    # Step 1: Move the mouse cursor to the starting position (object position)
    pyautogui.moveTo(start_x, start_y)

    # Step 2: Press and hold the mouse button
    pyautogui.mouseDown()

    # Step 3: Drag the mouse cursor to the target position
    pyautogui.dragTo(target_x, target_y, duration=duration)

    # Step 4: Release the mouse button
    pyautogui.mouseUp()

# Example usage: Replace start_x, start_y, angle, and force with your values
start_x = 138
start_y = 360
angle = 274
force = -9859/100

  # 860.4603501690095 10193.260913924609

# Calculate target position using impulse components
target_x, target_y = calculate_target_point(start_x, start_y, angle, force)

# Perform the mouse drag action from start position to target position
perform_drag_action(start_x, start_y, target_x, target_y)
