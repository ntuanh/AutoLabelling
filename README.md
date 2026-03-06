# Manual Video Label Tool

A lightweight **manual annotation tool** to review and correct YOLO bounding boxes generated from video frames.

The tool allows you to quickly **navigate frames, edit labels, delete objects, and visualize all objects in a frame** using a bounding box panel.

---

# 1. Prepare Dataset

Run the dataset generation notebook:

https://colab.research.google.com/drive/1iFjVq-5QtHfJkEJ85zm7Kin2oJXDVqn0?usp=sharing

Download the generated dataset and **unzip it** ( create **dataset** directory) so the project structure becomes:

```text
dataset/
│
├── raw_data/
│   ├── frame_000001.jpg
│   ├── frame_000002.jpg
│   └── ...
│
├── bounding_box/
│   ├── frame_000001.txt
│   ├── frame_000002.txt
│   └── ...
│
└── state.json
```

* **raw_data** → video frames
* **bounding_box** → YOLO labels
* **state.json** → stores the last labeled frame

---

# 2. Install Dependencies

Create a Python environment and install PyQt:

```bash
pip install PyQt6
```

---

# 3. Run the Tool

```bash
python main.py
```

The tool will automatically:

* Load frames from `dataset/raw_data`
* Load YOLO labels from `dataset/bounding_box`
* Resume from the last labeled frame using `state.json`

---

# Interface Overview

### Main Window

Displays the current frame and bounding boxes.

Each object is labeled with:

```
index. class_name
```

Example:

```
1. truck
2. car
3. bus
```

---

### Bounding Box Panel

The right panel displays all objects in the current frame.

Each object appears as a **card** containing:

* object index
* class selector (dropdown)
* coordinates
* delete button

Example:

```
1
┌──────────────────────┐
[7. truck ▼]
x1=70 y1=281 x2=309 y2=449
[Delete]
└──────────────────────┘
```

Selecting a card highlights the corresponding bounding box in the image.

---

# Controls

### Frame Navigation

| Key | Action         |
| --- | -------------- |
| N   | Next frame     |
| B   | Previous frame |

---

### Annotation

| Key | Action              |
| --- | ------------------- |
| I   | Insert bounding box |
| D   | Delete bounding box |
| U   | Undo last box       |

---

### Object Editing

* Click an object card to select it
* Use the dropdown to change the class
* Click **Delete** to remove the object

---

# YOLO Label Format

Each label file uses YOLO format:

```
class_id x_center y_center width height
```

Example:

```
7 0.512 0.421 0.215 0.314
```

Values are normalized between **0 and 1**.

---

# Resume Labeling

The tool automatically saves the current frame index in:

```
dataset/state.json
```

Example:

```json
{
  "current_frame": 120
}
```

When restarting the tool, labeling resumes from that frame.

---

# Typical Workflow

1. Run the Colab notebook to generate frames and initial YOLO labels.
2. Unzip the dataset into the `dataset/` folder.
3. Run the labeling tool.
4. Review and correct bounding boxes.

This workflow combines **automatic detection + manual correction** to significantly speed up dataset creation.
