# Manual Label Tool

Lightweight tool to **review and edit YOLO bounding boxes** generated from video frames.

---

## 1. Prepare Dataset

Run the dataset generation notebook:

https://colab.research.google.com/drive/1iFjVq-5QtHfJkEJ85zm7Kin2oJXDVqn0?usp=sharing

Download the generated dataset and **unzip it** so that your project contains:

```
datasets/
│
├── raw_data/
│   ├── frame_000001.jpg
│   └── ...
│
├── bounding_box/
│   ├── frame_000001.txt
│   └── ...
│
└── state.json
```

* **raw_data** → video frames
* **bounding_box** → YOLO labels
* **state.json** → stores last edited frame

---

## 2. Install Dependencies

```
pip install PyQt6
```

---

## 3. Run the Tool

```
python manual_labelling.py
```

The tool automatically **resumes from the last edited frame**.

---

## Controls

| Key        | Action         |
| ---------- | -------------- |
| **I**      | Insert bbox    |
| **D**      | Delete bbox    |
| **U**      | Undo           |
| **N**      | Next frame     |
| **B**      | Previous frame |
| **0-9**    | Change class   |
| **Scroll** | Zoom image     |

Click a bounding box to **select it** before changing class.

---

## YOLO Label Format

```
class_id x_center y_center width height
```

Example:

```
2 0.51 0.42 0.21 0.31
```
