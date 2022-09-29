from PyQt5 import QtGui, QtWidgets
from fbxConvert import Ui_FbxConverter
from skymapConverter import Ui_SkymapConverter
from skinConverter import Ui_SkinConverter
from texturesConverter import Ui_TexturesConverter
from managerPaths import Paths
from staticMethods import StaticMethods

class Ui_Converters(object):
    def __init__(self, win, app):
        self.app = app
        self.converters = win
        self.setupUi(self.converters)
        self.converters.show()

    def openWindow(self, ui):
        self.win = QtWidgets.QMainWindow()
        if ui == Ui_FbxConverter:
            Ui_FbxConverter(self.win, self.app)
        elif ui == Ui_SkymapConverter:
            Ui_SkymapConverter(self.win, self.app)
        elif ui == Ui_SkinConverter:
            Ui_SkinConverter(self.win, self.app)
        elif ui == Ui_TexturesConverter:
            Ui_TexturesConverter(self.win, self.app)

    def setupUi(self, converters):
        converters.resize(300, 200)
        converters.setObjectName('convertersWindow')
        converters.setWindowTitle('converters')

        self.centralwidget = QtWidgets.QWidget(converters)
        self.centralwidget.setObjectName('centralwidget')

        self.centralLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setContentsMargins(20, 20, 20, 20)

        self.fbxToGlbButton = QtWidgets.QPushButton()
        self.fbxToGlbButton.setObjectName('fbxToGlbButton')
        self.fbxToGlbButton.setText('FBX to GLB\nConverter')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.fbxToGlbButton.setFont(font)
        self.fbxToGlbButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                          QtWidgets.QSizePolicy.Policy.Expanding)
        self.fbxToGlbButton.clicked.connect(lambda: self.openWindow(Ui_FbxConverter))
        self.centralLayout.addWidget(self.fbxToGlbButton, 0, 0)

        self.skymapButton = QtWidgets.QPushButton()
        self.skymapButton.setObjectName('skymapButton')
        self.skymapButton.setText('Skymap\nConverter')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.skymapButton.setFont(font)
        self.skymapButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                        QtWidgets.QSizePolicy.Policy.Expanding)
        self.skymapButton.clicked.connect(lambda: self.openWindow(Ui_SkymapConverter))
        self.centralLayout.addWidget(self.skymapButton, 0, 1)

        self.skinButton = QtWidgets.QPushButton()
        self.skinButton.setObjectName('skinButton')
        self.skinButton.setText('Skin\nConverter')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.skinButton.setFont(font)
        self.skinButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                      QtWidgets.QSizePolicy.Policy.Expanding)
        self.skinButton.clicked.connect(lambda: self.openWindow(Ui_SkinConverter))
        self.centralLayout.addWidget(self.skinButton, 1, 0)

        self.texturesButton = QtWidgets.QPushButton()
        self.texturesButton.setObjectName('texturesButton')
        self.texturesButton.setText('Textures\nConverter')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.texturesButton.setFont(font)
        self.texturesButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                          QtWidgets.QSizePolicy.Policy.Expanding)
        self.texturesButton.clicked.connect(lambda: self.openWindow(Ui_TexturesConverter))
        self.centralLayout.addWidget(self.texturesButton, 1, 1)

        self.centralwidget.setLayout(self.centralLayout)


        converters.setCentralWidget(self.centralwidget)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    Paths.getDir('Release')
    Ui_Converters(win)
    win.show()
    sys.exit(app.exec_())