from PyQt6.QtWidgets import QWidget,QVBoxLayout,QScrollArea
from ui.bbox_item import BoxItem


class BBoxPanel(QWidget):

    def __init__(self,tool):

        super().__init__()

        self.tool=tool

        self.setWindowTitle("Bounding Boxes")
        self.setGeometry(1400,100,350,900)

        self.layout=QVBoxLayout()

        self.container=QWidget()
        self.container.setLayout(self.layout)

        scroll=QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.container)

        main=QVBoxLayout()
        main.addWidget(scroll)

        self.setLayout(main)


    def refresh(self):

        for i in reversed(range(self.layout.count())):

            self.layout.itemAt(i).widget().deleteLater()

        for i,(rect,cls) in enumerate(self.tool.boxes):

            item=BoxItem(i,rect,cls,self.tool)

            self.layout.addWidget(item)