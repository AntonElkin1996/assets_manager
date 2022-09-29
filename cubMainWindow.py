from PyQt5 import QtCore, QtGui, QtWidgets
from iconsManager import Ui_IconsWindow
from bundleManager import Ui_bundleSetup
from soundManager import Ui_SoundManager
from particlesManager import Ui_ParticlesWindow
from converters import Ui_Converters
from svnWorkspaceSync import Ui_SvnWorkspaceSync
from managerPaths import Paths
from staticMethods import StaticMethods


class MainWindowResizableRepaint(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.currWidth = (self.size().width() // 150) - 2

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if ((self.size().width() // 150) - 2) != self.currWidth:
            self.resized.emit()
            self.currWidth = ((self.size().width() // 150) - 2)
        return super(MainWindowResizableRepaint, self).resizeEvent(a0)

class MainWindowToQuit(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowToQuit, self).__init__()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        app.quit()

class Ui_MainWindow(object):
    def __init__(self, win, dir):
        self.setupUi(win, dir)
        win.show()

    def openWindow(self, ui):
        if ui == Ui_bundleSetup:
            self.win = QtWidgets.QMainWindow()
            Ui_bundleSetup(self.win)
        elif ui == Ui_IconsWindow:
            self.win = MainWindowResizableRepaint()
            Ui_IconsWindow(self.win)
        elif ui == Ui_SoundManager:
            self.win = QtWidgets.QMainWindow()
            Ui_SoundManager(self.win)
        elif ui == Ui_ParticlesWindow:
            self.win = QtWidgets.QMainWindow()
            Ui_ParticlesWindow(self.win)
        elif ui == Ui_Converters:
            self.win = QtWidgets.QMainWindow()
            Ui_Converters(self.win, app)
        elif ui == Ui_SvnWorkspaceSync:
            self.win = QtWidgets.QMainWindow()
            Ui_SvnWorkspaceSync(self.win, app)


    def setupUi(self, mainWindow, dir):
        mainWindow.setObjectName('mainWindow')
        mainWindow.resize(300, 370)
        mainWindow.setWindowTitle('Main Window - ' + dir)
        mainWindow.move(100, 100)

        self.mainWindow = mainWindow
        self.centralWidget = QtWidgets.QWidget(mainWindow)
        self.centralWidget.setObjectName('centralWidget')
        self.centralWidget.setMinimumWidth(320)

        self.centralLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.dirLabel = QtWidgets.QLabel(self.centralWidget)
        self.dirLabel.setObjectName('dirLabel')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeHead(app))
        self.dirLabel.setFont(font)
        self.dirLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dirLabel.setText(dir.capitalize())
        self.dirLabel.setMaximumHeight(150)
        self.dirLabel.setMinimumHeight(100)
        self.dirLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.buttonsWidget = QtWidgets.QWidget(self.centralWidget)
        self.buttonsWidget.setObjectName('buttonsWidget')
        self.buttonsWidget.setMinimumHeight(300)

        self.buttonsLayout = QtWidgets.QVBoxLayout(self.buttonsWidget)
        self.buttonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.buttonsLayout.setObjectName('buttonsLayout')

        self.bundleManagerButton = QtWidgets.QPushButton()
        self.bundleManagerButton.setObjectName('bundleManagerButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(app))
        self.bundleManagerButton.setFont(font)
        self.bundleManagerButton.setText('BUNDLE MANAGER')
        self.bundleManagerButton.setMinimumHeight(35)
        self.bundleManagerButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.bundleManagerButton.clicked.connect(lambda: self.openWindow(Ui_bundleSetup))

        self.iconsManagerButton = QtWidgets.QPushButton()
        self.iconsManagerButton.setObjectName('iconsManagerButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(app))
        self.iconsManagerButton.setFont(font)
        self.iconsManagerButton.setText('ICONS MANAGER')
        self.iconsManagerButton.setMinimumHeight(35)
        self.iconsManagerButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.iconsManagerButton.clicked.connect(lambda: self.openWindow(Ui_IconsWindow))

        self.soundManagerButton = QtWidgets.QPushButton()
        self.soundManagerButton.setObjectName('soundManagerButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(app))
        self.soundManagerButton.setFont(font)
        self.soundManagerButton.setText('SOUND MANAGER')
        self.soundManagerButton.setMinimumHeight(35)
        self.soundManagerButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.particlesManagerButton = QtWidgets.QPushButton()
        self.particlesManagerButton.setObjectName('particlesManagerButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(app))
        self.particlesManagerButton.setFont(font)
        self.particlesManagerButton.setText('PARTICLES MANAGER')
        self.particlesManagerButton.setMinimumHeight(35)
        self.particlesManagerButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.particlesManagerButton.clicked.connect(lambda: self.openWindow(Ui_ParticlesWindow))

        self.convertersManagerButton = QtWidgets.QPushButton()
        self.convertersManagerButton.setObjectName('convertersManagerButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(app))
        self.convertersManagerButton.setFont(font)
        self.convertersManagerButton.setText('CONVERTERS')
        self.convertersManagerButton.setMinimumHeight(35)
        self.convertersManagerButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.convertersManagerButton.clicked.connect(lambda: self.openWindow(Ui_Converters))

        self.svnSyncWorkspaceButton = QtWidgets.QPushButton()
        self.svnSyncWorkspaceButton.setObjectName('svnSyncWorkspaceButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(app))
        self.svnSyncWorkspaceButton.setFont(font)
        self.svnSyncWorkspaceButton.setText('SVN WORKSPACE SYNC')
        self.svnSyncWorkspaceButton.setMinimumHeight(35)
        self.svnSyncWorkspaceButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.svnSyncWorkspaceButton.clicked.connect(lambda: self.openWindow(Ui_SvnWorkspaceSync))

        self.buttonsLayout.addWidget(self.bundleManagerButton)
        self.buttonsLayout.addWidget(self.iconsManagerButton)
        self.buttonsLayout.addWidget(self.soundManagerButton)
        self.buttonsLayout.addWidget(self.particlesManagerButton)
        self.buttonsLayout.addWidget(self.convertersManagerButton)
        self.buttonsLayout.addWidget(self.svnSyncWorkspaceButton)
        self.buttonsWidget.setLayout(self.buttonsLayout)

        self.centralLayout.addWidget(self.dirLabel)
        self.centralLayout.addWidget(self.buttonsWidget)
        self.centralWidget.setLayout(self.centralLayout)

        mainWindow.setCentralWidget(self.centralWidget)

class UiGetPath(object):
    def __init__(self, win):
        self.screenRect = app.desktop().screenGeometry()
        self.screenW = self.screenRect.width()
        self.screenH = self.screenRect.height()
        self.pathToWorkspace = os.path.join(os.getcwd(), 'Art_workspace')
        self.setupUi(win)
        self.currWin = win

    def openMainWin(self, dir):
        self.win = MainWindowToQuit()
        Ui_MainWindow(self.win, dir)
        Paths.getDir(dir)
        self.currWin.close()


    def setupUi(self, getPathWindow):
        getPathWindow.setObjectName('getPathWindow')
        getPathWindow.resize(300, 100)
        getPathWindow.setWindowTitle('choose directory')

        self.centralWidget = QtWidgets.QWidget(mainWindow)
        self.centralWidget.setObjectName('centralWidget')

        self.centralLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QtWidgets.QLabel()
        self.label.setObjectName('label')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(self.screenW // 150)
        self.label.setFont(font)
        self.label.setText('Choose working directory')
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.setObjectName('comboBox')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(self.screenW // 150)
        self.comboBox.setFont(font)
        self.comboBox.addItem('Release')
        self.comboBox.addItems(os.listdir(self.pathToWorkspace))
        self.comboBox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.button = QtWidgets.QPushButton()
        self.button.setObjectName('button')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(self.screenW // 150)
        self.button.setFont(font)
        self.button.setText('Go!')
        self.button.clicked.connect(lambda: self.openMainWin(self.comboBox.currentText()))
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.centralLayout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.centralLayout.addWidget(self.comboBox)
        self.centralLayout.addWidget(self.button, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.centralWidget.setLayout(self.centralLayout)

        getPathWindow.setCentralWidget(self.centralWidget)



if __name__ == "__main__":
    import sys
    import os
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    UiGetPath(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())