import os

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter,QPen,QPixmap
from PyQt6.QtCore import Qt,QRect,QPoint

from config import RAW_DIR,BBOX_DIR,COCO_CLASSES
from utils.state_manager import load_state,save_state
from utils.yolo_io import load_boxes


class LabelTool(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Manual Label Tool")

        self.image_files=sorted(os.listdir(RAW_DIR))

        self.index=load_state()

        self.zoom_scale=1.0

        self.boxes=[]
        self.selected_box=None

        self.mode="insert"

        self.start_point=QPoint()
        self.end_point=QPoint()

        self.drawing=False

        self.panel=None

        self.load_frame()



    def set_bbox_panel(self,panel):

        self.panel=panel

        self.panel.refresh()



    # ----------------------------------
    # LOAD FRAME
    # ----------------------------------

    def load_frame(self):

        img_path=os.path.join(RAW_DIR,self.image_files[self.index])

        self.pixmap=QPixmap(img_path)

        self.w=self.pixmap.width()
        self.h=self.pixmap.height()

        self.boxes=load_boxes(self.image_files[self.index],self.w,self.h)

        if self.panel:
            self.panel.refresh()

        self.update()



    # ----------------------------------
    # SAVE BOXES
    # ----------------------------------

    def save_boxes(self):

        name=self.image_files[self.index].replace(".jpg",".txt")

        path=os.path.join(BBOX_DIR,name)

        with open(path,"w") as f:

            for rect,cls in self.boxes:

                x1=rect.left()
                y1=rect.top()
                x2=rect.right()
                y2=rect.bottom()

                xc=((x1+x2)/2)/self.w
                yc=((y1+y2)/2)/self.h

                w=(x2-x1)/self.w
                h=(y2-y1)/self.h

                f.write(f"{cls} {xc} {yc} {w} {h}\n")



    # ----------------------------------
    # KEYBOARD
    # ----------------------------------

    def keyPressEvent(self,event):

        if event.key()==Qt.Key.Key_I:
            self.mode="insert"

        elif event.key()==Qt.Key.Key_D:
            self.mode="delete"

        elif event.key()==Qt.Key.Key_U:

            if self.boxes:
                self.boxes.pop()

                self.save_boxes()

                if self.panel:
                    self.panel.refresh()

                self.update()


        elif event.key()==Qt.Key.Key_N:

            if self.index < len(self.image_files)-1:

                self.index+=1

                save_state(self.index)

                self.load_frame()


        elif event.key()==Qt.Key.Key_B:

            if self.index>0:

                self.index-=1

                save_state(self.index)

                self.load_frame()


        elif Qt.Key.Key_0 <= event.key() <= Qt.Key.Key_9:

            if self.selected_box is not None:

                cls=event.key()-Qt.Key.Key_0

                rect,_=self.boxes[self.selected_box]

                self.boxes[self.selected_box]=(rect,cls)

                self.save_boxes()

                if self.panel:
                    self.panel.refresh()

                self.update()



    # ----------------------------------
    # ZOOM
    # ----------------------------------

    def wheelEvent(self,event):

        if event.angleDelta().y()>0:
            self.zoom_scale*=1.1
        else:
            self.zoom_scale/=1.1

        self.update()



    # ----------------------------------
    # MOUSE
    # ----------------------------------

    def mousePressEvent(self,event):

        point=event.position().toPoint()

        point=QPoint(
            int(point.x()/self.zoom_scale),
            int(point.y()/self.zoom_scale)
        )

        for i,(rect,cls) in enumerate(self.boxes):

            if rect.contains(point):

                self.selected_box=i

                self.update()

                return


        if self.mode=="insert":

            self.start_point=point
            self.end_point=point

            self.drawing=True


        elif self.mode=="delete":

            for rect,cls in self.boxes:

                if rect.contains(point):

                    self.boxes.remove((rect,cls))

                    self.save_boxes()

                    if self.panel:
                        self.panel.refresh()

                    self.update()

                    break



    def mouseMoveEvent(self,event):

        if self.drawing:

            point=event.position().toPoint()

            point=QPoint(
                int(point.x()/self.zoom_scale),
                int(point.y()/self.zoom_scale)
            )

            self.end_point=point

            self.update()



    def mouseReleaseEvent(self,event):

        if self.drawing:

            self.drawing=False

            rect=QRect(self.start_point,self.end_point)

            self.boxes.append((rect,0))

            self.save_boxes()

            if self.panel:
                self.panel.refresh()

            self.update()



    # ----------------------------------
    # DRAW
    # ----------------------------------

    def paintEvent(self,event):

        painter=QPainter(self)

        scaled=self.pixmap.scaled(
            int(self.w*self.zoom_scale),
            int(self.h*self.zoom_scale),
            Qt.AspectRatioMode.KeepAspectRatio
        )

        painter.drawPixmap(0,0,scaled)


        for i,(rect,cls) in enumerate(self.boxes):

            x=int(rect.left()*self.zoom_scale)
            y=int(rect.top()*self.zoom_scale)
            w=int(rect.width()*self.zoom_scale)
            h=int(rect.height()*self.zoom_scale)

            scaled_rect=QRect(x,y,w,h)

            if i==self.selected_box:
                pen=QPen(Qt.GlobalColor.blue,3)
            else:
                pen=QPen(Qt.GlobalColor.red,2)

            painter.setPen(pen)

            painter.drawRect(scaled_rect)

            painter.drawText(x,y-5,COCO_CLASSES[cls])


        if self.drawing:

            rect=QRect(self.start_point,self.end_point)

            x=int(rect.left()*self.zoom_scale)
            y=int(rect.top()*self.zoom_scale)
            w=int(rect.width()*self.zoom_scale)
            h=int(rect.height()*self.zoom_scale)

            painter.setPen(QPen(Qt.GlobalColor.yellow,2))

            painter.drawRect(QRect(x,y,w,h))


        painter.setPen(QPen(Qt.GlobalColor.yellow,2))

        painter.drawText(20,30,f"Frame {self.index+1}/{len(self.image_files)}")
        painter.drawText(20,60,f"Mode: {self.mode}")
        painter.drawText(20,90,f"Boxes: {len(self.boxes)}")