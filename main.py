import sys
import os

from PyQt6.QtWidgets import QApplication

from ui.label_tool import LabelTool
from ui.bbox_panel import BBoxPanel


app=QApplication(sys.argv)

tool=LabelTool()

panel=BBoxPanel(tool)

tool.set_bbox_panel(panel)

tool.setMinimumSize(1400,900)

tool.show()

panel.show()

sys.exit(app.exec())