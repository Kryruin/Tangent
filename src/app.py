from distutils import core
import sys
import time
from MainWindow import MainWindow
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from PyQt5.QtCore import QObject,pyqtSignal
import win32gui
import pyautogui ,keyboard
from PyQt5.QtWidgets import QMainWindow

import threading
clickOffset = (15,0)




mainThread = threading.get_ident()
#Main Application
class Tangent():
    def __init__(self) -> None:

        self.app = QApplication(sys.argv)
        self.window = MainWindow(self.PasteAndHide)
        self.lastMousePosition = [0,0]
        self.app.focusChanged.connect(self.OnFocusChangedEvent)
        self.isShowing = False
        self.window.quitAction.triggered.connect(self.app.exit)
        self.ShowWindow()
    def GetOffsetFromQuadrant(self) :
        x = self.lastMousePosition[0]
        y = self.lastMousePosition[1]
        sWidth = pyautogui.size()[0]
        sHeight = pyautogui.size()[1]
        #Default Bottom Left
        positionOffset = [30,-30]
        #Left Side
        #If x is on right side, Get the width + offset value and minus it from 
        #the mouse's position
        if x > sWidth/2:
            positionOffset[0] = -(self.window.geometry().width() + positionOffset[0])
        if y < sHeight/2: 
            positionOffset[1] = (self.window.geometry().height() - positionOffset[1])
        return positionOffset  
    def SetSignalConnection(self, obj):
        obj.sig.connect(self.ShowWindow)
    def ShowWindow(self):
        if not self.isShowing:
            # keyboard_focused = HwndWrapper(win32gui.GetForegroundWindow()).has_keyboard_focus()
            self.lastMousePosition = list(win32gui.GetCursorPos())
            self.window.MoveThenShow(list(map(lambda i,j: i+j,self.lastMousePosition,self.GetOffsetFromQuadrant())))
            self.app.focusWindow()
            self.isShowing = True
        else:
            print("Tangent is already showing")
    def HideWindow(self):
        if  self.isShowing:
            self.isShowing = False
            self.window.Hide()
        else:
            print("Tangent is already hidden")
        # self.window.showMinimized()
    def PasteAndHide(self):
        #Move back to original text box operation
        pyautogui.moveTo(tuple(map(lambda i, j: i-j,self.lastMousePosition,clickOffset)))
        pyautogui.leftClick()
        #Paste Operation
        pyautogui.keyDown('ctrl')
        pyautogui.press('v')
        pyautogui.keyUp('ctrl')
        pyautogui.press('enter')
    #Hide itself when not in focus
    def OnFocusChangedEvent(self):
        if not self.window.isActiveWindow():
            self.HideWindow()


class SignalEmitter(QObject):
    def __init__(self):
        super(QObject,self).__init__()
    sig = pyqtSignal()
    closeSig = pyqtSignal()
    def doEmit(self):
        self.sig.emit()



# https://stackoverflow.com/questions/30676599/emitting-signals-from-a-python-thread-using-qobject
if __name__ == "__main__":
    tangent = Tangent()
    sEmitter = SignalEmitter()
    tangent.SetSignalConnection(sEmitter)
    print("Application Main Window: " + threading.current_thread().name)
    print(threading.get_ident())
    keyboard.add_hotkey('alt+q', sEmitter.doEmit)
    sys.exit(tangent.app.exec())
