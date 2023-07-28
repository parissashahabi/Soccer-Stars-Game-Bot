import time

import cv2
import pytesseract

from util import find_longest_string

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def detect_text(image, output_image_path):

    height, width, _ = image.shape
    cropped_image = image[height//8:height//4, width//8:width//3]
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    results = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)
    num_boxes = len(results['text'])
    _, i = find_longest_string(results['text'])

    x, y, w, h = results['left'][i], results['top'][i], results['width'][i], results['height'][i]
    conf = int(results['conf'][i])
    text = results['text'][i]
    if conf > 0 and text.strip() != "":
        x -= 5
        y -= 5
        w += 10
        h += 10

        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        text_screenshot = cropped_image[y:y+h, x:x+w]
        cv2.imwrite(output_image_path, text_screenshot)

    return results
