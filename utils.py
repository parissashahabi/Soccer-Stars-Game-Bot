import win32gui
import cv2
import numpy as np
from PIL import Image, ImageChops


def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)


def cv2_to_pil(cv2_image):
    # Convert the cv2 image to RGB format
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

    # Create a PIL image from the RGB image
    pil_image = Image.fromarray(rgb_image)

    return pil_image


def pil_to_cv2(pil_image):
    # Convert the PIL image to a numpy array
    numpy_array = np.array(pil_image)

    # Convert the numpy array to a cv2 image
    cv2_image = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)

    return cv2_image


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        output_image = im.crop(bbox)
        return output_image


def crop_image_center(path, new_size, offset=5):
    # Open the image
    image = Image.open(path)

    # Calculate the crop box coordinates
    left = (image.width - new_size[0]) // 2
    top = ((image.height - new_size[1]) // 2) - offset
    right = left + new_size[0]
    bottom = top + new_size[1]

    # Crop the image to the desired size
    cropped_image = image.crop((left, top, right, bottom))

    # Save the cropped image
    cropped_image.save(path)


def compare_and_resize_images(image1_path, image2_path):
    # Open the two images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Get the sizes of the images
    image1_size = image1.size[0]
    image2_size = image2.size[0]

    # Compare the sizes of the images
    if image1_size < image2_size:
        # Resize image2 by cropping to match image1's size
        crop_image_center(image2_path, image1.size)
    elif image1_size > image2_size:
        # Resize image1 by cropping to match image2's size
        crop_image_center(image1_path, image2.size)
    else:
        pass