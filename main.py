import sys
import os
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet # Thêm dòng này

from ui.label_tool import LabelTool
from ui.bbox_panel import BBoxPanel
from config_label import SHORTCUT_LABELS

# Kiểm tra trùng lặp và phím chức năng
seen_keys = set()
RESERVED_KEYS = {'N', 'B', 'I', 'D', 'U'}

for key, label in SHORTCUT_LABELS:
    key_upper = key.upper()
    if key_upper in RESERVED_KEYS:
        print(f"Lỗi: Phím tắt '{key}' trong config_label.py trùng với phím chức năng mặc định (N, B, I, D, U)!")
        sys.exit(1)
    if key_upper in seen_keys:
        print(f"Lỗi: Phím tắt '{key}' bị trùng lặp trong config_label.py!")
        sys.exit(1)
    seen_keys.add(key_upper)

app = QApplication(sys.argv)

# Áp dụng theme tối (ví dụ: dark_teal.xml hoặc dark_amber.xml)
apply_stylesheet(app, theme='dark_teal.xml')

tool = LabelTool()
panel = BBoxPanel(tool)
tool.set_bbox_panel(panel)
tool.setMinimumSize(1400, 900)

tool.show()
panel.show()
sys.exit(app.exec())