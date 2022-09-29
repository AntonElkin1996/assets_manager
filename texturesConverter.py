import PIL
from PyQt5 import QtWidgets, QtCore, QtGui
import os
from PIL import Image
from managerPaths import Paths
from staticMethods import StaticMethods

class Ui_TexturesConverter(object):
    def __init__(self, win, app):
        self.app = app
        self.win = win
        self.setupUi(win)
        win.show()

    def setupUi(self, texturesConverter):
        texturesConverter.resize(350, 200)
        texturesConverter.setObjectName('texturesConverterWindow')
        texturesConverter.setWindowTitle('textures_converter')

        self.centralWidget = QtWidgets.QWidget(texturesConverter)
        self.centralWidget.setObjectName('centralWidget')

        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.centralLayout.setContentsMargins(20, 20, 20, 20)

        self.selectionWidget = QtWidgets.QWidget(self.centralWidget)
        self.selectionWidget.setObjectName('selectionWidget')

        self.selectionLayout = QtWidgets.QHBoxLayout()
        self.selectionLayout.setObjectName('selectionLayout')
        self.selectionLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.buttonWidget = QtWidgets.QWidget(self.selectionWidget)
        self.buttonWidget.setObjectName('buttonWidget')

        self.buttonsLayout = QtWidgets.QVBoxLayout()
        self.buttonsLayout.setObjectName('buttonsLayout')
        self.buttonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.folderLineEdit = QtWidgets.QLineEdit(self.selectionWidget)
        self.folderLineEdit.setObjectName('folderLineEdit')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.folderLineEdit.setFont(font)
        self.folderLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.chooseFolderButton = QtWidgets.QPushButton(self.buttonWidget)
        self.chooseFolderButton.setObjectName('chooseFolderButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.chooseFolderButton.setFont(font)
        self.chooseFolderButton.setText('Choose\nFolder')
        self.chooseFolderButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.chooseFolderButton.setMinimumHeight(50)
        self.chooseFolderButton.clicked.connect(lambda: self.chooseFolder())

        self.clearFolderButton = QtWidgets.QPushButton(self.buttonWidget)
        self.clearFolderButton.setObjectName('clearFolderButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.clearFolderButton.setFont(font)
        self.clearFolderButton.setText('Clear')
        self.clearFolderButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.clearFolderButton.setMinimumHeight(35)
        self.clearFolderButton.clicked.connect(lambda: self.clearFolder())

        self.buttonsLayout.addWidget(self.chooseFolderButton, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.buttonsLayout.addWidget(self.clearFolderButton, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.buttonWidget.setLayout(self.buttonsLayout)

        self.selectionLayout.addWidget(self.folderLineEdit, 6, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.selectionLayout.addWidget(self.buttonWidget, 4)

        self.selectionWidget.setLayout(self.selectionLayout)

        self.convertTexturesButton = QtWidgets.QPushButton(self.centralWidget)
        self.convertTexturesButton.setObjectName('convertTexturesButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.convertTexturesButton.setFont(font)
        self.convertTexturesButton.setText('Convert\ntextures')
        self.convertTexturesButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.convertTexturesButton.setMinimumSize(150, 50)
        self.convertTexturesButton.setEnabled(False)
        self.convertTexturesButton.clicked.connect(lambda: self.convertTextures())

        self.centralLayout.addWidget(self.selectionWidget)
        self.centralLayout.addWidget(self.convertTexturesButton, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.centralWidget.setLayout(self.centralLayout)

        texturesConverter.setCentralWidget(self.centralWidget)

    def clearFolder(self):
        self.folderLineEdit.clear()
        self.currFolder = ''
        self.convertTexturesButton.setEnabled(False)
        self.folderLineEdit.setEnabled(True)
        self.chooseFolderButton.setEnabled(True)

    def chooseFolder(self):
        fileDialog = QtWidgets.QFileDialog()
        self.currFolder = fileDialog.getExistingDirectory()
        self.folderLineEdit.setText(self.currFolder)
        self.folderLineEdit.setEnabled(False)
        self.convertTexturesButton.setEnabled(True)
        self.chooseFolderButton.setEnabled(False)


    def convertTextures(self):
        for root, dirs, files in os.walk(self.currFolder):
            for file in files:
                try:
                    print(os.path.normpath(os.path.join(root, file)))
                    texturePath = os.path.normpath(os.path.join(root, file))
                    textureName = os.path.splitext(file)[0]
                    currImg = Image.open(texturePath)
                    newImg = currImg.convert(mode='RGBA')
                    newImg.save(os.path.join(root, textureName + '.png'))
                    if currImg.format != 'PNG':
                        os.remove(texturePath)
                except PIL.UnidentifiedImageError:
                    print("NOT IMG:::" + os.path.normpath(os.path.join(root, file)))

        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setText("Info")
        messageBox.setInformativeText('Done!')
        messageBox.setWindowTitle("Info")
        messageBox.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    Paths.getDir('Release')
    Ui_TexturesConverter(mainWindow, app)
    mainWindow.show()
    sys.exit(app.exec_())