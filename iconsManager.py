from PyQt5 import QtCore, QtGui, QtWidgets
import os
from addIcon import Ui_AddIcon
from managerPaths import Paths
import webbrowser
import json
import shutil
from staticMethods import StaticMethods

class MainWindowResizableRepaint1(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.currWidth = (self.size().width() // 130) - 2

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if ((self.size().width() // 130) - 2) != self.currWidth:
            self.resized.emit()
            self.currWidth = ((self.size().width() // 130) - 2)
        return super(MainWindowResizableRepaint1, self).resizeEvent(a0)

class IconWidget(QtWidgets.QWidget):
    def __init__(self, parentTab):
        super(IconWidget, self).__init__(parentTab)

class MainWinCloseUpdate(QtWidgets.QMainWindow):
    def __init__(self, prevWin):
        super().__init__()
        print(prevWin)
        self.prevWin = prevWin

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.prevWin.updateWindow(currIdx=None)

class DropWidget(QtWidgets.QWidget):
    def __init__(self, parent, win, ui):
        super().__init__(parent)
        self.win = win
        self.mainUi = ui
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        print(event.mimeData().formats())
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        newIcons = []
        for url in event.mimeData().urls():
            print(url.path())
            newIcons.append(url.path().lstrip('/'))
        iconsTypeList = []
        for iconsType in os.listdir(Paths.icons):
            iconsTypeList.append(iconsType)
        Ui_AddIcon(MainWinCloseUpdate(self.mainUi), newIcons, iconsTypeList)

    def updateWindow(self, win, ui):
        ui.createState()
        win.resized.disconnect()
        ui.setupUi(win)
        win.update()

class Ui_IconsWindow(object):
    def __init__(self, win):
        self.createState()
        self.dynamicObjList = []
        self.selectedObjList = []
        self.setupUi(win)
        win.show()

    def createState(self):
        self.iconTypes = os.listdir(Paths.icons)
        self.iconsDict = dict()
        for type in self.iconTypes:
            objList = []
            for iconObj in os.listdir(os.path.join(Paths.icons, type)):
                obj = {
                    "name": iconObj.rsplit('.')[0],
                    "path": os.path.join(Paths.icons, type, iconObj),
                    "isChecked": False
                }
                objList.append(obj)

            self.iconsDict[type] = {"selectAllState": False, "isFiltered": False, "objects": objList}

    def setupUi(self, iconsWindow):
        iconsWindow.setObjectName('iconsWindow')
        iconsWindow.setWindowTitle('icons manager')
        # iconsWindow.resize(900, 600)
        self.iconsWindow = iconsWindow

        self.centralWidget = QtWidgets.QWidget(iconsWindow)
        self.centralWidget.setObjectName('centralWidget')

        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName('tabWidget')

        self.buttonsWidget = QtWidgets.QWidget()
        self.buttonsWidget.setObjectName('buttonsWidget')
        self.buttonsWidget.setMaximumHeight(100)

        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setObjectName('buttonsLayout')
        self.buttonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.addButton = QtWidgets.QPushButton(clicked=lambda: self.addIcon())
        self.addButton.setObjectName('deleteButton')
        self.addButton.setText('ADD')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.addButton.setMinimumSize(150, 35)
        self.addButton.setFont(font)

        self.selectallButton = QtWidgets.QPushButton()
        self.selectallButton.setObjectName('selectallButton')
        self.selectallButton.setText('SELECT ALL')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.selectallButton.setMinimumSize(150, 35)
        self.selectallButton.setFont(font)
        self.selectallButton.clicked.connect(lambda: self.selectAll())

        self.deleteButton = QtWidgets.QPushButton(clicked=lambda: self.deleteIcon())
        self.deleteButton.setObjectName('deleteButton')
        self.deleteButton.setText('DELETE')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.deleteButton.setMinimumSize(150, 35)
        self.deleteButton.setFont(font)

        self.openDirButton = QtWidgets.QPushButton(clicked=lambda: \
            webbrowser.open(os.path.join(Paths.icons, self.tabWidget.tabText(self.tabWidget.currentIndex()))))
        self.openDirButton.setObjectName('openDirButton')
        self.openDirButton.setText('OPEN DIRECTORY')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.openDirButton.setFont(font)
        self.openDirButton.setMinimumSize(150, 35)
        self.openDirButton.setEnabled(True)

        for iconsType in os.listdir(Paths.icons):
            self.createTab(iconsType)

        spacer1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                        QtWidgets.QSizePolicy.Policy.Fixed)
        spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                        QtWidgets.QSizePolicy.Policy.Fixed)

        self.buttonsLayout.addItem(spacer1)
        self.buttonsLayout.addWidget(self.addButton)
        self.buttonsLayout.addWidget(self.selectallButton)
        self.buttonsLayout.addWidget(self.deleteButton)
        self.buttonsLayout.addWidget(self.openDirButton)
        self.buttonsLayout.addItem(spacer2)
        self.buttonsWidget.setLayout(self.buttonsLayout)

        self.centralLayout.addWidget(self.tabWidget)
        self.centralLayout.addWidget(self.buttonsWidget)
        self.centralWidget.setLayout(self.centralLayout)

        iconsWindow.setCentralWidget(self.centralWidget)

    def createTab(self, iconsType):
        self.tabField = DropWidget(self.tabWidget, self.iconsWindow, self)
        self.tabField .setObjectName(iconsType + 'Tab')
        self.tabWidget.addTab(self.tabField, '')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabField), iconsType)

        self.tabMainLayout = QtWidgets.QVBoxLayout()
        self.tabMainLayout.setObjectName('tabMainLayout')
        self.tabMainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.scrollArea = QtWidgets.QScrollArea(self.tabField)
        self.scrollArea.setObjectName('scrollArea')
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.tabGrid = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.tabGrid.setContentsMargins(10, 10, 10, 10)
        self.tabGrid.setHorizontalSpacing(1)
        self.tabGrid.setVerticalSpacing(1)
        self.tabGrid.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.tabGrid.setObjectName(iconsType + 'GridLayout')

        self.searchWidget = QtWidgets.QWidget(self.tabField)
        self.searchWidget.setObjectName(iconsType + 'SearchWidget')
        self.searchWidget.setMaximumHeight(100)
        self.searchWidget.setMaximumWidth(350)

        self.searchFormLayout = QtWidgets.QFormLayout()
        self.searchFormLayout.setObjectName(iconsType + 'SearchFormLayout')
        self.searchFormLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.searchLabel = QtWidgets.QLabel(self.searchWidget)
        self.searchLabel.setObjectName(iconsType + 'SearchLabel')
        self.searchLabel.setText('search here')
        self.searchLineEdit = QtWidgets.QLineEdit(self.searchWidget)
        self.searchLineEdit.setObjectName(iconsType + 'SearchLineEdit')
        print(str(self.searchLineEdit) + ' - created')
        self.searchFormLayout.addRow(self.searchLabel, self.searchLineEdit)

        self.searchWidget.setLayout(self.searchFormLayout)

        self.searchCompleter = QtWidgets.QCompleter(self.tabField)
        self.searchCompleter.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.searchLineEdit.setCompleter(self.searchCompleter)

        objectsList = []
        for objects in self.iconsDict[iconsType]['objects']:
            objectsList.append(objects)

        self.paintField(objectsList, self.tabGrid, iconsType, self.searchCompleter)

        self.searchLineEdit.textChanged.connect(lambda bool, comp=self.searchCompleter, lineEdit=self.searchLineEdit,
                                                       tabField=self.tabField:
                                                self.dynamicRepaint(objectsList, lineEdit, tabField, comp))

        self.iconsWindow.resized.connect(lambda comp=self.searchCompleter, lineEdit=self.searchLineEdit,
                                                tabField=self.tabField:
                                         self.dynamicRepaint(objectsList, lineEdit, tabField, comp))



        self.tabMainLayout.addWidget(self.scrollArea)
        self.tabMainLayout.addWidget(self.searchWidget)
        self.tabField.setLayout(self.tabMainLayout)

    def isFiltered(self, text, iconsType):
        if text != '':
            self.iconsDict[iconsType]['isFiltered'] = True
        else:
            self.iconsDict[iconsType]['isFiltered'] = False

    def paintField(self, objects, grid, type, completer):
        x = 0
        y = 0
        completer.setModel(QtCore.QStringListModel(self.fillCompleterList(objects)))
        for each in objects:
            iconWidget = IconWidget(self.tabWidget)
            iconWidget.setObjectName(each['name'] + 'Widget')
            iconWidget.setFixedSize(150, 170)
            pal = QtGui.QPalette()
            pal.setColor(QtGui.QPalette.Background, QtGui.QColor('#D0D0D0'))
            iconWidget.setPalette(pal)
            iconWidget.setAutoFillBackground(True)
            iconLayout = QtWidgets.QVBoxLayout()
            iconLayout.setObjectName(each['name'] + 'Layout')
            iconPic = QtWidgets.QLabel()
            iconPic.resize(128, 128)
            pixmap = QtGui.QPixmap(os.path.join(each['path'])).scaled(128, 128, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            iconPic.setPixmap(pixmap)
            iconName = QtWidgets.QLabel(iconWidget)
            iconName.setObjectName(each['name'] + 'Name')
            iconName.setText(each['name'])
            iconName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            iconLayout.addWidget(iconPic, 9)
            iconLayout.addWidget(iconName, 1)

            checkbox = QtWidgets.QCheckBox(iconWidget)
            checkbox.setGeometry(125, 5, 20, 20)
            checkbox.setChecked(each['isChecked'])
            checkbox.clicked.connect(lambda bool, name=each['name'], currCheckbox=checkbox: self.check(name, type, currCheckbox.isChecked()))


            iconWidget.setLayout(iconLayout)

            checkbox.raise_()
            grid.addWidget(iconWidget, x, y, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

            y += 1
            if y > ((self.iconsWindow.size().width()) // 135) - 2:
                x += 1
                y = 0

    def fillCompleterList(self, objects):
        cleanCompleterList = []
        for each in objects:
            cleanCompleterList.append(each['name'])
        return cleanCompleterList

    def check(self, name, iconType, state):
        for eachObj in self.iconsDict[iconType]['objects']:
            if eachObj['name'] == name:
                eachObj['isChecked'] = state

    def repaintField(self, objects, tabWidget, searchCompleter):
        objectType = tabWidget.objectName().rsplit('Tab')[0]
        grid = self.getTabGrid(tabWidget)
        for i in reversed(range(grid.count())):
            grid.itemAt(i).widget().setParent(None)
        self.paintField(objects, grid, objectType, searchCompleter)

    def getTabGrid(self, tab):
        tabName = tab.objectName().rsplit('Tab')[0]
        grid = tab.findChild(QtWidgets.QGridLayout, (tabName + 'GridLayout'))
        return grid

    def dynamicRepaint(self, objectsList, lineEdit, tabWidget, searchCompleter):
        currentText = lineEdit.text()
        iconsType = tabWidget.objectName().rsplit('Tab')[0]
        self.isFiltered(currentText, iconsType)

        if currentText == '':
            self.dynamicObjList.clear()
            self.repaintField(objectsList, tabWidget, searchCompleter)
            for eachObj in self.iconsDict[iconsType]['objects']:
                if eachObj['isChecked'] == True:
                    self.selectallButton.setText('CLEAR SELECTION')
                    break
                else:
                    for type in self.iconsDict:
                        if self.iconsDict[type]['isFiltered'] == True:
                            self.selectallButton.setText('ADD TO SELECTION')
                            break
                        else:
                            self.selectallButton.setText('SELECT ALL')
        else:
            self.dynamicObjList.clear()
            for eachObject in objectsList:
                if currentText in eachObject['name']:
                    self.dynamicObjList.append(eachObject)
            self.repaintField(self.dynamicObjList, tabWidget, searchCompleter)
            self.selectallButton.setText('ADD TO SELECTION')

    def deleteIcon(self):
        deletionList = []
        deletionNamesList = []
        blocksToDelete = []
        for type in self.iconsDict:
            for obj in self.iconsDict[type]['objects']:
                if obj['isChecked'] == True:
                    deletionList.append(obj['path'])
                    deletionNamesList.append(obj['name'])
                    if type == 'blocks':
                        blocksToDelete.append(obj['name'])

        if len(deletionList) != 0:
            questionBox = QtWidgets.QMessageBox()
            questionBox.setWindowTitle('Delete')
            questionBox.setIcon(QtWidgets.QMessageBox.Question)
            questionBox.setText('Are you sure you want to delete this icons? \n' + str(deletionNamesList))
            questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            button = questionBox.exec()

            if button == QtWidgets.QMessageBox.Yes:

                for each in deletionList:
                    print(each)
                    os.remove(each)

                if len(blocksToDelete) != 0:
                    self.removeBlockFromCubelariaDB(blocksToDelete)
                    cmState = StaticMethods.getCreationModeInventoryState(Paths.creationModeInventory)
                    StaticMethods.deleteObjectFromCreationModeInventory(cmState, blocksToDelete, 'blocks')
                    StaticMethods.updateCreationModeInventoryFile(cmState, Paths.creationModeInventory)

                self.updateWindow(self.tabWidget.currentIndex())

            else:
                pass
        else:
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setText("Info")
            messageBox.setInformativeText('Nothing to delete.')
            messageBox.setWindowTitle("Info")
            messageBox.exec_()

    def selectAll(self):
        tab = self.tabWidget.currentWidget()
        grid = self.getTabGrid(tab)
        iconsType = self.tabWidget.currentWidget().objectName().rsplit('Tab')[0]
        objectsList = []
        for objects in self.iconsDict[iconsType]['objects']:
            objectsList.append(objects)
        lineEdit = tab.findChild(QtWidgets.QLineEdit)
        completer = tab.findChild(QtWidgets.QCompleter)
        self.dynamicRepaint(objectsList, lineEdit, tab, completer)

        if self.iconsDict[iconsType]['selectAllState'] == False:
            if len(self.dynamicObjList) == 0:
                for eachObj in self.iconsDict[iconsType]['objects']:
                    if eachObj['isChecked'] == False:
                        eachObj['isChecked'] = True

                for i in range(grid.count()):
                    grid.itemAt(i).widget().findChild(QtWidgets.QCheckBox).setChecked(True)

                self.iconsDict[iconsType]['selectAllState'] = True
                self.selectallButton.setText('CLEAR SELECTION')

            else:
                for eachObj in self.iconsDict[iconsType]['objects']:
                    for eachItem in self.dynamicObjList:
                        if eachObj['name'] == eachItem['name']:
                            print(eachObj['name'] + ' ' + eachItem['name'])
                            if eachObj['isChecked'] == False:
                                eachObj['isChecked'] = True

                    for i in range(grid.count()):
                        name = grid.itemAt(i).widget().layout().itemAt(1).widget().text()
                        print(name)
                        if name == eachObj['name']:
                            grid.itemAt(i).widget().findChild(QtWidgets.QCheckBox).setChecked(True)

                self.selectedObjList = list(self.dynamicObjList)
                self.iconsDict[iconsType]['selectAllState'] = True
                self.selectallButton.setText('CLEAR SELECTION')


        else:
            if len(self.dynamicObjList) == 0:
                for eachObj in self.iconsDict[iconsType]['objects']:
                    if eachObj['isChecked'] == True:
                        eachObj['isChecked'] = False

                for i in range(grid.count()):
                    grid.itemAt(i).widget().findChild(QtWidgets.QCheckBox).setChecked(False)

                self.iconsDict[iconsType]['selectAllState'] = False
                self.selectallButton.setText('SELECT ALL')

            elif self.dynamicObjList == self.selectedObjList:
                for eachObj in self.iconsDict[iconsType]['objects']:
                    for eachItem in self.dynamicObjList:
                        if eachObj['name'] == eachItem['name']:
                            print(eachObj['name'] + ' ' + eachItem['name'])
                            if eachObj['isChecked'] == True:
                                eachObj['isChecked'] = False

                    for i in range(grid.count()):
                        name = grid.itemAt(i).widget().layout().itemAt(1).widget().text()
                        print(name)
                        if name == eachObj['name']:
                            grid.itemAt(i).widget().findChild(QtWidgets.QCheckBox).setChecked(False)

                self.iconsDict[iconsType]['selectAllState'] = False
                self.selectallButton.setText('SELECT ALL')

            else:
                for eachObj in self.iconsDict[iconsType]['objects']:
                    for eachItem in self.dynamicObjList:
                        if eachObj['name'] == eachItem['name']:
                            print(eachObj['name'] + ' ' + eachItem['name'])
                            if eachObj['isChecked'] == False:
                                eachObj['isChecked'] = True

                    for i in range(grid.count()):
                        name = grid.itemAt(i).widget().layout().itemAt(1).widget().text()
                        print(name)
                        if name == eachObj['name']:
                            grid.itemAt(i).widget().findChild(QtWidgets.QCheckBox).setChecked(True)

                self.selectedObjList = list(self.dynamicObjList)
                self.iconsDict[iconsType]['selectAllState'] = True
                self.selectallButton.setText('CLEAR SELECTION')

    def updateWindow(self, currIdx):
        self.createState()
        self.iconsWindow.resized.disconnect()
        self.setupUi(self.iconsWindow)
        self.iconsWindow.update()
        if currIdx != None:
            self.tabWidget.setCurrentIndex(currIdx)

    def removeBlockFromCubelariaDB(self, selectedNames):
        with open(Paths.blocksDb, 'r', encoding='utf8') as cub_db:
            self.cubelariaDbDict = json.load(cub_db)
        newBlocksList = []
        for eachBlock in self.cubelariaDbDict['blocks']:
            if eachBlock['name'] not in selectedNames:
                newBlocksList.append(eachBlock)
            else:
                pass

        self.cubelariaDbDict['blocks'] = newBlocksList

        with open(Paths.blocksDb, 'w', encoding='utf8') as cub_db:
            json.dump(self.cubelariaDbDict, cub_db, indent=3, ensure_ascii=False, separators=(',', ':'))

    def deleteFromBundlesInventory(self, selectedNames):
        with open(os.path.join(Paths.bundles, 'inventory.json'), 'r', encoding='utf8') as inventoryJson:
            inventoryJsonList = json.load(inventoryJson)
        newInventoryJsonList = []
        for eachObj in inventoryJsonList:
            name = str(eachObj['name'])
            nameLower = name.lower()
            if nameLower.rsplit('::')[0] == 'blocks':
                nameClean = nameLower.rsplit('blocks::')[1]
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

    def addIcon(self):
        fileDialog = QtWidgets.QFileDialog()
        newIcons = fileDialog.getOpenFileNames()[0]
        if len(newIcons) != 0:
            Ui_AddIcon(MainWinCloseUpdate(self), newIcons, self.iconTypes)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    iconsWindow = MainWindowResizableRepaint1()
    Paths.getDir('Release')
    Ui_IconsWindow(iconsWindow)
    iconsWindow.show()
    sys.exit(app.exec_())