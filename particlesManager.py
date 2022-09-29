from PyQt5 import QtCore, QtGui, QtWidgets
import os
import json
import shutil
from managerPaths import Paths
from addParticles import Ui_AddParticles, Ui_EditParticle
from staticMethods import StaticMethods

class MainWinCloseUpdate(QtWidgets.QMainWindow):
    def __init__(self, prevWin):
        super().__init__()
        print(prevWin)
        self.prevWin = prevWin

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.prevWin.updateWindow()

class DragDropListWidget(QtWidgets.QListWidget):
    def __init__(self, parent, win, ui):
        super().__init__(parent)
        self.win = win
        self.mainUi = ui
        self.setAcceptDrops(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.mimeTypesList = ['application/x-qt-windows-mime;value="Shell IDList Array"',
                              'application/x-qt-windows-mime;value="UsingDefaultDragImage"',
                              'application/x-qt-windows-mime;value="DragImageBits"',
                              'application/x-qt-windows-mime;value="DragContext"',
                              'application/x-qt-windows-mime;value="DragSourceHelperFlags"',
                              'application/x-qt-windows-mime;value="InShellDragLoop"',
                              'text/uri-list',
                              'application/x-qt-windows-mime;value="FileName"',
                              'application/x-qt-windows-mime;value="FileContents"',
                              'application/x-qt-windows-mime;value="FileNameW"',
                              'application/x-qt-windows-mime;value="FileGroupDescriptorW"']

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event: QtGui.QDropEvent):
        for url in event.mimeData().urls():
            print(url.path())


    def updateWindow(self, win, ui):
        ui.setupUi(win)
        win.update()

class Ui_ParticlesWindow(object):
    def __init__(self, win):
        self.cubelariaDBOpen()
        self.setupUi(win)
        win.show()

    def updateWindow(self):
        self.setupUi(self.particlesWindow)
        self.particlesWindow.update()

    def setupUi(self, particlesWindow):
        particlesWindow.resize(600, 800)
        particlesWindow.setObjectName('particlesWindow')
        particlesWindow.setWindowTitle('particles manager')
        self.particlesWindow = particlesWindow

        self.centralwidget = QtWidgets.QWidget(particlesWindow)
        self.centralwidget.setObjectName('centralwidget')

        self.centralLayout = QtWidgets.QHBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setContentsMargins(10, 20, 10, 20)
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.listWidget = DragDropListWidget(self.centralwidget, self.particlesWindow, self)
        self.listWidget.setObjectName('listWidget')
        self.listWidget.setMinimumWidth(230)
        self.listWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.listWidgetFill()
        self.listWidget.itemClicked.connect(lambda: self.showIcon(self.listWidget.currentItem().text()))
        self.listWidget.itemDoubleClicked.connect(lambda: self.openForEditing(self.listWidget.currentItem().text()))

        self.rightSideWidget = QtWidgets.QWidget()
        self.rightSideWidget.setObjectName('rightSideWidget')
        self.rightSideWidget.setMaximumWidth(250)

        self.rightSideLayout = QtWidgets.QVBoxLayout()
        self.rightSideLayout.setObjectName('rightSideLayout')
        self.rightSideLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.rightSideLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.particleIcon = QtWidgets.QLabel()
        self.particleIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.particleIcon.setObjectName('particleIcon')
        self.particleIcon.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.particleIcon.setMinimumSize(128, 128)

        self.particleNameLabel = QtWidgets.QLabel()
        self.particleNameLabel.setObjectName('particleNameLabel')
        self.particleNameLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.particleNameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.addNewParticlesButton = QtWidgets.QPushButton()
        self.addNewParticlesButton.setObjectName('addNewParticlesButton')
        self.addNewParticlesButton.setMinimumSize(150, 35)
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.addNewParticlesButton.setFont(font)
        self.addNewParticlesButton.setText('ADD')
        self.addNewParticlesButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        self.addNewParticlesButton.clicked.connect(lambda: self.addParticles())

        self.deleteButton = QtWidgets.QPushButton()
        self.deleteButton.setObjectName('deleteButton')
        self.deleteButton.setMinimumSize(150, 35)
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.deleteButton.setFont(font)
        self.deleteButton.setText('DELETE')
        self.deleteButton.clicked.connect(lambda: self.deleteParticles())

        spacerV1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Fixed,
                                         QtWidgets.QSizePolicy.Policy.Fixed)
        spacerV2 = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Policy.Fixed,
                                        QtWidgets.QSizePolicy.Policy.Expanding)

        self.rightSideLayout.addItem(spacerV1)
        self.rightSideLayout.addWidget(self.particleIcon, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rightSideLayout.addWidget(self.particleNameLabel)
        self.rightSideLayout.addWidget(self.addNewParticlesButton)
        self.rightSideLayout.addWidget(self.deleteButton)
        self.rightSideLayout.addItem(spacerV2)
        self.rightSideWidget.setLayout(self.rightSideLayout)

        spacerH1 = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                         QtWidgets.QSizePolicy.Policy.Fixed)
        spacerH2 = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                         QtWidgets.QSizePolicy.Policy.Fixed)
        spacerH3 = QtWidgets.QSpacerItem(30, 40, QtWidgets.QSizePolicy.Policy.Fixed,
                                         QtWidgets.QSizePolicy.Policy.Fixed)

        self.centralLayout.addItem(spacerH1)
        self.centralLayout.addWidget(self.listWidget)
        self.centralLayout.addItem(spacerH3)
        self.centralLayout.addWidget(self.rightSideWidget)
        self.centralLayout.addItem(spacerH2)
        self.centralwidget.setLayout(self.centralLayout)

        particlesWindow.setCentralWidget(self.centralwidget)

    def openForEditing(self, item):
        listForEditing = []
        listForEditing.append(os.path.join(Paths.particles, item))
        Ui_EditParticle(MainWinCloseUpdate(self), listForEditing)

    def listWidgetFill(self):
        for each in os.listdir(Paths.particles):
            self.listWidget.addItem(each)

    def showIcon(self, name):
        pathToCurrItem = os.path.join(Paths.icons, 'particles', name.rsplit('.')[0] + '.png')
        if os.path.exists(pathToCurrItem):
            pixmap = QtGui.QPixmap(pathToCurrItem).scaled(128, 128, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        else:
            pixmap = QtGui.QPixmap(os.path.join(Paths.icons, 'misc', 'missing.png')).scaled(128, 128, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.particleIcon.setPixmap(pixmap)
        self.particleNameLabel.setText(name.rsplit('.')[0])
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor('#D0D0D0'))
        self.particleIcon.setAutoFillBackground(True)
        self.particleIcon.setPalette(pal)

    def addParticles(self):
        fileDialog = QtWidgets.QFileDialog()
        newCurrParticles = fileDialog.getOpenFileNames(filter='Magic Particles (*.ptc)')[0]
        if len(newCurrParticles) != 0:
            Ui_AddParticles(MainWinCloseUpdate(self), newCurrParticles)

    def deleteParticles(self):
        cmState = StaticMethods.getCreationModeInventoryState(Paths.creationModeInventory)
        selectedItems = []
        selectedNames = []
        for each in self.listWidget.selectedItems():
            selectedItems.append(each.text())
            selectedNames.append((each.text().rsplit('.')[0]))
        questionBox = QtWidgets.QMessageBox()
        questionBox.setWindowTitle('Delete')
        questionBox.setIcon(QtWidgets.QMessageBox.Question)
        questionBox.setText('Are you sure you want to delete ' + str(selectedItems) + ' particles?')
        questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        button = questionBox.exec()

        if button == QtWidgets.QMessageBox.Yes:
            for each in selectedItems:
                deletionPath = os.path.join(Paths.particles, each)
                os.remove(deletionPath)

            newDict = {}

            for type in self.cubelariaDBDict:
                objects = []
                for each in self.cubelariaDBDict[type]:
                    if each['name'] not in selectedNames:
                        objects.append(each)
                newDict[type] = objects

            with open(Paths.objectsDb, 'w', encoding='utf8') as dbFile:
                json.dump(newDict, dbFile, indent=3, ensure_ascii=False, separators=(',', ':'))

            StaticMethods.deleteObjectFromCreationModeInventory(cmState, selectedNames, 'particles')
            StaticMethods.updateCreationModeInventoryFile(cmState, Paths.creationModeInventory)
            self.updateWindow()


    def cubelariaDBOpen(self):
        self.cubelariaDBDict = {}
        self.dBParticlesList = []
        with open(Paths.objectsDb, 'r', encoding='utf8') as cubelariaDB:
            self.cubelariaDBDict = json.load(cubelariaDB)
            for each in self.cubelariaDBDict['particles']:
                print(each['name'])
                self.dBParticlesList.append(each)

    def deleteFromBundlesInventory(self, selectedNames):
        with open(os.path.join(Paths.bundles, 'inventory.json'), 'r', encoding='utf8') as inventoryJson:
            inventoryJsonList = json.load(inventoryJson)
        newInventoryJsonList = []
        for eachObj in inventoryJsonList:
            name = str(eachObj['name'])
            nameLower = name.lower()
            if nameLower.rsplit('::')[0] == 'particles':
                nameClean = nameLower.rsplit('particles::')[1]
                if nameClean not in selectedNames:
                    newInventoryJsonList.append(eachObj)
            else:
                newInventoryJsonList.append(eachObj)

        with open(os.path.join(Paths.bundles, 'inventory.json'), 'w', encoding='utf8') as inventoryJson:
            json.dump(newInventoryJsonList, inventoryJson, indent=2, separators=(',', ':'))

        for eachBundle in os.listdir(os.path.join(Paths.bundles, 'user')):
            if os.path.exists(os.path.join(Paths.bundles, 'user', eachBundle, 'inventory.json')):
                os.remove(os.path.join(Paths.bundles, 'user', eachBundle, 'inventory.json'))
                shutil.copyfile(os.path.join(Paths.bundles, 'inventory.json'),
                                os.path.join(Paths.bundles, 'user', eachBundle, 'inventory.json'))
            else:
                shutil.copyfile(os.path.join(Paths.bundles, 'inventory.json'),
                                os.path.join(Paths.bundles, 'user', eachBundle, 'inventory.json'))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    particlesWindow = QtWidgets.QMainWindow()
    Paths.getDir('Release')
    Ui_ParticlesWindow(particlesWindow)
    particlesWindow.show()
    sys.exit(app.exec_())