import cv2 as cv
import numpy as np

# target = cv.imread('images/soccer stars.png', cv.IMREAD_UNCHANGED)
# template = cv.imread('images/player.png', cv.IMREAD_UNCHANGED)
#
# result = cv.matchTemplate(target, template, eval(METHODS[1]))

# --------------------Single Match--------------------
# min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

# print('Best match top left position: %s' % str(max_loc))
# print('Best match confidence: %s' % max_val)
#
# threshold = 0.8
# if max_val >= threshold:
#     template_height, template_width = template.shape[0], template.shape[1]
#     top_left = max_loc
#
#     bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
#     cv.rectangle(target, top_left, bottom_right, (0, 255, 0), 2, cv.LINE_4)
#
#     cv.imwrite('images/result.jpg', target)
#
#     # Display the result
#     cv.imshow('Template Matching Result', target)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
# else:
#     print('Template not found.')


# --------------------Multiple Match--------------------
# threshold = 0.95
# locations = np.where(result >= threshold)
# locations = list(zip(*locations[::-1]))
#
# # print(locations)
# print(len(locations))
#
# if locations:
#     template_height, template_width = template.shape[0], template.shape[1]
#     line_color = (0, 255, 0)
#     line_type = cv.LINE_4
#
#     # Loop over all the locations and draw their rectangle
#     for loc in locations:
#         # Determine the box positions
#         top_left = loc
#         bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
#         # Draw the box
#         cv.rectangle(target, top_left, bottom_right, line_color, line_type)
#
#     cv.imwrite('images/result.jpg', target)
#
#     # Display the result
#     cv.imshow('Matches', target)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
# else:
#     print('Needle not found.')


# Find Object Positions
class ObjectDetection:
    def __init__(self, template_path, method, line_color):
        self.method = eval(method)
        self.imread_flag = cv.IMREAD_UNCHANGED
        self.template = cv.imread(template_path, self.imread_flag)
        self.template_height = self.template.shape[0]
        self.template_width = self.template.shape[1]
        self.group_threshold = 2
        self.eps = 0.1
        self.line_color = line_color
        self.line_type = cv.LINE_4
        self.marker_color = (255, 0, 255)
        self.marker_type = cv.MARKER_CROSS
        self.thickness = 2
        self.marker_size = 40

    def find_objects(self, target, threshold=0.7, max_results=10):
        result = cv.matchTemplate(target, self.template, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        if not locations:
            return np.array([], np.int32).reshape(0, 4)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.template_width, self.template_height]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, self.group_threshold, self.eps)

        if len(rectangles) > max_results:
            print('Warning: too many results, raise the threshold.')
            rectangles = rectangles[:max_results]

        return rectangles

    def get_click_points(self, rectangles):
        points = []

        for (x, y, w, h) in rectangles:
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            points.append((center_x, center_y))

        return points

    def draw_rectangles(self, target, rectangles):
        for (x, y, w, h) in rectangles:
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv.rectangle(target, top_left, bottom_right, self.line_color, self.line_type, self.thickness)

        return target

    def draw_crosshairs(self, target, points):
        for (center_x, center_y) in points:
            cv.drawMarker(target, (center_x, center_y), self.marker_color, self.marker_type,  self.marker_size, self.thickness)

        return target
