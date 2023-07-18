import win32gui
import cv2 as cv
import numpy as np
from PIL import Image, ImageChops
import os
from matplotlib import pyplot as plt


def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(winEnumHandler, None)


def cv2_to_pil(image):
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)

    return pil_image


def pil_to_cv2(image):
    numpy_array = np.array(image)
    cv2_image = cv.cvtColor(numpy_array, cv.COLOR_RGB2BGR)

    return cv2_image


def trim(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        output_image = image.crop(bbox)
        return output_image


def resize_image(image_path, new_size, offset=0):
    image = Image.open(image_path)

    left = (image.width - new_size[0]) // 2
    top = ((image.height - new_size[1]) // 2) - offset
    right = left + new_size[0]
    bottom = top + new_size[1]

    cropped_image = image.crop((left, top, right, bottom))

    cropped_image.save(image_path)


def compare_and_resize_images(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    image1_size = image1.size[0]
    image2_size = image2.size[0]

    if image1_size < image2_size:
        resize_image(image2_path, image1.size)
    elif image1_size > image2_size:
        resize_image(image1_path, image2.size)
    else:
        pass


def match_template(target, conf):
    template_path, threshold, METHOD, lt = conf[0], conf[1], conf[2], conf[3]
    template = cv.imread(template_path)

    template_height = template.shape[0]
    template_width = template.shape[1]

    result = cv.matchTemplate(target, template, METHOD)

    if lt:
        locations = np.where(result <= threshold)
    else:
        locations = np.where(result >= threshold)

    locations = list(zip(*locations[::-1]))
    if not locations:
        return np.array([], np.int32).reshape(0, 4)

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), template_width, template_height]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 2, 0.1)

    if len(rectangles) > 10:
        print('Warning: too many results, raise the threshold.')
        rectangles = rectangles[:10]

    for (x, y, w, h) in rectangles:
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        cv.rectangle(target, top_left, bottom_right, (0, 255, 0), cv.LINE_4, 2)

    if len(rectangles) >= 1:
        return True

    return False


def is_game_started():
    return True


def is_handle_found(image_path):
    if os.path.exists(image_path):
        return True
    return False


def find_longest_string(strings):
    longest_string = ""
    longest_index = -1
    for i, string in enumerate(strings):
        if len(string) > len(longest_string):
            longest_string = string
            longest_index = i
    return longest_string, longest_index


def delete_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
        print("Image file deleted successfully.")
    else:
        print("Image file does not exist.")


def is_players_turn(image, conf):
    area_x, area_y, area_width, area_height = conf[0], conf[1], conf[2], conf[3]
    area = image[area_y:area_y+area_height, area_x:area_x+area_width]

    pil_sc = cv2_to_pil(area)
    trimmed_sc = trim(pil_sc)
    area = pil_to_cv2(trimmed_sc)

    area_gray = cv.cvtColor(area, cv.COLOR_BGR2GRAY)

    hist = cv.calcHist([area_gray], [0], None, [256], [0, 256])

    if hist[255] > 0:
        return True
    else:
        return False
