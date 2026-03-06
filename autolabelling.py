# if run on colab !pip -q install -U ultralytics opencv-python tqdm
# colab link https://colab.research.google.com/drive/1iFjVq-5QtHfJkEJ85zm7Kin2oJXDVqn0?usp=sharing

import cv2
import os
import torch
from ultralytics import YOLO
from tqdm import tqdm

# ======================
# CONFIG
# ======================

video_path = "video_1.mp4"

raw_dir = "dataset/raw_data"
bbox_dir = "dataset/bounding_box"

os.makedirs(raw_dir, exist_ok=True)
os.makedirs(bbox_dir, exist_ok=True)

# ======================
# LOAD MODEL (GPU)
# ======================

device = 0 if torch.cuda.is_available() else "cpu"

model = YOLO("yolo26x.pt")
model.to(device)

# ======================
# VIDEO INFO
# ======================

cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

frame_id = 0

pbar = tqdm(total=total_frames, desc="Processing video")

# ======================
# PROCESS VIDEO
# ======================

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    frame_name = f"frame_{frame_id:06d}.jpg"
    txt_name = f"frame_{frame_id:06d}.txt"

    img_path = os.path.join(raw_dir, frame_name)
    txt_path = os.path.join(bbox_dir, txt_name)

    # save frame
    cv2.imwrite(img_path, frame)

    # ======================
    # YOLO INFERENCE
    # ======================

    results = model(frame, device=device, conf=0.5)

    h, w, _ = frame.shape

    with open(txt_path, "w") as f:

        for r in results:

            if r.boxes is None:
                continue

            for box in r.boxes:

                cls = int(box.cls[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                # convert to YOLO format
                x_center = ((x1 + x2) / 2) / w
                y_center = ((y1 + y2) / 2) / h
                width = (x2 - x1) / w
                height = (y2 - y1) / h

                f.write(f"{cls} {x_center} {y_center} {width} {height}\n")

    pbar.update(1)

cap.release()
pbar.close()

print("Dataset generation finished")