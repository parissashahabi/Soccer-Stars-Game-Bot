import torch
from PIL import Image

# Load the YOLOv5 model
model = torch.hub.load('YOLO Model/yolov5', 'custom', path='YOLO Model/best.pt', source='local')

# Load the input image
img_path = 'images/soccer stars 2.png'
img = Image.open(img_path)

# Perform object detection on the input image
results = model(img)

# Get the bounding box coordinates (positions) and confidence scores
results_data = results.pandas().xyxy[0]

# Iterate through the results to get the positions of each detected object
for index, row in results_data.iterrows():
    label = row['name']  # Object label (e.g., 'player', 'ball', etc.)
    x_min, y_min, x_max, y_max = row['xmin'], row['ymin'], row['xmax'], row['ymax']
    confidence = row['confidence']  # Confidence score of the detection

    # Do something with the position information (e.g., print or use it in your game simulation)
    print(f"Object: {label}, Position: ({x_min}, {y_min}), ({x_max}, {y_max}), Confidence: {confidence}")

# Show the annotated image with bounding boxes
results.show()
