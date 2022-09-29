from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os
import shutil
from PIL import Image
from managerPaths import Paths
from staticMethods import StaticMethods

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent, newIcons):
        super(TabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)
        self.newIcons = newIcons

    def closeTab(self, currentIndex):
        currentQWidget = self.widget(currentIndex)
        currentQWidget.deleteLater()
        self.removeTab(currentIndex)
        self.newIcons.pop(currentIndex)
        if currentIndex == 0:
            self.parent().parent().close()

class Ui_AddIcon(object):
    def __init__(self, win, newIcons, typeList):
        with open(Paths.objectsDb, 'r', encoding='utf8') as self.objDB:
            self.objDBdict = json.load(self.objDB)

        with open(Paths.blocksDb, 'r', encoding='utf8') as self.blocksDB:
            self.blocksDBdict = json.load(self.blocksDB)

        self.setupUi(win, newIcons, typeList)
        win.show()

    def setupUi(self, addIcon, newIcons, typeList):
        addIcon.setObjectName('addIcon')
        addIcon.resize(670, 750)
        addIcon.setWindowTitle('add icon')
        self.addIcon = addIcon

        self.centralWidget = QtWidgets.QWidget(addIcon)
        self.centralWidget.setObjectName('centralWidget')

        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.saveButtonWidget = QtWidgets.QWidget()
        self.saveButtonWidget.setObjectName('saveButtonWidget')
        self.saveButtonWidget.setMaximumHeight(100)

        self.saveButtonLayout = QtWidgets.QHBoxLayout()
        self.saveButtonLayout.setObjectName('saveButtonLayout')
        self.saveButtonLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        spacer1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                        QtWidgets.QSizePolicy.Policy.Fixed)

        self.saveButton = QtWidgets.QPushButton(self.centralWidget)
        self.saveButton.setObjectName('saveButton')
        self.saveButton.setFixedSize(QtCore.QSize(170, 35))
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.saveButton.setFont(font)
        self.saveButton.setText('SAVE')
        self.saveButton.setStyleSheet('background-color: #ECFFC9;')
        self.saveButton.clicked.connect(lambda: self.saveNewIcons(newIcons))

        self.saveButtonLayout.addItem(spacer1)
        self.saveButtonLayout.addWidget(self.saveButton)
        self.saveButtonWidget.setLayout(self.saveButtonLayout)

        self.tabWidget = TabWidget(self.centralWidget, newIcons)
        self.tabWidget.setObjectName('tabWidget')

        quantityOfTabs = 0
        for each in newIcons:
            quantityOfTabs += 1
            tabName = os.path.basename(each).rsplit('.')[0]
            newIconPath = each
            print(newIconPath)
            self.createTab(tabName, quantityOfTabs, typeList, newIconPath)

        self.centralLayout.addWidget(self.tabWidget)
        self.centralLayout.addWidget(self.saveButtonWidget)
        self.centralWidget.setLayout(self.centralLayout)

        addIcon.setCentralWidget(self.centralWidget)

    def createTab(self, tabName, quantityOfTabs, typeList, newIconPath):
        tabField = QtWidgets.QWidget()
        tabField.setObjectName(tabName + 'Tab')
        self.tabWidget.addTab(tabField, '')
        self.tabWidget.setTabText(self.tabWidget.indexOf(tabField), str(quantityOfTabs) + ' icon')

        tabMainLayout = QtWidgets.QHBoxLayout()
        tabMainLayout.setObjectName('tabMainLayout')
        tabMainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        formLayoutWidget = QtWidgets.QWidget()
        formLayoutWidget.setObjectName(tabName + "formLayoutWidget")
        formLayoutWidget.setFixedWidth(350)

        formLayout = QtWidgets.QFormLayout()
        formLayout.setContentsMargins(5, 5, 5, 5)
        formLayout.setHorizontalSpacing(10)
        formLayout.setObjectName(tabName + "formLayout")

        iconNameLabel = QtWidgets.QLabel(formLayoutWidget)
        iconNameLabel.setObjectName("iconName")
        iconNameLabel.setText('icon name')
        self.iconNameLineEdit = QtWidgets.QLineEdit(formLayoutWidget)
        self.iconNameLineEdit.setObjectName("iconNameLineEdit")
        self.iconNameLineEdit.setText(tabName)
        currNameLine = self.iconNameLineEdit
        formLayout.addRow(iconNameLabel, self.iconNameLineEdit)

        iconTypeLabel = QtWidgets.QLabel(formLayoutWidget)
        iconTypeLabel.setObjectName("iconType")
        iconTypeLabel.setText('icon type')
        self.iconTypeComboBox = QtWidgets.QComboBox(formLayoutWidget)
        self.iconTypeComboBox.setObjectName("iconTypeComboBox")
        self.iconTypeComboBox.addItems(typeList)
        formLayout.addRow(iconTypeLabel, self.iconTypeComboBox)
        currComboBox = self.iconTypeComboBox

        completerLabel = QtWidgets.QLabel(formLayoutWidget)
        completerLabel.setObjectName('completerLabel')
        completerLabel.setText('search here')
        completerLineEdit = QtWidgets.QLineEdit(formLayoutWidget)
        completerLineEdit.setObjectName('completerLineEdit')
        formLayout.addRow(completerLabel, completerLineEdit)

        objectsListLabel = QtWidgets.QLabel(formLayoutWidget)
        objectsListLabel.setObjectName('objectsListLabel')
        objectsListLabel.setText('objects list')
        self.objectsList = QtWidgets.QListWidget(formLayoutWidget)
        self.objectsList.setObjectName('objectsList')
        currObjectList = self.objectsList

        formLayout.addRow(objectsListLabel, self.objectsList)

        completer = QtWidgets.QCompleter()
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completerLineEdit.setCompleter(completer)

        formLayoutWidget.setLayout(formLayout)

        ##########################################################################################

        imageWidget = QtWidgets.QWidget()
        imageWidget.setObjectName(tabName + 'imageWidget')
        imageWidget.setFixedWidth(320)

        imageLayout = QtWidgets.QVBoxLayout(imageWidget)
        imageLayout.setObjectName(tabName + 'imageLayout')
        imageLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        imageLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        labelLogoPic = QtWidgets.QLabel()
        labelLogoPic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        pixmap = QtGui.QPixmap(newIconPath)
        labelLogoPic.setPixmap(pixmap.scaled(128, 128, QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        originalSizeLabel = QtWidgets.QLabel()
        originalSizeLabel.setObjectName(tabName + 'originalSizeLabel')
        originalSizeLabel.setText('original size')
        originalSizeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        originalSizeEqual = QtWidgets.QLabel()
        originalSizeEqual.setObjectName(tabName + 'originalSizeEqual')
        originalSizeEqual.setText(str(Image.open(newIconPath).size))
        originalSizeEqual.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        resizeCheckbox = QtWidgets.QCheckBox()

        resizeCheckbox.setObjectName(tabName + 'resizeCheckbox')
        resizeCheckbox.setText('need resize')

        sizePixelsComboBox = QtWidgets.QComboBox()
        sizePixelsComboBox.setObjectName(tabName + "sizePixelsComboBox")
        sizePixelsComboBox.addItems(['128, 128', '256, 256', '512, 512'])
        sizePixelsComboBox.hide()

        spacerV = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Policy.Fixed,
                                        QtWidgets.QSizePolicy.Policy.Expanding)

        imageLayout.addWidget(labelLogoPic)
        imageLayout.addWidget(originalSizeLabel)
        imageLayout.addWidget(originalSizeEqual)
        imageLayout.addWidget(resizeCheckbox)
        imageLayout.addWidget(sizePixelsComboBox)
        imageLayout.addItem(spacerV)

        imageWidget.setLayout(imageLayout)

        spacerH1 = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                        QtWidgets.QSizePolicy.Policy.Fixed)
        spacerH2 = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                         QtWidgets.QSizePolicy.Policy.Fixed)

        tabMainLayout.addItem(spacerH1)
        tabMainLayout.addWidget(formLayoutWidget)
        tabMainLayout.addWidget(imageWidget)
        tabMainLayout.addItem(spacerH2)
        tabField.setLayout(tabMainLayout)

        for type in self.objDBdict:
            for object in self.objDBdict[type]:
                if tabName == object['name']:
                    currComboBox.setCurrentText(type)
                    self.autoResize(currComboBox, resizeCheckbox, sizePixelsComboBox, newIconPath)
                    self.fillObjectsList(box=currComboBox, list=currObjectList, comp=completer)
                    objListItems = currObjectList.findItems(tabName, QtCore.Qt.MatchFlag.MatchStartsWith)
                    try:
                        objListItem = objListItems[0]
                        currObjectList.setCurrentItem(objListItem)
                    except IndexError:
                        pass
                    print('found in ' + type)
                    break

        for type in self.blocksDBdict:
            for object in self.blocksDBdict[type]:
                if tabName == object['name']:
                    currComboBox.setCurrentText(type)
                    self.autoResize(currComboBox, resizeCheckbox, sizePixelsComboBox, newIconPath)
                    self.fillObjectsList(box=currComboBox, list=currObjectList, comp=completer)
                    objListItems = currObjectList.findItems(tabName, QtCore.Qt.MatchFlag.MatchStartsWith)
                    objListItem = objListItems[0]
                    currObjectList.setCurrentItem(objListItem)
                    print('found in ' + type)
                    break

        completerLineEdit.completer().activated.connect(lambda: currObjectList.setCurrentItem(currObjectList.findItems(completerLineEdit.text(), QtCore.Qt.MatchFlag.MatchExactly)[0]))

        self.iconTypeComboBox.currentIndexChanged.connect(lambda idx, box=currComboBox,
                                                                 list=currObjectList,
                                                                 comp=completer: self.fillObjectsList(box, list, comp))

        self.objectsList.itemClicked.connect(lambda list=currObjectList, line=currNameLine,
                                                    box=currComboBox: self.changeName(list, line, box))



        resizeCheckbox.stateChanged.connect(lambda bool, button=resizeCheckbox,
                                                 combobox=sizePixelsComboBox: self.displayResizeBox(button, combobox))

        self.iconTypeComboBox.currentTextChanged.connect(lambda idx, box=currComboBox,
                                                                 button=resizeCheckbox,
                                                                 resizeComboBox=sizePixelsComboBox: self.autoResize(box, button, resizeComboBox, newIconPath))

    def autoResize(self, box, button, resizeComboBox, newIconPath):
        with Image.open(newIconPath) as currentImage:
            originalSize = currentImage.size

        if box.currentText() == 'blocks':
            if originalSize != (128, 128):
                button.setChecked(True)
                resizeComboBox.show()
                resizeComboBox.setCurrentText('128, 128')
            else:
                button.setChecked(False)
        elif box.currentText() == 'inventory':
            if originalSize != (128, 128):
                button.setChecked(True)
                resizeComboBox.show()
                resizeComboBox.setCurrentText('128, 128')
            else:
                button.setChecked(False)
        elif box.currentText() == 'objects':
            if originalSize != (128, 128):
                button.setChecked(True)
                resizeComboBox.show()
                resizeComboBox.setCurrentText('128, 128')
            else:
                button.setChecked(False)
        elif box.currentText() == 'outfitter':
            if originalSize != (128, 128):
                button.setChecked(True)
                resizeComboBox.show()
                resizeComboBox.setCurrentText('128, 128')
            else:
                button.setChecked(False)
        elif box.currentText() == 'particles':
            if originalSize != (128, 128):
                button.setChecked(True)
                resizeComboBox.show()
                resizeComboBox.setCurrentText('128, 128')
            else:
                button.setChecked(False)
        else:
            button.setChecked(False)

    def displayResizeBox(self, button, combobox):
        if button.isChecked():
            combobox.show()
        else:
            combobox.hide()

    def changeName(self, list, line, box):
        print(list.text())
        if box.currentText() == 'blocks':
            newName = list.text()
        elif list.text() == 'none':
            newName = '<set name>'
        else:
            newName = list.text().rsplit('.')[0]
        line.setText(newName)

    def fillObjectsList(self, box, list, comp):
        list.clear()

        pathToObjects = ''
        if box.currentText() == 'creatures':
            pathToObjects = os.path.join(Paths.assets, 'actors', 'creatures')
        elif box.currentText() == 'objects':
            pathToObjects = os.path.join(Paths.assets, 'actors', 'objects')
        elif box.currentText() == 'particles':
            pathToObjects = os.path.join(Paths.assets, 'particles')
        elif box.currentText() == 'blocks':
            for each in self.blocksDBdict['blocks']:
                blockId = each['params']
                list.addItem(str(blockId['blockId']))

        if pathToObjects != '':
            list.addItem('none')
            for each in os.listdir(pathToObjects):
                print(each)
                list.addItem(str(each))
                list.repaint()

        comp.setModel(QtCore.QStringListModel(self.completerFill(list=list)))

    def completerFill(self, list):
        objListFilled = []
        for each in range(list.count()):
            objListFilled.append(list.item(each).text())
        return objListFilled

    def addBlockToCubelariaDB(self, name):
        newBlocksList = []
        for eachBlock in self.blocksDBdict['blocks']:
            if eachBlock['name'] == name:
                return
            else:
                newBlocksList.append(eachBlock)

        currBlockObj = {}
        params = {}
        params['blockId'] = name
        currBlockObj['name'] = name
        currBlockObj['description'] = 'block: ' + name
        currBlockObj['type'] = 'block'
        currBlockObj['params'] = params

        newBlocksList.append(currBlockObj)

        self.blocksDBdict['blocks'] = newBlocksList

        with open(Paths.blocksDb, 'w', encoding='utf8') as cub_db:
            json.dump(self.blocksDBdict, cub_db, indent=3, ensure_ascii=False, separators=(',', ':'))

    def addObjInBundleInventory(self, name):
        with open(os.path.join(Paths.bundles, 'inventory.json'), 'r') as inventoryJson:
            inventoryJsonList = json.load(inventoryJson)

        for eachObj in inventoryJsonList:
            if eachObj['name'] == 'blocks::' + name:
                return

        inventoryJsonList.append(self.createNewObjForInventory(name))

        with open(os.path.join(Paths.bundles, 'inventory.json'), 'w', encoding='utf8') as inventoryJson:
            json.dump(inventoryJsonList, inventoryJson, indent=2, separators=(',', ':'))

        for eachBundle in os.listdir(os.path.join(Paths.bundles, 'user')):
            if os.path.exists(os.path.join(Paths.bundles, 'user', eachBundle, 'inventory.json')):
                os.remove(os.path.join(Paths.bundles, 'user', eachBundle, 'inventory.json'))
                shutil.copyfile(os.path.join(Paths.bundles, 'inventory.json'),
                                os.path.join(Paths.bundles, 'user', eachBundle, 'inventory.json'))
            else:
                shutil.copyfile(os.path.join(Paths.bundles, 'inventory.json'),
                                os.path.join(Paths.bundles, 'user', eachBundle, 'inventory.json'))

    def saveNewIcons(self, newIcons):
        jsonList = []
        cmState = StaticMethods.getCreationModeInventoryState(Paths.creationModeInventory)
        for each in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(each)
            if tab.isEnabled() == True:
                currIconPath = newIcons[each]
                iconSettingLayout = tab.findChild(QtWidgets.QFormLayout,
                                                  os.path.basename(newIcons[each]).rsplit('.')[0] + 'formLayout')
                objType = iconSettingLayout.itemAt(3).widget().currentText()
                currIconName = iconSettingLayout.itemAt(1).widget().text()

                if objType == 'blocks':
                    objList = iconSettingLayout.itemAt(7).widget()
                    try:
                        if objList.currentItem().text() != currIconName:
                            self.addBlockToCubelariaDB(currIconName)
                        else:
                            pass
                    except AttributeError:
                        self.addBlockToCubelariaDB(currIconName)
                    StaticMethods.addObjectInCreationModeInventory(cmState, currIconName, 'blocks')

                if objType == 'creatures' or objType == 'objects' or objType == 'particles':
                    if iconSettingLayout.itemAt(7).widget().currentItem() != None:
                        obj = iconSettingLayout.itemAt(7).widget().currentItem().text()
                        for objInDB in self.objDBdict[objType]:
                            jsonList.append(objInDB['name'])
                        if obj.rsplit('.')[0] not in jsonList:
                            messageBox = QtWidgets.QMessageBox()
                            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                            messageBox.setText("Error")
                            messageBox.setInformativeText('Object ' + currIconName +
                                                          ' is now found in cubelaria_db.json. Please,check and add it later.')
                            messageBox.setWindowTitle("Error")
                            messageBox.exec_()

                if os.path.exists(os.path.join(Paths.icons, objType, currIconName + '.png')):
                    questionBox = QtWidgets.QMessageBox()
                    questionBox.setWindowTitle('Icon exists')
                    questionBox.setIcon(QtWidgets.QMessageBox.Question)
                    questionBox.setText('Icon ' + currIconName + ' already exists. Do you wanna replace?')
                    questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    button = questionBox.exec()

                    if button == QtWidgets.QMessageBox.Yes:
                        currImageLayout = tab.findChild(QtWidgets.QVBoxLayout,
                                                        os.path.basename(newIcons[each]).rsplit('.')[0] + 'imageLayout')
                        currResizeButton = currImageLayout.itemAt(3).widget()
                        if currResizeButton.isChecked():
                            resizedImagePath = self.resizeIcon(tab, currIconPath)
                            shutil.copyfile(resizedImagePath,
                                            os.path.join(Paths.icons, objType,
                                                         currIconName +
                                                         os.path.splitext(os.path.basename(resizedImagePath))[1]))
                            os.remove(resizedImagePath)
                            tab.setEnabled(False)
                        else:
                            shutil.copyfile(currIconPath,
                                            os.path.join(Paths.icons,
                                                         objType, currIconName + '.png'))
                            tab.setEnabled(False)

                    else:
                        self.tabWidget.setCurrentIndex(each)
                        return

                else:
                    currImageLayout = tab.findChild(QtWidgets.QVBoxLayout,
                                                    os.path.basename(newIcons[each]).rsplit('.')[0] + 'imageLayout')
                    currResizeButton = currImageLayout.itemAt(3).widget()
                    if currResizeButton.isChecked():
                        resizedImagePath = self.resizeIcon(tab, currIconPath)
                        if resizedImagePath != '':
                            shutil.copyfile(resizedImagePath,
                                            os.path.join(Paths.icons, objType,
                                                         currIconName +
                                                         os.path.splitext(os.path.basename(resizedImagePath))[1]))
                            os.remove(resizedImagePath)
                            tab.setEnabled(False)
                    else:
                        shutil.copyfile(currIconPath,
                                        os.path.join(Paths.icons,
                                                     objType, currIconName + '.png'))
                        tab.setEnabled(False)

            else:
                pass

        StaticMethods.updateCreationModeInventoryFile(cmState, Paths.creationModeInventory)
        self.addIcon.close()

    def resizeIcon(self, tab, currentIconPath):
        currSizeComboBox = tab.findChild(QtWidgets.QComboBox,
                                         os.path.basename(currentIconPath).rsplit('.')[0] + 'sizePixelsComboBox')
        currNewPicSize = currSizeComboBox.currentText()
        x = int(currNewPicSize.split(', ')[0])
        y = int(currNewPicSize.split(', ')[1])
        currNewPicSizeTuple = x, y
        with Image.open(currentIconPath) as currentImage:
            originalSize = currentImage.size
            if currNewPicSizeTuple > originalSize:
                messageBox = QtWidgets.QMessageBox()
                messageBox.setIcon(QtWidgets.QMessageBox.Warning)
                messageBox.setText("Error")
                messageBox.setInformativeText('Icon ' + os.path.basename(currentIconPath) +
                                              ' cant resize to the bigger size. If you need to increase this icon, please repaint it.')
                messageBox.setWindowTitle("Error")
                messageBox.exec_()
                resizedImagePath = ''
            else:
                resizedImage = currentImage.resize(currNewPicSizeTuple, Image.LANCZOS)
                resizedImage.save(os.path.splitext(currentIconPath)[0] + 'RESIZED.png')
                resizedImagePath = os.path.splitext(currentIconPath)[0] + 'RESIZED.png'

        return resizedImagePath

    def createNewObjForInventory(self, name):
        obj = {}
        obj['name'] = 'blocks::' + name
        obj['quantity'] = 100

        return obj

