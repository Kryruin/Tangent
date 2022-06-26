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
# from pywinauto.controls.hwndwrapper import HwndWrapper
# from ctypes import LibraryLoader,WinDLL
# https://gitpress.io/u/1155/pyqt-example-MinimizeToTray
# https://stackoverflow.com/questions/12781059/how-to-know-if-the-keyboard-is-active-on-a-text-input/13448409#13448409
# https://stackoverflow.com/questions/59884688/getguithreadinfo-with-pywin32
# https://github.com/boppreh/keyboard
# https://stackoverflow.com/questions/12781059/how-to-know-if-the
# -keyboard-is-active-on-a-text-input/13448409#13448409
# https://pywinauto.readthedocs.io/en/latest/getting_started.html
#https://www.youtube.com/watch?v=lTJ-QkC_Sxw&ab_channel=KDAB
#https://stackoverflow.com/questions/49331513/calling-a-method-from-inside-a-thread-to-another-class-in-python-pyqt
clickOffset = (15,0)
# GetWindowThreadProcessId.restype = wintypes.DWORD
# windll = LibraryLoader(WinDLL)
# GetWindowThreadProcessId.argtypes = [
#     wintypes.HWND,
#     POINTER(wintypes.DWORD),
# ]
# def HasKeyboardFocus():
#     windll.user32.GetWindowThreadProcessId()
#     control_thread = windll.user32.GetWindowThreadProcessId(self.handle, None)
#     win32process.AttachThreadInput(control_thread, win32api.GetCurrentThreadId(), 1)
#     focused = win32gui.GetFocus()
#     win32process.AttachThreadInput(control_thread, win32api.GetCurrentThreadId(), 0)

#     win32functions.WaitGuiThreadIdle(handle)

#     return self.handle == focused
# print("Application Main Window: " + threading.current_thread().name)
# print(threading.get_ident())



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
        obj.closeSig.connect(self.window.close)
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
    def doCloseEmit(self):
        self.closeSig.emit()


# https://stackoverflow.com/questions/30676599/emitting-signals-from-a-python-thread-using-qobject
if __name__ == "__main__":
    tangent = Tangent()
    sEmitter = SignalEmitter()
    tangent.SetSignalConnection(sEmitter)
    print("Application Main Window: " + threading.current_thread().name)
    print(threading.get_ident())
    keyboard.add_hotkey('alt+q', sEmitter.doEmit)
    keyboard.add_hotkey('alt+w', sEmitter.doCloseEmit)
    sys.exit(tangent.app.exec())
