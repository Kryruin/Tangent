from io import BytesIO, StringIO
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect
from PyQt5 import QtGui
from PyQt5.Qt import *
import win32clipboard
from PIL import Image


def SendToClipboard(clipType,data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clipType,data)
    win32clipboard.CloseClipboard()
    
class ImageButton(QAbstractButton):
    def __init__(self,dcCallback, path,buttonSize, parent=None):
        super(ImageButton, self).__init__(parent)
        pixmap = QtGui.QPixmap(path)
        self.path = path
        self.extension = path[path.find('.')+1:]
        self.pixmap = pixmap
        self.pixmap_hover = pixmap
        self.pixmap_pressed = pixmap
        self.ButtonSize = buttonSize
        self.cb = dcCallback
        self.pressed.connect(self.update)
        self.released.connect(self.update)
    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed
        # print(self.pixmap.size())
        painter = QPainter(self)
        # painter.drawRect(QRect(0,0,100,100))
        painter.fillRect(QRect(0,0,self.ButtonSize,self.ButtonSize),QColor("silver"))
        painter.drawPixmap(QRect(5,5,self.ButtonSize-10,self.ButtonSize-10), pix)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        output = BytesIO()
        img = Image.open(self.path)
        img.convert("RGB").save(output,"BMP")
        data = output.getvalue()[14:]
        output.close()
        SendToClipboard(win32clipboard.CF_DIB,data)
        self.cb()
        return super().mouseDoubleClickEvent(a0)
    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()