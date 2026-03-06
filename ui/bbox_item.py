from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLineEdit,QLabel,QPushButton,QFrame
from config import COCO_CLASSES


class BoxItem(QWidget):

    def __init__(self,index,rect,cls,tool):

        super().__init__()

        self.index=index
        self.rect=rect
        self.cls=cls
        self.tool=tool


        # container frame
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

        layout=QVBoxLayout()

        # label name
        self.label_edit=QLineEdit(f"{index+1}. {COCO_CLASSES[cls]}")

        # coordinates
        coords=QLabel(
            f"x1={rect.left()} y1={rect.top()} x2={rect.right()} y2={rect.bottom()}"
        )

        delete_btn=QPushButton("Delete")

        layout.addWidget(self.label_edit)
        layout.addWidget(coords)
        layout.addWidget(delete_btn)

        frame.setLayout(layout)

        main_layout=QVBoxLayout()
        main_layout.addWidget(frame)

        self.setLayout(main_layout)

        delete_btn.clicked.connect(self.delete_box)

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

        self.tool.save_boxes()

        if self.tool.panel:
            self.tool.panel.refresh()

        self.tool.update()

    def change_class(self):

        text = self.label_edit.text()

        if "." in text:

            name = text.split(".", 1)[1].strip()

        else:

            name = text.strip()

        if name in COCO_CLASSES:
            cls = COCO_CLASSES.index(name)

            rect, _ = self.tool.boxes[self.index]

            self.tool.boxes[self.index] = (rect, cls)

            self.tool.save_boxes()

            self.tool.update()