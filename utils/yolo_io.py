import os
from PyQt6.QtCore import QRect
from config import BBOX_DIR


def load_boxes(image_name,w,h):

    boxes=[]

    name=image_name.replace(".jpg",".txt")

    path=os.path.join(BBOX_DIR,name)

    if not os.path.exists(path):
        return boxes

    with open(path) as f:

        for line in f.readlines():

            cls,xc,yc,bw,bh=map(float,line.split())

            x1=(xc-bw/2)*w
            y1=(yc-bh/2)*h
            x2=(xc+bw/2)*w
            y2=(yc+bh/2)*h

            rect=QRect(int(x1),int(y1),int(x2-x1),int(y2-y1))

            boxes.append((rect,int(cls)))

    return boxes