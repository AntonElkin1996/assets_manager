from PyQt5 import QtCore, QtGui, QtWidgets
import os
import json
import shutil
from managerPaths import Paths
from staticMethods import StaticMethods

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super(TabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)

    def closeTab(self, currentIndex):
        currentQWidget = self.widget(currentIndex)
        currentQWidget.deleteLater()
        self.removeTab(currentIndex)
        if currentIndex == 0:
            self.parent().parent().close()

class Ui_AddParticles(object):
    def __init__(self, win, newCurrParticles):
        self.newIconsPaths = []
        self.cubelariaDBOpen()
        self.setupUi(win, newCurrParticles)
        win.show()

    def setupUi(self, addParticles, newCurrParticles):
        addParticles.setObjectName('addParticles')
        addParticles.resize(430, 600)
        addParticles.setWindowTitle('add particles')
        self.addParticles = addParticles

        self.centralWidget = QtWidgets.QWidget(addParticles)
        self.centralWidget.setObjectName('centralWidget')

        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.tabWidget = TabWidget(self.centralWidget)
        self.tabWidget.setObjectName('tabWidget')

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
        self.saveButton.clicked.connect(lambda: self.saveNewParticles())

        self.saveButtonLayout.addItem(spacer1)
        self.saveButtonLayout.addWidget(self.saveButton)
        self.saveButtonWidget.setLayout(self.saveButtonLayout)

        self.quantityOfTabs = 0

        for each in newCurrParticles:
            self.quantityOfTabs += 1
            tabName = os.path.basename(each).rsplit('.')[0]
            currPath = each
            print(each)
            self.createTab(tabName, self.quantityOfTabs, currPath)

        for i in range(self.quantityOfTabs):
            self.newIconsPaths.append(None)

        self.centralLayout.addWidget(self.tabWidget)
        self.centralLayout.addWidget(self.saveButtonWidget)
        self.centralWidget.setLayout(self.centralLayout)

        addParticles.setCentralWidget(self.centralWidget)

    def createTab(self, tabName, quantityOfTabs, currPath):
        self.tabField = QtWidgets.QWidget()
        self.tabField.setObjectName(tabName + 'Tab')
        self.tabWidget.addTab(self.tabField, '')
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabField), str(quantityOfTabs) + ' particle')

        tabMainLayout = QtWidgets.QHBoxLayout()
        tabMainLayout.setObjectName('tabMainLayout')
        tabMainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        formLayoutWidget = QtWidgets.QWidget()
        formLayoutWidget.setObjectName(tabName + "formLayoutWidget")
        formLayoutWidget.setMinimumWidth(450)

        formLayout = QtWidgets.QFormLayout(formLayoutWidget)
        formLayout.setContentsMargins(5, 5, 5, 5)
        formLayout.setHorizontalSpacing(20)
        formLayout.setObjectName(tabName + "formLayout")
        formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        nameLabel = QtWidgets.QLabel()
        nameLabel.setObjectName('nameLabel')
        nameLabel.setText('name')
        self.nameLineEdit = QtWidgets.QLineEdit()
        self.nameLineEdit.setObjectName('nameLineEdit')
        self.nameLineEdit.setText(tabName)
        self.nameLineEdit.textChanged.connect(lambda: self.connectData(self.tabWidget.currentWidget(), tabName))
        formLayout.addRow(nameLabel, self.nameLineEdit)

        descriptionLabel = QtWidgets.QLabel()
        descriptionLabel.setObjectName('descriptionLabel')
        descriptionLabel.setText('description')
        self.descriptionLineEdit = QtWidgets.QLineEdit()
        self.descriptionLineEdit.setObjectName('descriptionLineEdit')
        self.descriptionLineEdit.setText(self.nameLineEdit.text())
        formLayout.addRow(descriptionLabel, self.descriptionLineEdit)

        placementLabel = QtWidgets.QLabel()
        placementLabel.setObjectName('placementLabel')
        placementLabel.setText('placement')
        self.placementLineEdit = QtWidgets.QLineEdit()
        self.placementLineEdit.setObjectName('placementLineEdit')
        self.placementLineEdit.setText('limited')
        formLayout.addRow(placementLabel, self.placementLineEdit)

        typeLabel = QtWidgets.QLabel()
        typeLabel.setObjectName('typeLabel')
        typeLabel.setText('type')
        self.typeLineEdit = QtWidgets.QLineEdit()
        self.typeLineEdit.setObjectName('typeLineEdit')
        self.typeLineEdit.setText('object')
        formLayout.addRow(typeLabel, self.typeLineEdit)

        paramsLabel = QtWidgets.QLabel()
        paramsLabel.setObjectName('paramsLabel')
        font = QtGui.QFont()
        font.setPointSize(12)
        paramsLabel.setFont(font)
        paramsLabel.setText('params:')
        formLayout.addRow(paramsLabel, )

        classLabel = QtWidgets.QLabel()
        classLabel.setObjectName('classLabel')
        classLabel.setText('class')
        self.classLineEdit = QtWidgets.QLineEdit()
        self.classLineEdit.setObjectName('classLineEdit')
        self.classLineEdit.setText('InteractiveObject')
        formLayout.addRow(classLabel, self.classLineEdit)

        particleLabel = QtWidgets.QLabel()
        particleLabel.setObjectName('particleLabel')
        font = QtGui.QFont()
        font.setPointSize(12)
        particleLabel.setFont(font)
        particleLabel.setText('particle:')
        formLayout.addRow(particleLabel, )

        idLabel = QtWidgets.QLabel()
        idLabel.setObjectName('idLabel')
        idLabel.setText('particleId')
        self.idLineEdit = QtWidgets.QLineEdit()
        self.idLineEdit.setObjectName('idLineEdit')
        self.idLineEdit.setText(self.nameLineEdit.text())
        formLayout.addRow(idLabel, self.idLineEdit)

        modeLabel = QtWidgets.QLabel()
        modeLabel.setObjectName('modeLabel')
        modeLabel.setText('mode')
        self.modeLineEdit = QtWidgets.QLineEdit()
        self.modeLineEdit.setObjectName('modeLineEdit')
        self.modeLineEdit.setText('2')
        formLayout.addRow(modeLabel, self.modeLineEdit)

        obj_cmLabel = QtWidgets.QLabel()
        obj_cmLabel.setObjectName('obj_cmLabel')
        obj_cmLabel.setText('CreationModeInventory.json')
        self.obj_cmCheckBox = QtWidgets.QCheckBox()
        self.obj_cmCheckBox.setObjectName('obj_cmCheckBox')
        self.obj_cmCheckBox.setChecked(True)
        formLayout.addRow(obj_cmLabel, self.obj_cmCheckBox)

        ##########################################################################

        iconAreaWidget = QtWidgets.QWidget()
        iconAreaWidget.setObjectName('iconAreaWidget')

        iconLayout = QtWidgets.QVBoxLayout()
        iconLayout.setObjectName('iconLayout')
        iconLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        iconLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.pixLabel = QtWidgets.QLabel()
        self.pixLabel.setObjectName('pixLabel')
        self.pixLabel.setFixedSize(128, 128)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor('#D0D0D0'))
        self.pixLabel.setPalette(pal)
        self.pixLabel.setAutoFillBackground(True)

        self.setIconButton = QtWidgets.QPushButton()
        self.setIconButton.setObjectName('setIconButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(10)
        self.setIconButton.setFont(font)
        self.setIconButton.setMinimumHeight(30)
        self.setIconButton.setText('ADD ICON')
        self.setIconButton.clicked.connect(lambda bool, currPixLabel=self.pixLabel,
                                                  tab=quantityOfTabs: self.setIcon(currPixLabel, tab))

        tipsLabel = QtWidgets.QLabel()
        tipsLabel.setObjectName('tipsLabel')
        tipsLabel.setText('Mode:\n1 - world\n2 - local')

        spacerV1 = QtWidgets.QSpacerItem(40, 40, QtWidgets.QSizePolicy.Policy.Fixed,
                                         QtWidgets.QSizePolicy.Policy.Expanding)

        iconLayout.addWidget(self.pixLabel)
        iconLayout.addWidget(self.setIconButton)
        iconLayout.addWidget(tipsLabel)
        iconLayout.addItem(spacerV1)
        iconAreaWidget.setLayout(iconLayout)

        tabMainLayout.addWidget(formLayoutWidget)
        tabMainLayout.addWidget(iconAreaWidget)
        self.tabField.setLayout(tabMainLayout)

        oldPath = QtWidgets.QLineEdit(self.tabField)
        oldPath.setObjectName(tabName + 'oldPath')
        oldPath.setText(currPath)
        oldPath.hide()

    def connectData(self, tab, tabName):
        formLayout = tab.findChild(QtWidgets.QFormLayout, tabName + 'formLayout')
        name = formLayout.itemAt(1).widget().text()
        description = formLayout.itemAt(3).widget()
        description.setText(name)
        particleId = formLayout.itemAt(13).widget()
        particleId.setText(name)

    def cubelariaDBOpen(self):
        self.cubelariaDBDict = {}
        self.dBParticlesList = []
        with open(Paths.objectsDb, 'r', encoding='utf8') as cubelariaDB:
            self.cubelariaDBDict = json.load(cubelariaDB)
            for each in self.cubelariaDBDict['particles']:
                self.dBParticlesList.append(each)

    def setIcon(self, label, tab):
        fileDialog = QtWidgets.QFileDialog()
        currIcon = fileDialog.getOpenFileName(filter='PNG (*.png)')[0]
        pixmap = QtGui.QPixmap(currIcon).scaled(128, 128, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        label.setPixmap(pixmap)
        try:
            self.newIconsPaths[tab-1] = currIcon
        except IndexError:
            self.newIconsPaths[tab] = currIcon
        print(self.newIconsPaths)

    def updateCubJson(self, tab):
        tabName = tab.objectName().rsplit('Tab')[0]
        formLayout = tab.findChild(QtWidgets.QFormLayout, tabName + 'formLayout')

        particle = {}
        particle['particleId'] = formLayout.itemAt(13).widget().text()
        particle['mode'] = int(formLayout.itemAt(15).widget().text())

        params = {}
        params['class'] = formLayout.itemAt(10).widget().text()
        params['particle'] = particle

        obj = {}
        obj['name'] = formLayout.itemAt(1).widget().text()
        obj['description'] = formLayout.itemAt(3).widget().text()
        obj['placement'] = formLayout.itemAt(5).widget().text()
        obj['type'] = formLayout.itemAt(7).widget().text()
        obj['params'] = params

        return obj

    def saveNewParticles(self):
        cmState = StaticMethods.getCreationModeInventoryState(Paths.creationModeInventory)
        for each in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(each)
            tabName = tab.objectName().rsplit('Tab')[0]
            formLayout = tab.findChild(QtWidgets.QFormLayout, tabName + 'formLayout')
            name = formLayout.itemAt(1).widget().text()
            oldPath = tab.findChild(QtWidgets.QLineEdit, tabName + 'oldPath').text()
            if os.path.exists(os.path.join(Paths.particles, name + '.ptc')):
                questionBox = QtWidgets.QMessageBox()
                questionBox.setWindowTitle('Replace')
                questionBox.setIcon(QtWidgets.QMessageBox.Question)
                questionBox.setText('Particle ' + name + ' already exists in directory. Do you want to replace?')
                questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                button = questionBox.exec()

                if button == QtWidgets.QMessageBox.Yes:
                    os.remove(os.path.join(Paths.particles, name + '.ptc'))
                    shutil.copyfile(oldPath, os.path.join(Paths.particles, name + '.ptc'))

                elif button == QtWidgets.QMessageBox.No:
                    return
            else:
                shutil.copyfile(oldPath, os.path.join(Paths.particles, name + '.ptc'))

            existanceFlag = False
            for eachParticle in self.dBParticlesList:
                if eachParticle['name'] == name:
                    existanceFlag = True

            if existanceFlag == False:
                self.dBParticlesList.append(self.updateCubJson(tab))
            else:
                pass


            checkbox = formLayout.itemAt(17).widget()

            if checkbox.isChecked():
                StaticMethods.addObjectInCreationModeInventory(cmState, name, 'particles')
            else:
                pass

            if self.newIconsPaths[each] != None:
                if os.path.exists(os.path.join(Paths.icons, 'particles', name + '.png')):
                    questionBox = QtWidgets.QMessageBox()
                    questionBox.setWindowTitle('Replace')
                    questionBox.setIcon(QtWidgets.QMessageBox.Question)
                    questionBox.setText('Icon ' + name + ' already exists in directory. Do you want to replace?')
                    questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    button = questionBox.exec()

                    if button == QtWidgets.QMessageBox.Yes:
                        os.remove(os.path.join(Paths.icons, 'particles', name + '.png'))
                        shutil.copyfile(self.newIconsPaths[each],
                                        os.path.join(Paths.icons, 'particles', name + '.png'))
                else:
                    shutil.copyfile(self.newIconsPaths[each],
                                    os.path.join(Paths.icons, 'particles', name + '.png'))


        self.cubelariaDBDict['particles'] = self.dBParticlesList

        with open(Paths.objectsDb, 'w', encoding='utf8') as dbFile:
            json.dump(self.cubelariaDBDict, dbFile, indent=3, ensure_ascii=False, separators=(',', ':'))

        StaticMethods.updateCreationModeInventoryFile(cmState, Paths.creationModeInventory)
        self.addParticles.close()

    def createNewObjForInventory(self, name):
        obj = {}
        obj['name'] = 'particles::' + name
        obj['quantity'] = 100

        return obj

    def addParticleToBundleInventory(self, name):
        with open(os.path.join(Paths.bundles, 'inventory.json'), 'r') as inventoryJson:
            inventoryJsonList = json.load(inventoryJson)

        for eachObj in inventoryJsonList:
            if eachObj['name'] == 'particles::' + name:
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


class Ui_EditParticle(Ui_AddParticles):
    def __init__(self, win, listForEditing):
        super(Ui_EditParticle, self).__init__(win, listForEditing)
        self.setupUi(win, listForEditing)
        win.show()

    def setupUi(self, addParticles, newCurrParticles):
        super(Ui_EditParticle, self).setupUi(addParticles, newCurrParticles)
        self.saveButton.clicked.disconnect()
        self.saveButton.clicked.connect(lambda: self.updateParticle())

    def createTab(self, tabName, quantityOfTabs, currPath):
        cmState = StaticMethods.getCreationModeInventoryState(Paths.creationModeInventory)
        super(Ui_EditParticle, self).createTab(tabName, quantityOfTabs, currPath)
        self.prevName = tabName
        self.descriptionLineEdit.setText(self.searchInDbParticlesList()['description'])
        self.placementLineEdit.setText(self.searchInDbParticlesList()['placement'])
        self.typeLineEdit.setText(self.searchInDbParticlesList()['type'])
        self.classLineEdit.setText(self.searchInDbParticlesList()['params']['class'])
        self.idLineEdit.setText(self.searchInDbParticlesList()['params']['particle']['particleId'])
        self.modeLineEdit.setText(str(self.searchInDbParticlesList()['params']['particle']['mode']))
        if self.prevName in cmState['particles']:
            self.obj_cmCheckBox.setChecked(True)
        else:
            self.obj_cmCheckBox.setChecked(False)
        self.setIconButton.setText('EDIT ICON')

        pathToCurrItem = os.path.join(Paths.icons, 'particles', tabName.rsplit('.')[0] + '.png')

        if os.path.exists(pathToCurrItem):
            pixmap = QtGui.QPixmap(pathToCurrItem).scaled(128, 128, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        else:
            pixmap = QtGui.QPixmap(os.path.join(Paths.icons, 'misc', 'missing.png')).scaled(128, 128, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        self.pixLabel.setPixmap(pixmap)

    def searchInDbParticlesList(self):
        currObj = {}
        for eachObj in self.dBParticlesList:
            if eachObj['name'] == self.prevName:
                currObj = eachObj
        return currObj

    def updateParticle(self):
        cmState = StaticMethods.getCreationModeInventoryState(Paths.creationModeInventory)
        for each in range(self.tabWidget.count()):
            tab = self.tabWidget.widget(each)
            tabName = tab.objectName().rsplit('Tab')[0]
            formLayout = tab.findChild(QtWidgets.QFormLayout, tabName + 'formLayout')
            name = formLayout.itemAt(1).widget().text()
            for i in range(len(self.dBParticlesList)):
                if self.dBParticlesList[i]['name'] == self.prevName:
                    print(self.dBParticlesList[i])
                    self.dBParticlesList[i] = self.updateCubJson(tab)
                    print(self.dBParticlesList[i])
            try:
                os.rename(os.path.join(Paths.particles, self.prevName + '.ptc'),
                          os.path.join(Paths.particles, name + '.ptc'))
            except FileExistsError:
                pass

            obj_cmCheckbox = formLayout.itemAt(17).widget()
            if obj_cmCheckbox.isChecked():
                if self.prevName != name:
                    StaticMethods.deleteObjectFromCreationModeInventory(cmState, [self.prevName], 'particles')
                    StaticMethods.addObjectInCreationModeInventory(cmState, name, 'particles')
                else:
                    StaticMethods.addObjectInCreationModeInventory(cmState, name, 'particles')
            else:
                StaticMethods.deleteObjectFromCreationModeInventory(cmState, [self.prevName], 'particles')

            if self.prevName != name:

                questionBox = QtWidgets.QMessageBox()
                questionBox.setWindowTitle('Delete')
                questionBox.setIcon(QtWidgets.QMessageBox.Question)
                questionBox.setText('Do you want to rename ' + name + ' icon?')
                questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                button = questionBox.exec()

                if button == QtWidgets.QMessageBox.Yes:
                    os.rename(os.path.join(Paths.icons, 'particles', self.prevName + '.png'),
                              os.path.join(Paths.icons, 'particles', name + '.png'))

            if self.newIconsPaths[each] != None:
                if os.path.exists(os.path.join(Paths.icons, 'particles', name + '.png')):
                    questionBox = QtWidgets.QMessageBox()
                    questionBox.setWindowTitle('Replace')
                    questionBox.setIcon(QtWidgets.QMessageBox.Question)
                    questionBox.setText('Icon ' + name + ' already exists in directory. Do you want to replace?')
                    questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    button = questionBox.exec()

                    if button == QtWidgets.QMessageBox.Yes:
                        os.remove(os.path.join(Paths.icons, 'particles', name + '.png'))
                        shutil.copyfile(self.newIconsPaths[each],
                                        os.path.join(Paths.icons, 'particles', name + '.png'))
                else:
                    shutil.copyfile(self.newIconsPaths[each],
                                    os.path.join(Paths.icons, 'particles', name + '.png'))

        self.cubelariaDBDict['particles'] = self.dBParticlesList

        with open(Paths.objectsDb, 'w', encoding='utf8') as dbFile:
            json.dump(self.cubelariaDBDict, dbFile, indent=3, ensure_ascii=False, separators=(',', ':'))

        StaticMethods.updateCreationModeInventoryFile(cmState, Paths.creationModeInventory)
        self.addParticles.close()

    def renameInBundleInventory(self, prevName, name):
        with open(os.path.join(Paths.bundles, 'inventory.json'), 'r', encoding='utf8') as inventoryJson:
            inventoryJsonList = json.load(inventoryJson)

        for eachObj in inventoryJsonList:
            if str(eachObj['name']).lower().rsplit('::')[0] == 'particles':
                if str(eachObj['name']).lower().rsplit('particles::')[1] == prevName:
                    eachObj['name'] = 'particles::' + name

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
