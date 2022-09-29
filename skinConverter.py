from PyQt5 import QtWidgets, QtCore, QtGui
import os
import subprocess
from managerPaths import Paths
from staticMethods import StaticMethods

class Ui_SkinConverter(object):
    def __init__(self, win, app):
        self.app = app
        self.win = win
        self.setupUi(win)
        win.show()

        self.texturePackerSettings = 'TexturePacker --format phaser-json-hash --png-opt-level 1 --force-squared ' \
                                     '--max-size 4096 --scale 1 --scale-mode Smooth --algorithm MaxRects ' \
                                     '--maxrects-heuristics Best --pack-mode Best --trim-mode Trim --pack-normalmaps ' \
                                     '--normalmap-filter "/normalmaps/" --normalmap-suffix "_n"'

    def setupUi(self, skinConverter):
        skinConverter.resize(350, 200)
        skinConverter.setObjectName('skinConverterWindow')
        skinConverter.setWindowTitle('skin_converter')

        self.centralwidget = QtWidgets.QWidget(skinConverter)
        self.centralwidget.setObjectName('centralwidget')

        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.centralLayout.setContentsMargins(20, 20, 20, 20)

        self.selectionWidget = QtWidgets.QWidget(self.centralwidget)
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
        self.chooseFolderButton.setText('Choose\nDefaultMC')
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

        self.mainButtonsWidget = QtWidgets.QWidget(self.centralwidget)
        self.mainButtonsWidget.setObjectName('mainButtonsWidget')

        self.mainButtonsLayout = QtWidgets.QHBoxLayout()
        self.mainButtonsLayout.setObjectName('mainButtonsLayout')
        self.mainButtonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.updateAtlasButton = QtWidgets.QPushButton(self.mainButtonsWidget)
        self.updateAtlasButton.setObjectName('updateAtlasButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.updateAtlasButton.setFont(font)
        self.updateAtlasButton.setText('Update\natlas')
        self.updateAtlasButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.updateAtlasButton.setMinimumSize(150, 50)
        self.updateAtlasButton.setEnabled(False)
        self.updateAtlasButton.clicked.connect(lambda: self.updateAtlas())

        self.addTexturesButton = QtWidgets.QPushButton(self.mainButtonsWidget)
        self.addTexturesButton.setObjectName('addTexturesButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.addTexturesButton.setFont(font)
        self.addTexturesButton.setText('Add textures\nfrom somewhere')
        self.addTexturesButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.addTexturesButton.setMinimumSize(150, 50)
        self.addTexturesButton.setEnabled(False)

        spacerH1 = QtWidgets.QSpacerItem(50, 40, QtWidgets.QSizePolicy.Policy.Fixed,
                                         QtWidgets.QSizePolicy.Policy.Fixed)

        self.mainButtonsLayout.addWidget(self.updateAtlasButton)
        self.mainButtonsLayout.addItem(spacerH1)
        self.mainButtonsLayout.addWidget(self.addTexturesButton)

        self.mainButtonsWidget.setLayout(self.mainButtonsLayout)

        self.centralLayout.addWidget(self.selectionWidget)
        self.centralLayout.addWidget(self.mainButtonsWidget)

        self.centralwidget.setLayout(self.centralLayout)

        skinConverter.setCentralWidget(self.centralwidget)

    def clearFolder(self):
        self.folderLineEdit.clear()
        self.currFolder = ''
        self.updateAtlasButton.setEnabled(False)
        self.folderLineEdit.setEnabled(True)
        self.chooseFolderButton.setEnabled(True)

    def chooseFolder(self):
        fileDialog = QtWidgets.QFileDialog()
        self.currFolder = fileDialog.getExistingDirectory()
        self.folderLineEdit.setText(self.currFolder)
        self.folderLineEdit.setEnabled(False)
        self.updateAtlasButton.setEnabled(True)
        self.chooseFolderButton.setEnabled(False)

    def updateAtlas(self):
        pathToConverter = os.path.join(Paths.tools, 'minecraft_skin_converter.exe')
        pathToSkin = os.path.join(Paths.world, 'skin.dat')
        pathToMCAssets = os.path.join(self.currFolder, 'assets')
        pathToAtlasPng = os.path.join(Paths.world, 'world.png')
        pathToWorldJson = os.path.join(self.currFolder, 'world.json')
        pathToTextures = os.path.join(self.currFolder, 'assets', 'minecraft', 'textures', 'block')

        try:
            os.remove(pathToSkin)
        except FileNotFoundError:
            pass

        try:
            os.remove(pathToAtlasPng)
        except FileNotFoundError:
            pass

        try:
            os.remove(os.path.join(Paths.world, 'world_n.png'))
        except FileNotFoundError:
            pass


        subprocess.call('start /wait ' + self.texturePackerSettings + ' --sheet "' + pathToAtlasPng +
                        '" --data "' + pathToWorldJson + '" "' + pathToTextures + '"', shell=True, cwd=os.getcwd())
        subprocess.call('start /wait ' + pathToConverter + ' ' + pathToSkin + ' ' + pathToMCAssets + ' ' + pathToWorldJson,
                        shell=True)

        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setText("Info")
        messageBox.setInformativeText('Files world.png, world_n.png, skin.dat have successfully converted in "world" directory.')
        messageBox.setWindowTitle("Info")
        messageBox.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    Paths.getDir('Release')
    Ui_SkinConverter(mainWindow, app)
    mainWindow.show()
    sys.exit(app.exec_())