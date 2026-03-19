import os
import cv2
import torch
from ultralytics import YOLO

MODEL_PATH = "yolo11n.pt"
VIDEO_PATH = "video.mp4"
OUTPUT_DIR = "dataset/predictions"
CONF_THRES = 0.25

device = "cuda" if torch.cuda.is_available() else "cpu"

os.makedirs(OUTPUT_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

cap = cv2.VideoCapture(VIDEO_PATH)
frame_id = 1

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    results = model(frame, conf=CONF_THRES, device=device)[0]

    output_file = os.path.join(OUTPUT_DIR, f"frame_{frame_id:06d}.txt")

    with open(output_file, "w") as f:

        if results.boxes is not None:

            boxes = results.boxes.xyxy.cpu().numpy()
            confs = results.boxes.conf.cpu().numpy()
            classes = results.boxes.cls.cpu().numpy().astype(int)

            for i in range(len(boxes)):

                x1, y1, x2, y2 = boxes[i]

                cx = ((x1 + x2) / 2) / w
                cy = ((y1 + y2) / 2) / h
                bw = (x2 - x1) / w
                bh = (y2 - y1) / h

                f.write(f"{classes[i]} {cx} {cy} {bw} {bh} {confs[i]}\n")

    frame_id += 1

cap.release()

print("Done.")