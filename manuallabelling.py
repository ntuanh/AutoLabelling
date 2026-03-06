import sys
import os
import json

from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit
from PyQt6.QtGui import QPainter, QPen, QPixmap
from PyQt6.QtCore import Qt, QRect, QPoint


RAW_DIR = "dataset/raw_data"
BBOX_DIR = "dataset/bounding_box"

STATE_FILE = "dataset/state.json"


COCO_CLASSES = [
"person","bicycle","car","motorcycle","airplane","bus","train","truck","boat",
"traffic light","fire hydrant","stop sign","parking meter","bench","bird","cat",
"dog","horse","sheep","cow","elephant","bear","zebra","giraffe","backpack",
"umbrella","handbag","tie","suitcase","frisbee","skis","snowboard","sports ball",
"kite","baseball bat","baseball glove","skateboard","surfboard","tennis racket",
"bottle","wine glass","cup","fork","knife","spoon","bowl","banana","apple",
"sandwich","orange","broccoli","carrot","hot dog","pizza","donut","cake","chair",
"couch","potted plant","bed","dining table","toilet","tv","laptop","mouse",
"remote","keyboard","cell phone","microwave","oven","toaster","sink",
"refrigerator","book","clock","vase","scissors","teddy bear","hair drier",
"toothbrush"
]


# ===================================
# INFO WINDOW
# ===================================

class InfoWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Bounding Boxes")
        self.setGeometry(1400,100,350,900)

        self.text = QTextEdit(self)
        self.text.setGeometry(0,0,350,900)
        self.text.setReadOnly(True)

    def update_boxes(self,boxes):

        output=""

        for i,(rect,cls) in enumerate(boxes):

            output += f"{i}: {COCO_CLASSES[cls]}\n"
            output += f"x1={rect.left()} y1={rect.top()}\n"
            output += f"x2={rect.right()} y2={rect.bottom()}\n\n"

        self.text.setText(output)



# ===================================
# MAIN LABEL TOOL
# ===================================

class LabelTool(QWidget):

    def __init__(self,info_window):

        super().__init__()

        self.info_window = info_window

        self.image_files = sorted(os.listdir(RAW_DIR))

        self.zoom_scale = 1.0

        self.boxes = []
        self.selected_box = None

        self.mode = "insert"

        self.start_point = QPoint()
        self.end_point = QPoint()

        self.drawing = False

        self.load_state()

        self.load_frame()



    # ===================================
    # STATE
    # ===================================

    def load_state(self):

        if os.path.exists(STATE_FILE):

            with open(STATE_FILE) as f:

                data = json.load(f)

                self.index = data.get("current_frame",0)

        else:

            self.index = 0


    def save_state(self):

        with open(STATE_FILE,"w") as f:

            json.dump({
                "current_frame": self.index
            },f,indent=2)



    # ===================================
    # LOAD FRAME
    # ===================================

    def load_frame(self):

        img_path = os.path.join(RAW_DIR,self.image_files[self.index])

        self.pixmap = QPixmap(img_path)

        self.w = self.pixmap.width()
        self.h = self.pixmap.height()

        self.selected_box = None
        self.drawing = False

        self.load_boxes()

        self.update()

        self.info_window.update_boxes(self.boxes)



    # ===================================
    # LOAD LABEL
    # ===================================

    def load_boxes(self):

        self.boxes = []

        name = self.image_files[self.index].replace(".jpg",".txt")

        path = os.path.join(BBOX_DIR,name)

        if not os.path.exists(path):
            return

        with open(path) as f:

            for line in f.readlines():

                cls,xc,yc,w,h = map(float,line.split())

                x1 = (xc-w/2)*self.w
                y1 = (yc-h/2)*self.h
                x2 = (xc+w/2)*self.w
                y2 = (yc+h/2)*self.h

                rect = QRect(int(x1),int(y1),int(x2-x1),int(y2-y1))

                self.boxes.append((rect,int(cls)))



    # ===================================
    # SAVE LABEL
    # ===================================

    def save_boxes(self):

        name = self.image_files[self.index].replace(".jpg",".txt")

        path = os.path.join(BBOX_DIR,name)

        with open(path,"w") as f:

            for rect,cls in self.boxes:

                x1 = rect.left()
                y1 = rect.top()
                x2 = rect.right()
                y2 = rect.bottom()

                xc = ((x1+x2)/2)/self.w
                yc = ((y1+y2)/2)/self.h

                w = (x2-x1)/self.w
                h = (y2-y1)/self.h

                f.write(f"{cls} {xc} {yc} {w} {h}\n")



    # ===================================
    # KEYBOARD
    # ===================================

    def keyPressEvent(self,event):

        if event.key()==Qt.Key.Key_I:
            self.mode="insert"

        elif event.key()==Qt.Key.Key_D:
            self.mode="delete"

        elif event.key()==Qt.Key.Key_U:

            if self.boxes:

                self.boxes.pop()

                self.save_boxes()

                self.update()


        elif event.key()==Qt.Key.Key_N:

            if self.index < len(self.image_files)-1:

                self.index += 1

                self.save_state()

                self.load_frame()


        elif event.key()==Qt.Key.Key_B:

            if self.index > 0:

                self.index -= 1

                self.save_state()

                self.load_frame()


        elif Qt.Key.Key_0 <= event.key() <= Qt.Key.Key_9:

            if self.selected_box is not None:

                cls = event.key()-Qt.Key.Key_0

                rect,_ = self.boxes[self.selected_box]

                self.boxes[self.selected_box] = (rect,cls)

                self.save_boxes()

                self.update()

                self.info_window.update_boxes(self.boxes)



    # ===================================
    # ZOOM
    # ===================================

    def wheelEvent(self,event):

        if event.angleDelta().y() > 0:
            self.zoom_scale *= 1.1
        else:
            self.zoom_scale /= 1.1

        self.update()



    # ===================================
    # MOUSE
    # ===================================

    def mousePressEvent(self,event):

        point = event.position().toPoint()

        point = QPoint(
            int(point.x()/self.zoom_scale),
            int(point.y()/self.zoom_scale)
        )

        for i,(rect,cls) in enumerate(self.boxes):

            if rect.contains(point):

                self.selected_box = i

                self.update()

                return


        if self.mode=="insert":

            self.start_point = point
            self.end_point = point

            self.drawing = True


        elif self.mode=="delete":

            for rect,cls in self.boxes:

                if rect.contains(point):

                    self.boxes.remove((rect,cls))

                    self.save_boxes()

                    self.update()

                    self.info_window.update_boxes(self.boxes)

                    break



    def mouseMoveEvent(self,event):

        if self.drawing:

            point = event.position().toPoint()

            point = QPoint(
                int(point.x()/self.zoom_scale),
                int(point.y()/self.zoom_scale)
            )

            self.end_point = point

            self.update()



    def mouseReleaseEvent(self,event):

        if self.drawing:

            self.drawing = False

            rect = QRect(self.start_point,self.end_point)

            self.boxes.append((rect,0))

            self.save_boxes()

            self.update()

            self.info_window.update_boxes(self.boxes)



    # ===================================
    # DRAW
    # ===================================

    def paintEvent(self,event):

        painter = QPainter(self)

        scaled = self.pixmap.scaled(
            int(self.w*self.zoom_scale),
            int(self.h*self.zoom_scale),
            Qt.AspectRatioMode.KeepAspectRatio
        )

        painter.drawPixmap(0,0,scaled)


        for i,(rect,cls) in enumerate(self.boxes):

            x = int(rect.left()*self.zoom_scale)
            y = int(rect.top()*self.zoom_scale)
            w = int(rect.width()*self.zoom_scale)
            h = int(rect.height()*self.zoom_scale)

            scaled_rect = QRect(x,y,w,h)

            if i == self.selected_box:
                pen = QPen(Qt.GlobalColor.green,3)
            else:
                pen = QPen(Qt.GlobalColor.red,2)

            painter.setPen(pen)

            painter.drawRect(scaled_rect)

            painter.drawText(x,y-5,COCO_CLASSES[cls])


        if self.drawing:

            rect = QRect(self.start_point,self.end_point)

            x = int(rect.left()*self.zoom_scale)
            y = int(rect.top()*self.zoom_scale)
            w = int(rect.width()*self.zoom_scale)
            h = int(rect.height()*self.zoom_scale)

            painter.setPen(QPen(Qt.GlobalColor.blue,2))

            painter.drawRect(QRect(x,y,w,h))


        painter.setPen(QPen(Qt.GlobalColor.yellow,2))

        painter.drawText(20,30,f"Frame {self.index+1}/{len(self.image_files)}")
        painter.drawText(20,60,f"Mode: {self.mode}")
        painter.drawText(20,90,f"Boxes: {len(self.boxes)}")



# ===================================
# MAIN
# ===================================

app = QApplication(sys.argv)

info_window = InfoWindow()

main_window = LabelTool(info_window)

main_window.setWindowTitle("Manual Label Tool")

main_window.setGeometry(100,100,1300,900)

main_window.show()

info_window.show()

sys.exit(app.exec())