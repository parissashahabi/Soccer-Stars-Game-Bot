from PIL import Image, ImageDraw
import numpy as np
import cv2
import math
import torch
import time


def calculate_angle(contours, center_x, center_y):
    max_distance = 0
    point1 = None
    point2 = None

    for contour in contours:
        for point in contour:
            x, y = point[0]
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            if distance > max_distance:
                max_distance = distance
                point1 = (x, y)
                point2 = (center_x, center_y)

    angle_rad = math.atan2(point2[1] - point1[1], point2[0] - point1[0])
    angle_deg = -1 * np.degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360

    return angle_deg, angle_rad, point1


def find_max_distance_between_points(contours):
    max_distance = 0
    point1 = None
    point2 = None

    for contour in contours:
        for i in range(len(contour)):
            for j in range(i + 1, len(contour)):
                x1, y1 = contour[i][0]
                x2, y2 = contour[j][0]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance > max_distance:
                    max_distance = distance
                    point1 = (x1, y1)
                    point2 = (x2, y2)

    return max_distance, point1, point2


def get_arrow_angle(model, img, count, offset=0):

    results = model(img)
    results_data = results.pandas().xyxy[0]

    highest_confidence = 0
    arrow_position = None

    for index, row in results_data.iterrows():
        label = row['name']
        x_min, y_min, x_max, y_max = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        confidence = row['confidence']
        print(f"Object: {label}, Position: ({x_min}, {y_min}), ({x_max}, {y_max}), Confidence: {confidence}")

        if label == 'arrow' and confidence > highest_confidence:
            highest_confidence = confidence
            arrow_position = (int(x_min), int(y_min), int(x_max), int(y_max))

    if arrow_position is not None:
        arrow_region = img.crop(arrow_position)
        arrow_region.save(f"images/arrow_cropped_{count}.png")

        hsv_image = arrow_region.convert("HSV")

        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([40, 255, 255])
        lower_orange = np.array([0, 100, 100])
        upper_orange = np.array([20, 255, 255])

        yellow_mask = np.array(hsv_image)
        yellow_mask = cv2.inRange(yellow_mask, lower_yellow, upper_yellow)
        orange_mask = np.array(hsv_image)
        orange_mask = cv2.inRange(orange_mask, lower_orange, upper_orange)

        yellow_orange_mask = cv2.bitwise_or(yellow_mask, orange_mask)
        contours, _ = cv2.findContours(yellow_orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) <= 0:
            return None, None, None, None
        max_contour = max(contours, key=cv2.contourArea)

        M = cv2.moments(max_contour)
        center_x = int(M['m10'] / M['m00'])
        center_y = int(M['m01'] / M['m00'])

        angle_deg, angle_rad, tail = calculate_angle(contours, center_x, center_y)
        print("Angle:", np.degrees(angle_rad), angle_deg)

        max_distance, point_a, point_b = find_max_distance_between_points(contours)
        print("Max Distance:", max_distance)

        force = int(max_distance - offset) * 100
        print("Force:", force)

        original_head = (arrow_position[0] + center_x, arrow_position[1] + center_y)
        original_tail = (arrow_position[0] + tail[0], arrow_position[1] + tail[1])

        # draw = ImageDraw.Draw(img)
        # draw.line([original_head, original_tail], fill="grey", width=2)  # Line between the two points
        # draw.ellipse((original_tail[0] - 3, original_tail[1] - 3, original_tail[0] + 3, original_tail[1] + 3),
        #              fill="yellow")  # Tail
        # img.show()

        # draw = ImageDraw.Draw(arrow_region)
        # draw.line([point_a, point_b], fill="grey", width=2)  # Line between the two points
        # draw.ellipse((center_x - 3, center_y - 3, center_x + 3, center_y + 3), fill="green")  # Head
        # draw.ellipse((tail[0] - 3, tail[1] - 3, tail[0] + 3, tail[1] + 3), fill="yellow")  # Tail
        # arrow_region.save("results/annotated_arrow.png")
        # # arrow_region.show()

        return angle_deg, max_distance, force, original_tail

    return None, None, None, None


# MODEL = torch.hub.load('yolov5', 'custom', path='YOLO Model/arrow/best.pt', source='local')
# start_time = time.time()
# image_path = "images/angle.png"
# image = Image.open(image_path).convert("RGB")
# offset = 5
# angle, length, force, tail = get_arrow_angle(MODEL, image, -1, offset)
# end_time = time.time()
# duration_seconds = end_time - start_time
# print("Angle Detection Duration: {:.2f} seconds".format(duration_seconds))
