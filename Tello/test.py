import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Images
img = 'https://storage.googleapis.com/petbacker/images/blog/2017/dog-and-cat-cover.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
for result in results.crop():  # or .show(), .save(), .crop(), .pandas(), etc.
    print(result['label'])