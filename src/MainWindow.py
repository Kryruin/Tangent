from ctypes import alignment
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow, QSystemTrayIcon, QAction,QMenu,QStyle)
from ImageButton import ImageButton
import os
mainPath = "C:/Users/Admin/Desktop/Reactions"
dirList = os.listdir(mainPath)
buttonSize = 100
#how much padding in comparison to width of the window
#0.1 is 10% of width()
#to calculate dimensions, get w/h and minus off (2* paddingVal)
paddingPerc = 0.01
spacing =12



class MainWindow(QMainWindow):
    def __init__(self, buttonCB) -> None:
        super(MainWindow,self).__init__()
        self.setGeometry(0,0,(buttonSize * 4) + (spacing *5)+40,520)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.cb = buttonCB
        self.initUI()
        self.initTraySettings()
    def MoveThenShow(self,pos):
        self.move(pos[0],pos[1]-self.geometry().height())
        # Qt::WindowNoState	
        # Qt::WindowMinimized	
        # Qt::WindowMaximized
        # Qt::WindowFullScreen	
        # Qt::WindowActive
        self.setWindowState(QtCore.Qt.WindowMinimized)
        self.show()
        self.setWindowState(QtCore.Qt.WindowNoState)
    def Hide(self):
        self.hide()
    def initTraySettings(self): 
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(
            self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        #Setting the actions
        self.quitAction = QAction("Close",self)
        #Set up the tray menu and add the actions
        self.trayMenu = QMenu()
        self.trayMenu.addAction(self.quitAction)
        #Set the menu of the tray icon in the icon bar
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()
        pass
    def initUI(self):
        #create scroll view
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("CentralWidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)
        w = self.geometry().width()
        h = self.geometry().height()
        #scroll area dimension
        dim = QtCore.QRect(paddingPerc * w,paddingPerc * h, 
                            w - (paddingPerc * w * 2),h - (paddingPerc * h * 2))
        #set scroll area dimensions to fit the window
        self.scrollArea.setGeometry(dim)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Panel)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(spacing)
        #Set alignment
        self.scrollArea.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter )
        self.geometry().setWidth( self.geometry().width() +
        self.scrollArea.verticalScrollBar().geometry().width())
        numPerRow = 4
        # math.floor(dim.width() / buttonSize)-1
        i = 0
        # temp = self.createButton(self.scrollAreaWidgetContents,'Liu.jpg')
        # x = i%numPerRow
        # y = i/numPerRow
        # self.gridLayout.addWidget(temp, y,x)
        for file in dirList:
            path = mainPath + "/" + file
            if path[path.find('.')+1:] != "jpg" and path[path.find('.')+1:] != "png":
                print("invalid")
                continue
            button = self.createButton(self.scrollAreaWidgetContents,path)
            x = i%numPerRow
            y = i/numPerRow
            self.gridLayout.addWidget(button, y,x)
            i+=1
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.setCentralWidget(self.centralWidget)
        #create buttons
    def createButton(self, widgetParent,path):
        # newPix = QtGui.QPixmap(os.getcwd() + "/Tangent/" + "resources/images/Test.jpg")
        newButton = ImageButton(self.cb,path,buttonSize,widgetParent)
        # newButton = QtWidgets.QPushButton(widgetParent)
        # newButton.setIcon(QtGui.QIcon(path))
        # newButton.setStyleSheet("background-image : url(Liu.jpg);")
        #Set buttons

        newButton.setObjectName("Button")
        newButton.setFixedSize(buttonSize,buttonSize)
        return newButton



    