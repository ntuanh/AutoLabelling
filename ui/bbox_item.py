from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QComboBox
)

from config import COCO_CLASSES

class BoxItem(QWidget):
    def __init__(self,index,rect,cls,tool):

        super().__init__()

        self.index = index
        self.rect = rect
        self.cls = cls
        self.tool = tool

        main_layout = QVBoxLayout()

        index_label = QLabel(f"{index+1}")

        index_label.setStyleSheet("""
        color: #2aa3ff;
        font-size: 12px;
        font-weight: bold;
        margin-left: 6px;
        """)

        frame = QFrame()

        frame.setStyleSheet("""
        QFrame{
            border:2px solid #555;
            border-radius:6px;
            padding:6px;
            margin:6px;
            background:#1e1e1e;
        }
        """)

        layout = QVBoxLayout()

        self.class_combo = QComboBox()

        for i,name in enumerate(COCO_CLASSES):
            self.class_combo.addItem(f"{i}. {name}")

        self.class_combo.setCurrentIndex(cls)

        coords = QLabel(
            f"x1={rect.left()} y1={rect.top()} x2={rect.right()} y2={rect.bottom()}"
        )

        coords.setStyleSheet("""
        background:#2a2a2a;
        padding:6px;
        border-radius:4px;
        """)

        delete_btn = QPushButton("Delete")

        layout.addWidget(self.class_combo)
        layout.addWidget(coords)
        layout.addWidget(delete_btn)

        frame.setLayout(layout)

        main_layout.addWidget(index_label)
        main_layout.addWidget(frame)

        self.setLayout(main_layout)

        delete_btn.clicked.connect(self.delete_box)
        self.class_combo.currentIndexChanged.connect(self.change_class)

    def set_selected(self, selected):

        if selected:
            self.setStyleSheet("""
            QWidget{
                border:3px solid #2aa3ff;
                border-radius:6px;
                padding:6px;
                margin:4px;
                background:#1e1e1e;
            }
            """)

    def mousePressEvent(self, event):

        self.tool.selected_box = self.index

        if self.tool.panel:
            self.tool.panel.refresh()

        self.tool.update()

    def delete_box(self):

        self.tool.boxes.pop(self.index)

        self.tool.selected_box = None

        self.tool.save_boxes()

        if self.tool.panel:
            self.tool.panel.refresh()

        self.tool.update()

    def change_class(self, index):

        rect, _ = self.tool.boxes[self.index]

        self.tool.boxes[self.index] = (rect, index)

        self.tool.save_boxes()

        if self.tool.panel:
            self.tool.panel.refresh()

        self.tool.update()