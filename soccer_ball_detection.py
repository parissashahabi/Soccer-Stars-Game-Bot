import torch
from PIL import Image


def get_soccer_ball_position(model, img):

    results = model(img)
    results_data = results.pandas().xyxy[0]

    highest_confidence = 0
    ball_position = None

    for index, row in results_data.iterrows():
        label = row['name']  # Object label (e.g., 'player', 'ball', etc.)
        x_min, y_min, x_max, y_max = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        confidence = row['confidence']
        print(f"Object: {label}, Position: ({x_min}, {y_min}), ({x_max}, {y_max}), Confidence: {confidence}")

        if label == 'soccer_ball' and confidence > highest_confidence:
            highest_confidence = confidence
            ball_position = (x_min, y_min, x_max, y_max)

    # results.show()
    return ball_position


# model = torch.hub.load('yolov5', 'custom', path='YOLO Model/best.pt', source='local')
# img = "images/soccer stars.png"
# img = Image.open(img)
# get_soccer_ball_position(model, img)