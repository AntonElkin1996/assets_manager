from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os
import shutil
import subprocess
from managerPaths import Paths

class MainWindowCloseRmDir(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, prevWin, addedBundlePath):
        super().__init__()
        self.prevWin = prevWin
        self.addedBundlePath = addedBundlePath
        self.currWidth = (self.size().width() // 155) - 2

    def rmCurrDir(self, addedBundlePath):
        try:
            shutil.rmtree(addedBundlePath)
        except:
            pass

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.rmCurrDir(self.addedBundlePath)
        self.prevWin.updateWindow()

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if ((self.size().width() // 155) - 2) != self.currWidth:
            self.resized.emit()
            self.currWidth = ((self.size().width() // 155) - 2)
        return super(MainWindowCloseRmDir, self).resizeEvent(a0)

class ListWidget(QtWidgets.QListWidget):
    def __init__(self, parent, win):
        super().__init__(parent)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)

class Ui_bundleSetup(object):
    def __init__(self, win):
        self.setupUi(win)
        win.show()

    def openWindow(self, bundleName, ui, currentPath):
        if ui == Ui_bundleMenu:
            self.window = MainWindowCloseRmDir(self, addedBundlePath=None)
            Ui_bundleMenu(self.window, bundleName, currentPath)
        elif ui == Ui_AddLevelWindow:
            self.window = QtWidgets.QMainWindow()
            Ui_AddLevelWindow(self.window, self)

    def updateWindow(self):
        self.setupUi(self.bundleSetupWindow)
        self.bundleSetupWindow.update()

    def setupUi(self, bundleSetup):
        self.bundleSetupWindow = bundleSetup
        bundleSetup.setObjectName("bundleSetup")
        bundleSetup.setWindowTitle('bundleSetup')
        self.centralwidget = QtWidgets.QWidget(bundleSetup)
        self.centralwidget.setObjectName("centralwidget")

        self.centralLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.bundlesWidget = QtWidgets.QWidget(self.centralwidget)
        self.bundlesWidget.setObjectName('bundlesWidget')

        self.bundlesLayout = QtWidgets.QVBoxLayout(self.bundlesWidget)
        self.bundlesLayout.setObjectName('bundlesLayout')
        self.bundlesLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.bundlesLabel = QtWidgets.QLabel(self.centralwidget)
        self.bundlesLabel.setObjectName('bundlesCubLabel')
        self.bundlesLabel.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(16)
        self.bundlesLabel.setFont(font)
        self.bundlesLabel.setText('Bundles')

        self.bundleVarNameList = []

        self.bundlesListWidget = ListWidget(self.centralwidget, self)
        self.bundlesListWidget.setObjectName('bundlesListWidget')
        self.bundlesListWidget.setGeometry(40, 90, 300, 600)
        self.fillBundles(listwidget=self.bundlesListWidget)
        self.bundlesListWidget.itemDoubleClicked.connect(
            lambda: self.openWindow(bundleName=self.bundlesListWidget.currentItem().text(),
                                    ui=Ui_bundleMenu, currentPath=''))

        print(self.bundleVarNameList)

        self.buttonsWidget = QtWidgets.QWidget(self.centralwidget)
        self.buttonsWidget.setObjectName('buttonsWidget')

        self.buttonsLayout = QtWidgets.QVBoxLayout(self.buttonsWidget)
        self.buttonsLayout.setObjectName('buttonsLayout')
        self.buttonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.addNewBundleButton = QtWidgets.QPushButton(self.centralwidget)
        self.addNewBundleButton.setGeometry(QtCore.QRect(400, 150, 250, 40))
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.addNewBundleButton.setFont(font)
        self.addNewBundleButton.setObjectName("addNewBundleButton")
        self.addNewBundleButton.setText('ADD NEW')
        self.addNewBundleButton.setMinimumHeight(35)
        self.addNewBundleButton.clicked.connect(lambda: self.openWindow(bundleName='', ui=Ui_AddLevelWindow, currentPath=''))

        self.deleteBundleButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteBundleButton.setGeometry(QtCore.QRect(400, 200, 250, 40))
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.deleteBundleButton.setFont(font)
        self.deleteBundleButton.setObjectName("deleteBundleButton")
        self.deleteBundleButton.setText('DELETE')
        self.deleteBundleButton.setMinimumHeight(35)
        self.deleteBundleButton.clicked.connect(lambda: self.deleteBundle(self.bundlesListWidget))

        spacer1 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        spacer2 = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)

        self.bundlesLayout.addWidget(self.bundlesLabel)
        self.bundlesLayout.addWidget(self.bundlesListWidget)
        self.bundlesWidget.setLayout(self.bundlesLayout)

        self.buttonsLayout.addItem(spacer1)
        self.buttonsLayout.addWidget(self.addNewBundleButton)
        self.buttonsLayout.addWidget(self.deleteBundleButton)
        self.buttonsLayout.addItem(spacer2)
        self.buttonsWidget.setLayout(self.buttonsLayout)

        self.centralLayout.addWidget(self.bundlesWidget, 5)
        self.centralLayout.addWidget(self.buttonsWidget, 5)
        self.bundlesWidget.setLayout(self.centralLayout)

        bundleSetup.setCentralWidget(self.centralwidget)

    def deleteBundle(self, bundleList):
        selectedItems = []
        for each in bundleList.selectedItems():
            selectedItems.append(each.text())
        if not selectedItems:
            return
        questionBox = QtWidgets.QMessageBox()
        questionBox.setWindowTitle('Delete')
        questionBox.setIcon(QtWidgets.QMessageBox.Question)
        questionBox.setText('Are you sure you want to delete ' + str(selectedItems) + ' bundles?')
        questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        button = questionBox.exec()

        if button == QtWidgets.QMessageBox.Yes:
            for each in selectedItems:
                deletionPath = os.path.join(Paths.bundles, each)
                shutil.rmtree(deletionPath)
            self.updateWindow()

    def fillBundles(self, listwidget):
        for dir in os.listdir(Paths.bundles):
            if os.path.isdir(os.path.join(Paths.bundles, dir)):
                bundleVarName = dir
                self.bundleVarNameList.append(bundleVarName)
                listwidget.addItem(str(bundleVarName))

class Ui_bundleMenu(object):
    def __init__(self, win, bundleName, currentPath):
        self.currentPath = currentPath
        self.bundleMenuWindow = win
        self.bundleName = bundleName
        with open(os.path.join(Paths.bundles, self.bundleName, 'world', 'spawn.json'), 'r') as self.jsonObjects:
            self.jsonObjectsDict = json.load(self.jsonObjects)
        with open(os.path.join(Paths.bundles, self.bundleName, 'config.json'), 'r') as self.jsonConfig:
            self.jsonConfigDict = json.load(self.jsonConfig)
        self.createInventoryMap()
        self.currQuantityForGrid = (self.bundleMenuWindow.size().width() // 155) - 2
        self.setupUi(win)
        self.bundleMenuWindow.show()

    def createInventoryMap(self):
        self.objectsDict = {}

        with open(Paths.objectsDb, 'r') as self.objDB:
            self.objDBDict = json.load(self.objDB)

        with open(Paths.blocksDb, 'r') as self.blocksDB:
            self.blocksDBDict = json.load(self.blocksDB)

        if os.path.exists(os.path.join(Paths.bundles, self.bundleName, 'game', 'inventory.json')):
            with open(os.path.join(Paths.bundles, self.bundleName, 'game', 'inventory.json'), 'r') as self.inventoryJson:
                self.inventoryJsonDict = json.load(self.inventoryJson)

        self.inventoryAssetsList = ["creatures", "objects", "blocks", "particles"]

        for eachType in self.inventoryAssetsList:
            typeList = []
            if eachType == 'blocks':
                pathToIcons = os.path.join(Paths.icons, eachType)
                for eachObj in self.blocksDBDict[eachType]:
                    obj = {}
                    obj['name'] = eachObj['name']
                    try:
                        for i in self.inventoryJsonDict:
                            if i['name'] == eachType + '::' + eachObj['name']:
                                obj['quantity'] = i['quantity']
                                break
                            else:
                                obj['quantity'] = 0
                    except:
                        obj['quantity'] = 0

                    for eachIcon in os.listdir(pathToIcons):
                        obj['pathToIcon'] = ''
                        if eachIcon.rsplit('.')[0] == eachObj['name']:
                            obj['pathToIcon'] = os.path.join(Paths.icons, eachType, eachIcon)
                            break
                    if obj['pathToIcon'] == '':
                        obj['pathToIcon'] = os.path.join(Paths.icons, 'misc', 'missing.png')

                    typeList.append(obj)

                self.objectsDict[eachType] = typeList

            else:
                pathToIcons = os.path.join(Paths.icons, eachType)
                for eachObj in self.objDBDict[eachType]:
                    obj = {}
                    obj['name'] = eachObj['name']
                    try:
                        for i in self.inventoryJsonDict:
                            if i['name'] == eachType + '::' + eachObj['name']:
                                obj['quantity'] = i['quantity']
                                break
                            else:
                                obj['quantity'] = 0
                    except:
                        obj['quantity'] = 0

                    for eachIcon in os.listdir(pathToIcons):
                        obj['pathToIcon'] = ''
                        if eachIcon.rsplit('.')[0] == eachObj['name']:
                            obj['pathToIcon'] = os.path.join(Paths.icons, eachType, eachIcon)
                            break
                    if obj['pathToIcon'] == '':
                        obj['pathToIcon'] = os.path.join(Paths.icons, 'misc', 'missing.png')

                    typeList.append(obj)

                self.objectsDict[eachType] = typeList

    def setupUi(self, bundleMenu):
        bundleMenu.setObjectName("bundleMenu")
        bundleMenu.resize(900, 500)

        self.centralwidget = QtWidgets.QWidget(bundleMenu)
        self.centralwidget.setObjectName("centralwidget")

        self.centralLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.saveButtonWidget = QtWidgets.QWidget()
        self.saveButtonWidget.setObjectName('saveButtonWidget')
        self.saveButtonWidget.setMaximumHeight(100)

        self.saveButtonLayout = QtWidgets.QHBoxLayout()
        self.saveButtonLayout.setObjectName('saveButtonLayout')
        self.saveButtonLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        spacer1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        self.saveButton = QtWidgets.QPushButton(clicked=lambda: self.confirm())
        self.saveButton.setObjectName('saveButton')
        self.saveButton.setFixedSize(QtCore.QSize(170, 35))
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(12)
        self.saveButton.setFont(font)
        self.saveButton.setStyleSheet('background-color: #ECFFC9;')
        self.saveButton.setText('SAVE')

        self.saveButtonLayout.addItem(spacer1)
        self.saveButtonLayout.addWidget(self.saveButton)
        self.saveButtonWidget.setLayout(self.saveButtonLayout)

        self.bundleMenuTabWidget = QtWidgets.QTabWidget()
        self.bundleMenuTabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.bundleMenuTabWidget.setObjectName("bundleMenuTabWidget")

        ####################### CONFIG TAB #####################################

        self.config = QtWidgets.QWidget()
        self.config.setObjectName("config")

        self.mainConfigLayout = QtWidgets.QVBoxLayout()
        self.mainConfigLayout.setObjectName('mainConfigLayout')
        self.mainConfigLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.upperConfigWidget = QtWidgets.QWidget()
        self.upperConfigWidget.setObjectName('upperConfigWidget')

        self.upperConfigLayout = QtWidgets.QHBoxLayout()
        self.upperConfigLayout.setObjectName('upperConfigLayout')
        self.upperConfigLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.lowerConfigWidget = QtWidgets.QWidget()
        self.lowerConfigWidget.setObjectName('lowerConfigWidget')

        self.lowerConfigLayout = QtWidgets.QHBoxLayout()
        self.lowerConfigLayout.setObjectName('lowerConfigLayout')
        self.lowerConfigLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lowerConfigLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.logoAndBackgroundWidget = QtWidgets.QWidget()
        self.logoAndBackgroundWidget.setObjectName('logoAndBackgroundWidget')

        self.logoAndBackgroundLayout = QtWidgets.QHBoxLayout()
        self.logoAndBackgroundLayout.setObjectName('logoAndBackgroundLayout')
        self.logoAndBackgroundLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.logoWidget = QtWidgets.QWidget()
        self.logoWidget.setObjectName('logoWidget')
        self.logoWidget.setMinimumWidth(192)

        self.logoLayout = QtWidgets.QVBoxLayout()
        self.logoLayout.setObjectName('logoLayout')
        self.logoLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.backgroundWidget = QtWidgets.QWidget()
        self.backgroundWidget.setObjectName('backgroundWidget')
        self.backgroundWidget.setMinimumWidth(192)

        self.backgroundLayout = QtWidgets.QVBoxLayout()
        self.backgroundLayout.setObjectName('backgroundLayout')
        self.backgroundLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.labelLogoPic = QtWidgets.QLabel()
        self.labelLogoPic.setObjectName('labelLogoPic')
        self.labelLogoPic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if os.path.exists(os.path.join(Paths.bundles, self.bundleName, 'lobby', 'icon.png')):
            self.pixmap = QtGui.QPixmap(os.path.join(Paths.bundles, self.bundleName, 'lobby', 'icon.png'))
        else:
            self.pixmap = QtGui.QPixmap(os.path.join(Paths.icons, 'misc', 'default_game_logo.png'))
        self.oldIconPath = os.path.join(Paths.bundles, self.bundleName, 'lobby', 'icon.png')
        self.labelLogoPic.setPixmap(self.pixmap)
        self.logoIsEditedFlag = False

        self.editLogoButton = QtWidgets.QPushButton(clicked=lambda: self.editLogo())
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(10)
        self.editLogoButton.setFont(font)
        self.editLogoButton.setObjectName("editLogoButton")
        self.editLogoButton.setText("EDIT LOGO")

        self.backgroundLabelPic = QtWidgets.QLabel()
        self.backgroundLabelPic.setObjectName('backgroundLabelPic')
        self.backgroundLabelPic.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if os.path.exists(os.path.join(Paths.bundles, self.bundleName, 'lobby', 'background.png')):
            self.bgPixmap = QtGui.QPixmap(
                os.path.join(Paths.bundles, self.bundleName, 'lobby', 'background.png')).scaled(192, 128)
        else:
            self.bgPixmap = QtGui.QPixmap(os.path.join(Paths.icons, 'backgrounds', 'lobby')).scaled(192, 128)
        self.oldBackgroundPath = os.path.join(Paths.bundles, self.bundleName, 'lobby', 'background.png')
        self.backgroundLabelPic.setPixmap(self.bgPixmap)
        self.bgEditedFlag = False

        self.editBackgroundButton = QtWidgets.QPushButton()
        self.editBackgroundButton.setObjectName('editBackgroundButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(10)
        self.editBackgroundButton.setFont(font)
        self.editBackgroundButton.setText('EDIT BACKGROUND')
        self.editBackgroundButton.clicked.connect(lambda: self.editBackground())

        self.logoLayout.addWidget(self.labelLogoPic)
        self.logoLayout.addWidget(self.editLogoButton)
        self.logoWidget.setLayout(self.logoLayout)

        self.backgroundLayout.addWidget(self.backgroundLabelPic)
        self.backgroundLayout.addWidget(self.editBackgroundButton)
        self.backgroundWidget.setLayout(self.backgroundLayout)

        self.logoAndBackgroundLayout.addWidget(self.logoWidget, 5)
        self.logoAndBackgroundLayout.addWidget(self.backgroundWidget, 5)
        self.logoAndBackgroundWidget.setLayout(self.logoAndBackgroundLayout)

        self.formLayoutWidget = QtWidgets.QWidget()
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayoutWidget.setMinimumWidth(380)

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(5, 5, 5, 5)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)

        ####################################################################################

        self.folderNameLabel = QtWidgets.QLabel()
        self.folderNameLabel.setObjectName("folderName")
        self.folderNameLineEdit = QtWidgets.QLineEdit()
        self.folderNameLineEdit.setObjectName("folderNameLineEdit")
        self.folderNameLineEdit.setText(self.bundleName)
        self.formLayout.addRow(self.folderNameLabel, self.folderNameLineEdit)

        self.levelNameLabel = QtWidgets.QLabel()
        self.levelNameLabel.setObjectName("levelName")
        self.levelNameLineEdit = QtWidgets.QLineEdit()
        self.levelNameLineEdit.setObjectName("levelNameLineEdit")
        self.levelNameLineEdit.setText(str(self.jsonConfigDict['name']))
        self.formLayout.addRow(self.levelNameLabel, self.levelNameLineEdit)

        self.onlyInt = QtGui.QIntValidator()

        self.idLabel = QtWidgets.QLabel()
        self.idLabel.setObjectName("id")
        self.idLabel.setAlignment(QtCore.Qt.AlignRight)
        self.idLineEdit = QtWidgets.QLineEdit()
        self.idLineEdit.setObjectName("idLineEdit")
        self.idLineEdit.setValidator(self.onlyInt)
        self.idLineEdit.setText(str(self.jsonConfigDict['id']))
        self.formLayout.addRow(self.idLabel, self.idLineEdit)

        self.likesLabel = QtWidgets.QLabel()
        self.likesLabel.setObjectName("likes")
        self.likesLineEdit = QtWidgets.QLineEdit()
        self.likesLineEdit.setObjectName("likesLineEdit")
        self.likesLineEdit.setValidator(self.onlyInt)
        self.likesLineEdit.setText(str(self.jsonConfigDict['likes']))
        self.formLayout.addRow(self.likesLabel, self.likesLineEdit)

        self.minPlayersLabel = QtWidgets.QLabel()
        self.minPlayersLabel.setObjectName("minPlayers")
        self.minPlayersLineEdit = QtWidgets.QLineEdit()
        self.minPlayersLineEdit.setObjectName("minPlayersLineEdit")
        self.minPlayersLineEdit.setValidator(self.onlyInt)
        self.minPlayersLineEdit.setText(str(self.jsonConfigDict['minPlayers']))
        self.formLayout.addRow(self.minPlayersLabel, self.minPlayersLineEdit)

        self.maxPlayersLabel = QtWidgets.QLabel()
        self.maxPlayersLabel.setObjectName("maxPlayers")
        self.maxPlayersLineEdit = QtWidgets.QLineEdit()
        self.maxPlayersLineEdit.setObjectName("maxPlayersLineEdit")
        self.maxPlayersLineEdit.setValidator(self.onlyInt)
        self.maxPlayersLineEdit.setText(str(self.jsonConfigDict['maxPlayers']))
        self.formLayout.addRow(self.maxPlayersLabel, self.maxPlayersLineEdit)

        self.formLayoutWidget.setLayout(self.formLayout)

        self.upperConfigLayout.addWidget(self.formLayoutWidget, 5)
        self.upperConfigLayout.addWidget(self.logoAndBackgroundWidget, 5)
        self.upperConfigWidget.setLayout(self.upperConfigLayout)

        ##################################################################################

        self.descriptionMainWidget = QtWidgets.QWidget()
        self.descriptionMainWidget.setObjectName('descriptionMainWidget')

        self.descriptionMainLayout = QtWidgets.QVBoxLayout()
        self.descriptionMainLayout.setObjectName('descriptionMainLayout')
        self.descriptionMainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.descriptionList = str(self.jsonConfigDict['description']).rsplit('\n')

        if len(self.descriptionList) < 8:
            for each in range(8):
                try:
                    if self.descriptionList[each] != '':
                        continue
                except IndexError:
                    self.descriptionList.append('')

        self.descriptionLayoutWidget = QtWidgets.QWidget()
        self.descriptionLayoutWidget.setObjectName("descriptionLayoutWidget")

        self.descriptionLayout = QtWidgets.QVBoxLayout()
        self.descriptionLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.descriptionLayout.setObjectName("descriptionLayout")
        self.descriptionLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.descriptionLineEditList = []
        for each in range(8):
            self.descriptionLineEditList.append(QtWidgets.QLineEdit())
            self.descriptionLineEditList[each].setObjectName("descriptionLineEdit" + str(each))
            self.descriptionLineEditList[each].setMaxLength(46)
            self.descriptionLineEditList[each].setText(self.descriptionList[each])
            self.descriptionLayout.addWidget(self.descriptionLineEditList[each])

        self.descriptionLayoutWidget.setLayout(self.descriptionLayout)

        self.descriptionMainLayout.addWidget(self.descriptionLayoutWidget, 9)
        self.descriptionMainWidget.setLayout(self.descriptionMainLayout)

        self.spawnPointWidget = QtWidgets.QWidget()
        self.spawnPointWidget.setObjectName('spawnPointWidget')

        self.spawnPointLayout = QtWidgets.QVBoxLayout(self.spawnPointWidget)
        self.spawnPointLayout.setObjectName('spawnPointLayout')
        self.spawnPointLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.editSpawnPointButton = QtWidgets.QRadioButton(clicked=lambda: self.enableField(field=self.avatarParamsWidget))
        self.editSpawnPointButton.setObjectName('editSpawnPointButton')
        self.editSpawnPointButton.setText('edit spawn point')

        self.avatarParamsWidget = QtWidgets.QWidget()
        self.avatarParamsWidget.setObjectName('avatarParamsWidget')
        self.avatarParamsWidget.setEnabled(False)

        self.avatarParamsLayout = QtWidgets.QFormLayout(self.avatarParamsWidget)
        self.avatarParamsLayout.setObjectName('avatarParamsLayout')

        self.xLabel = QtWidgets.QLabel()
        self.xLabel.setObjectName('xLabel')
        self.xLabel.setText('x')
        self.xLineEdit = QtWidgets.QLineEdit()
        self.xLineEdit.setObjectName('xLineEdit')
        self.xLineEdit.setValidator(self.onlyInt)
        self.avatarParamsLayout.addRow(self.xLabel, self.xLineEdit)

        self.yLabel = QtWidgets.QLabel()
        self.yLabel.setObjectName('yLabel')
        self.yLabel.setText('y')
        self.yLineEdit = QtWidgets.QLineEdit()
        self.yLineEdit.setObjectName('yLineEdit')
        self.yLineEdit.setValidator(self.onlyInt)
        self.avatarParamsLayout.addRow(self.yLabel, self.yLineEdit)

        self.zLabel = QtWidgets.QLabel()
        self.zLabel.setObjectName('zLabel')
        self.zLabel.setText('z')
        self.zLineEdit = QtWidgets.QLineEdit()
        self.zLineEdit.setObjectName('zLineEdit')
        self.zLineEdit.setValidator(self.onlyInt)
        self.avatarParamsLayout.addRow(self.zLabel, self.zLineEdit)

        self.spawnPointLayout.addWidget(self.avatarParamsWidget)

        for avatar in self.jsonObjectsDict['Avatar']:
            self.xLineEdit.setText(str(avatar['x']))
            self.yLineEdit.setText(str(avatar['y']))
            self.zLineEdit.setText(str(avatar['z']))

        self.spawnPointLayout.addWidget(self.editSpawnPointButton)
        self.spawnPointLayout.addWidget(self.avatarParamsWidget)
        self.spawnPointWidget.setLayout(self.spawnPointLayout)

        self.lowerConfigLayout.addWidget(self.descriptionMainWidget, 5)
        self.lowerConfigLayout.addWidget(self.spawnPointWidget, 5)
        self.lowerConfigWidget.setLayout(self.lowerConfigLayout)

        self.mainConfigLayout.addWidget(self.upperConfigWidget)
        self.mainConfigLayout.addWidget(self.lowerConfigWidget)
        self.config.setLayout(self.mainConfigLayout)

        self.bundleMenuTabWidget.addTab(self.config, "")

        ############################## END CONFIG TAB ##############################################
        ############################## INVENTORY TAB ###############################################

        self.inventoryMainWidget = QtWidgets.QWidget()
        self.inventoryMainWidget.setObjectName("inventory")

        self.inventoryMainLayout = QtWidgets.QVBoxLayout()
        self.inventoryMainLayout.setObjectName('inventoryMainLayout')
        self.inventoryMainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.inventoryTabWidget = QtWidgets.QTabWidget()
        self.inventoryTabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.inventoryTabWidget.setObjectName("inventoryTabWidget")

        self.inventoryMainLayout.addWidget(self.inventoryTabWidget)
        self.inventoryMainWidget.setLayout(self.inventoryMainLayout)

        for asset in self.inventoryAssetsList:
            self.fillInventorySettings(asset)

        self.bundleMenuTabWidget.addTab(self.inventoryMainWidget, "")

        ############################## END INVENTORY TAB ##############################################

        self.levelAndSkymap = QtWidgets.QWidget()
        self.levelAndSkymap.setObjectName("levelAndSkymap")

        self.skymapMainLayout = QtWidgets.QVBoxLayout()
        self.skymapMainLayout.setObjectName('skymapMainLayout')
        self.skymapMainLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.skymapMainLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.skyboxesWidget = QtWidgets.QWidget()
        self.skyboxesWidget.setObjectName("skyboxesWidget")
        self.skyboxesWidget.setMaximumSize(400, 200)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Background, QtGui.QColor('#D0D0D0'))
        self.skyboxesWidget.setPalette(pal)
        self.skyboxesWidget.setAutoFillBackground(True)

        self.skyboxesLayout = QtWidgets.QVBoxLayout()
        self.skyboxesLayout.setObjectName("skyboxesLayout")

        self.skymapEnable = QtWidgets.QRadioButton(clicked = lambda: self.enableField(field=self.skyboxesFolderWidget))
        self.skymapEnable.setObjectName("skymapEnable")
        self.skymapEnable.setText("add skymap")
        self.skyboxesLayout.addWidget(self.skymapEnable)

        self.skyboxesFolderWidget = QtWidgets.QWidget()
        self.skyboxesFolderWidget.setObjectName("skyboxesFolderWidget")
        self.skyboxesFolderWidget.setEnabled(False)

        self.skyboxesFolderLayout = QtWidgets.QGridLayout()
        self.skyboxesFolderLayout.setObjectName("skyboxesFolderLayout")
        self.skyboxesFolderLayout.setContentsMargins(5, 5, 5, 5)

        self.skyboxLineEdit = QtWidgets.QLineEdit()
        self.skyboxLineEdit.setObjectName("skyboxLineEdit")
        self.skyboxesFolderLayout.addWidget(self.skyboxLineEdit, 1, 1)

        self.skyboxAddButton = QtWidgets.QPushButton(clicked = lambda: self.addFile(file=self.skyboxLineEdit))
        self.skyboxAddButton.setObjectName("skyboxAddButton")
        self.skyboxAddButton.setText("add skybox")
        self.skyboxesFolderLayout.addWidget(self.skyboxAddButton, 1, 2)

        self.iblLineEdit = QtWidgets.QLineEdit()
        self.iblLineEdit.setObjectName("iblLineEdit")
        self.skyboxesFolderLayout.addWidget(self.iblLineEdit, 2, 1)

        self.iblAddButton = QtWidgets.QPushButton(clicked = lambda: self.addFile(file=self.iblLineEdit))
        self.iblAddButton.setObjectName("iblAddButton")
        self.iblAddButton.setText("add ibl")
        self.skyboxesFolderLayout.addWidget(self.iblAddButton, 2, 2)

        self.skyboxesFolderWidget.setLayout(self.skyboxesFolderLayout)

        self.skyboxesLayout.addWidget(self.skyboxesFolderWidget)
        self.skyboxesWidget.setLayout(self.skyboxesLayout)

        self.skymapMainLayout.addWidget(self.skyboxesWidget)
        self.levelAndSkymap.setLayout(self.skymapMainLayout)

        self.bundleMenuTabWidget.addTab(self.levelAndSkymap, "")

        self.centralLayout.addWidget(self.bundleMenuTabWidget)
        self.centralLayout.addWidget(self.saveButtonWidget)
        self.centralwidget.setLayout(self.centralLayout)

        self.retranslateUi(bundleMenu)
        self.bundleMenuTabWidget.setCurrentIndex(0)

        bundleMenu.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(bundleMenu)

    def resizedRepaint(self, asset, text, grid, tab):
        if tab == 1:
            self.dynamicRepaint(asset, text, grid)

    def fillInventorySettings(self, asset):
        assetWidget = QtWidgets.QWidget()
        assetWidget.setObjectName(asset)

        assetLayout = QtWidgets.QVBoxLayout()
        assetLayout.setObjectName(asset + 'Layout')
        assetLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        assetScrollArea = QtWidgets.QScrollArea(assetWidget)
        assetScrollArea.setWidgetResizable(True)
        assetScrollArea.setObjectName(asset + "ScrollArea")

        assetScrollAreaWidgetContents = QtWidgets.QWidget()
        assetScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1, 1))
        assetScrollAreaWidgetContents.setObjectName(asset + "ScrollAreaWidgetContents")

        assetScrollArea.setWidget(assetScrollAreaWidgetContents)

        assetsGridLayout = QtWidgets.QGridLayout(assetScrollAreaWidgetContents)
        assetsGridLayout.setContentsMargins(5, 5, 5, 5)
        assetsGridLayout.setHorizontalSpacing(2)
        assetsGridLayout.setObjectName(asset + 'GridLayout')
        assetsGridLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        optionWidget = QtWidgets.QWidget()
        optionWidget.setObjectName(asset + 'OptionWidget')
        optionWidget.setMaximumHeight(50)

        optionLayout = QtWidgets.QHBoxLayout()
        optionLayout.setObjectName('optionLayout')
        optionLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        setNumToAllButton = QtWidgets.QPushButton()
        setNumToAllButton.setObjectName(asset + 'SetNumToAllButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(10)
        setNumToAllButton.setFont(font)
        setNumToAllButton.setMinimumSize(160, 35)
        setNumToAllButton.setText('SET QUANTITY')
        setNumToAllButton.clicked.connect(lambda: self.setNumToAll(assetWidget))

        searchLabel = QtWidgets.QLabel()
        searchLabel.setObjectName(asset + 'searchLabel')
        searchLabel.setText('Search here')
        searchLineEdit = QtWidgets.QLineEdit()
        searchLineEdit.setObjectName(asset + 'SearchLineEdit')
        searchLineEdit.setMaximumWidth(300)

        spacer = QtWidgets.QSpacerItem(50, 50, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)

        optionLayout.addWidget(searchLabel)
        optionLayout.addWidget(searchLineEdit)
        optionLayout.addItem(spacer)
        optionLayout.addWidget(setNumToAllButton)
        optionWidget.setLayout(optionLayout)

        assetLayout.addWidget(assetScrollArea)
        assetLayout.addWidget(optionWidget)
        assetWidget.setLayout(assetLayout)

        objectsListToPaint = []
        for eachObj in self.objectsDict[asset]:
            objectsListToPaint.append(eachObj)

        self.assetsPlacement(asset, assetsGridLayout, objectsListToPaint)

        searchLineEdit.textChanged.connect(lambda: self.dynamicRepaint(asset, searchLineEdit.text(), assetsGridLayout))
        self.bundleMenuWindow.resized.connect(lambda: self.resizedRepaint(asset, searchLineEdit.text(), assetsGridLayout,
                                                                          self.bundleMenuTabWidget.currentIndex()))

        self.inventoryTabWidget.addTab(assetWidget, "")
        self.inventoryTabWidget.setTabText(self.inventoryTabWidget.indexOf(assetWidget), asset)

    def editBackground(self):
        self.newBgLogo = ''
        self.fileDialog = QtWidgets.QFileDialog()
        self.newBgLogo = self.fileDialog.getOpenFileName(filter='PNG (*.png)')[0]
        print(self.newBgLogo)  # for test#
        self.newBgName = os.path.splitext(os.path.basename((os.path.join(self.newBgLogo))))[0]
        if self.newBgLogo == '':
            pass
        else:
            self.bgPixmap = QtGui.QPixmap(self.newBgLogo).scaled(192, 128)
            self.backgroundLabelPic.setPixmap(self.bgPixmap)
            self.bgEditedFlag = True

    def inventoryJsonFill(self):
        newInventoryJsonlist = []
        for objType in self.objectsDict:
            for obj in self.objectsDict[objType]:
                if obj['quantity'] != 0:
                    newObj = {}
                    newObj['name'] = objType + '::' +  obj['name']
                    newObj['quantity'] = obj['quantity']
                    newInventoryJsonlist.append(newObj)

        return newInventoryJsonlist

    def addFile(self, file):
        self.fileDialog = QtWidgets.QFileDialog()
        self.selectedFile = self.fileDialog.getOpenFileName(filter='HDR (*.hdr *.hdri)')[0]
        file.setText(self.selectedFile)

    def enableField(self, field):
        if QtWidgets.QApplication.instance().sender().isChecked():
            field.setEnabled(True)
        else:
            field.setEnabled(False)

    def editLogo(self):
        self.newLogo = ''
        self.fileDialog = QtWidgets.QFileDialog()
        self.newLogo = self.fileDialog.getOpenFileName(filter='PNG (*.png)')[0]
        self.newIconName = os.path.splitext(os.path.basename((os.path.join(self.newLogo))))[0]
        if self.newLogo == '':
            pass
        else:
            self.pixmap = QtGui.QPixmap(self.newLogo)
            self.labelLogoPic.setPixmap(self.pixmap)
            self.logoIsEditedFlag = True

    def confirm(self):
        print('basename - ' + os.path.basename(self.currentPath))
        print(self.folderNameLineEdit.text())
        if self.folderNameLineEdit.text() == os.path.basename(self.currentPath):
            errorMessage = 'Change folder name to unique (not ' + os.path.basename(self.currentPath) + ')'
            self.folderNameLineEdit.setStyleSheet('background-color: red;')
            self.infoWindow(message=errorMessage, type='warning')
        else:
            if os.path.isdir(os.path.join(Paths.bundles, self.folderNameLineEdit.text())):
                if self.folderNameLineEdit.text() != self.bundleName:
                    errorMessage = 'This name already exists'
                    self.folderNameLineEdit.setStyleSheet('background-color: red;')
                    self.infoWindow(message=errorMessage, type='warning')
                else:
                    self.updateBundle()
                    self.bundleMenuWindow.close()
            else:
                self.updateBundle()
                self.bundleMenuWindow.close()

    def descriptionListFill(self):
        self.descriptionStr = ''
        for each in range(8):
            if self.descriptionLineEditList[each].text() != '':
                try:
                    if self.descriptionLineEditList[each+1].text() != '':
                        self.descriptionList[each] = self.descriptionLineEditList[each].text() + '\n'
                    else:
                        self.descriptionList[each] = self.descriptionLineEditList[each].text()
                except IndexError:
                    self.descriptionList[each] = self.descriptionLineEditList[each].text()
            else:
                self.descriptionList[each] = self.descriptionLineEditList[each].text()
        self.descriptionStr = ''.join(self.descriptionList)
        return self.descriptionStr

    def updateBundle(self):
        if self.folderNameLineEdit.text() != self.bundleName:
            os.rename(os.path.join(Paths.bundles, self.bundleName),
                      os.path.join(Paths.bundles, self.folderNameLineEdit.text()))

        currentConfig = dict(name=self.levelNameLineEdit.text(), #icon=self.iconLineEdit.text(),
                             id=int(self.idLineEdit.text()), likes=int(self.likesLineEdit.text()),
                             description=self.descriptionListFill(),
                             minPlayers=int(self.minPlayersLineEdit.text()),
                             maxPlayers=int(self.maxPlayersLineEdit.text()))

        with open(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'config.json'), 'w') as self.jsonConfig:
            json.dump(currentConfig, self.jsonConfig, indent=2, separators=(',', ':'))

        if self.logoIsEditedFlag == True:
            shutil.copyfile(self.newLogo, os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', os.path.basename(self.newLogo)))
            try:
                os.rename(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', os.path.basename(self.newLogo)),
                          os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', 'icon.png'))
            except FileExistsError:
                os.remove(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', 'icon.png'))
                os.rename(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', os.path.basename(self.newLogo)),
                          os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', 'icon.png'))
            self.logoIsEditedFlag = False

        if self.bgEditedFlag == True:
            shutil.copyfile(self.newBgLogo, os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby',
                                                       os.path.basename(self.newBgLogo)))
            try:
                os.rename(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby',
                                       os.path.basename(self.newBgLogo)),
                          os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', 'background.png'))
            except FileExistsError:
                os.remove(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', 'background.png'))
                os.rename(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby',
                                       os.path.basename(self.newBgLogo)),
                          os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'lobby', 'background.png'))
            self.bgEditedFlag = False

        if self.editSpawnPointButton.isChecked():
            for avatar in self.jsonObjectsDict['Avatar']:
                avatar['x'] = float(self.xLineEdit.text())
                avatar['y'] = float(self.yLineEdit.text())
                avatar['z'] = float(self.zLineEdit.text())
            print(self.jsonObjectsDict)
            with open(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'world', 'spawn.json'), 'w') as self.jsonObjects:
                json.dump(self.jsonObjectsDict, self.jsonObjects, indent=2, separators=(',', ':'))

        if len(self.inventoryJsonFill()) == 0:
            if os.path.exists(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'game', 'inventory.json')):
                os.remove(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'game', 'inventory.json'))
        else:
            with open(os.path.join(Paths.bundles, self.folderNameLineEdit.text(), 'game', 'inventory.json'),
                      'w') as self.inventoryJson:
                json.dump(self.inventoryJsonFill(), self.inventoryJson, indent=2, separators=(',', ':'))

        if self.skymapEnable.isEnabled():
            self.convertSkymap()

        print('CHANGED')

    def convertSkymap(self):

        if self.skyboxLineEdit.text() != '':
            if os.path.exists(os.path.join(Paths.bundles, self.bundleName, 'world', 'skymap_skybox.ktx')):
                questionBox = QtWidgets.QMessageBox()
                questionBox.setWindowTitle('Delete')
                questionBox.setIcon(QtWidgets.QMessageBox.Question)
                questionBox.setText('Skybox already exists. Do you want to replace?')
                questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                button = questionBox.exec()

                if button == QtWidgets.QMessageBox.Yes:
                    os.remove(os.path.join(Paths.bundles, self.bundleName, 'world', 'skymap_skybox.ktx'))
                    subprocess.call('start /wait ' + Paths.tools + '\cmgen.exe -x "' + \
                                    os.path.join(Paths.bundles, self.bundleName, 'world') + \
                                    '" --format=ktx --size=256 "' + os.path.normpath(self.skyboxLineEdit.text()) + '"',
                                    shell=True, cwd=Paths.tools)
                    os.remove(os.path.join(Paths.bundles, self.bundleName, 'world', 'world_ibl.ktx'))
                    os.rename(os.path.join(Paths.bundles, self.bundleName, 'world', 'world_skybox.ktx'),
                              os.path.join(Paths.bundles, self.bundleName, 'world', 'skymap_skybox.ktx'))
                    self.infoWindow(message='Skybox adding - done!', type='info')
            else:
                subprocess.call('start /wait ' + Paths.tools + '\cmgen.exe -x "' + \
                                os.path.join(Paths.bundles, self.bundleName, 'world') + \
                                '" --format=ktx --size=256 "' + os.path.normpath(self.skyboxLineEdit.text()) + '"',
                                shell=True, cwd=Paths.tools)
                os.remove(
                    os.path.join(Paths.bundles, self.bundleName, 'world', 'world_ibl.ktx'))
                os.rename(
                    os.path.join(Paths.bundles, self.bundleName, 'world', 'world_skybox.ktx'),
                    os.path.join(Paths.bundles, self.bundleName, 'world', 'skymap_skybox.ktx'))
                self.infoWindow(message='Skybox adding - done!', type='info')

        if self.iblLineEdit.text() != '':
            if os.path.exists(os.path.join(Paths.bundles, self.bundleName, 'world', 'skymap_ibl.ktx')):
                questionBox = QtWidgets.QMessageBox()
                questionBox.setWindowTitle('Delete')
                questionBox.setIcon(QtWidgets.QMessageBox.Question)
                questionBox.setText('Ibl already exists. Do you want to replace?')
                questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                button = questionBox.exec()

                if button == QtWidgets.QMessageBox.Yes:
                    os.remove(os.path.join(Paths.bundles, self.bundleName, 'world', 'skymap_ibl.ktx'))
                    subprocess.call('start /wait ' + Paths.tools + '\cmgen.exe -x "' + \
                                    os.path.join(Paths.bundles, self.bundleName, 'world') + \
                                    '" --format=ktx --size=256 "' + os.path.normpath(self.iblLineEdit.text()) + '"',
                                    shell=True, cwd=Paths.tools)
                    os.remove(os.path.join(Paths.bundles, self.bundleName, 'world', 'world_skybox.ktx'))
                    os.rename(os.path.join(Paths.bundles, self.bundleName, 'world', 'world_ibl.ktx'),
                              os.path.join(Paths.bundles, self.bundleName, 'world', 'skymap_ibl.ktx'))
                    self.infoWindow(message='Ibl adding - done!', type='info')

            else:
                subprocess.call('start /wait ' + Paths.tools + '\cmgen.exe -x "' + \
                                os.path.join(Paths.bundles, self.bundleName, 'world') + \
                                '" --format=ktx --size=256 "' + os.path.normpath(self.iblLineEdit.text()) + '"',
                                shell=True, cwd=Paths.tools)
                os.remove(os.path.join(Paths.bundles, self.bundleName, 'world', 'world_skybox.ktx'))
                os.rename(os.path.join(Paths.bundles, self.bundleName, 'world', 'world_ibl.ktx'),
                          os.path.join(Paths.bundles, self.bundleName, 'world', 'skymap_ibl.ktx'))
                self.infoWindow(message='Ibl adding - done!', type='info')

    def assetsPlacement(self, asset, grid, listToPaint):
        x = 0
        y = 0
        for each in listToPaint:
            assetWidget = QtWidgets.QWidget()
            assetWidget.setFixedSize(160, 300)
            pal = QtGui.QPalette()
            pal.setColor(QtGui.QPalette.Background, QtGui.QColor('#D0D0D0'))
            assetWidget.setPalette(pal)
            assetWidget.setAutoFillBackground(True)
            assetVLayout = QtWidgets.QVBoxLayout()
            assetIcon = QtWidgets.QLabel()
            assetIcon.resize(128, 128)
            pixmap = QtGui.QPixmap(each['pathToIcon']).scaled(128, 128, QtCore.Qt.IgnoreAspectRatio)
            assetIcon.setPixmap(pixmap)
            assetName = QtWidgets.QLineEdit()
            assetName.setObjectName(asset + each['name'])
            assetName.setText(each['name'])
            assetName.setEnabled(False)
            assetNumberInInventory = QtWidgets.QLineEdit()
            assetNumberInInventory.setValidator(self.onlyInt)
            assetNumberInInventory.setObjectName(asset + 'Numbers' + each['name'])
            assetNumberInInventory.setText(str(each['quantity']))
            assetNumberInInventory.textChanged.connect(lambda str, name=each['name']: self.changeQuantity(asset, name, str))
            assetNumberInInventory.textChanged.connect(lambda str, lineEdit = assetNumberInInventory: self.isNotEmpty(lineEdit))
            setMaxItemsButton = QtWidgets.QPushButton(clicked=lambda: self.setMaxItems(sender=QtWidgets.QApplication.instance().sender()))
            setMaxItemsButton.setObjectName('setMaxItemsButton')
            font = QtGui.QFont()
            font.setFamily("Oswald Light")
            font.setPointSize(8)
            setMaxItemsButton.setFont(font)
            setMaxItemsButton.setText('ADD MAX')
            resetItemsButton = QtWidgets.QPushButton(clicked=lambda: self.resetItems(sender=QtWidgets.QApplication.instance().sender()))
            resetItemsButton.setObjectName('resetItemsButton')
            font = QtGui.QFont()
            font.setFamily("Oswald Light")
            font.setPointSize(8)
            resetItemsButton.setFont(font)
            resetItemsButton.setText('RESET')

            assetVLayout.addWidget(assetIcon)
            assetVLayout.addWidget(assetName)
            assetVLayout.addWidget(assetNumberInInventory)
            assetVLayout.addWidget(setMaxItemsButton)
            assetVLayout.addWidget(resetItemsButton)

            assetWidget.setLayout(assetVLayout)

            grid.addWidget(assetWidget, x, y, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

            y += 1
            if y > ((self.bundleMenuWindow.size().width()) // 150) - 2:
                x += 1
                y = 0

    def isNotEmpty(self, lineEdit):
        if lineEdit.text() == '':
            lineEdit.setText('0')

    def changeQuantity(self, asset, name, text):
        for eachObj in self.objectsDict[asset]:
            if eachObj['name'] == name:
                if text != '':
                    eachObj['quantity'] = int(text)
                else:
                    eachObj['quantity'] = 0

    def repaintField(self, asset, grid, dynamicObjList):
        for i in reversed(range(grid.count())):
            grid.itemAt(i).widget().setParent(None)
        self.assetsPlacement(asset, grid, dynamicObjList)

    def dynamicRepaint(self, asset, text, grid):
        dynamicObjList = []
        if text == '':
            for each in self.objectsDict[asset]:
                dynamicObjList.append(each)
            self.repaintField(asset, grid, dynamicObjList)
        else:
            for eachObject in self.objectsDict[asset]:
                if text in eachObject['name']:
                    dynamicObjList.append(eachObject)
            self.repaintField(asset, grid, dynamicObjList)

    def setNumToAll(self, assetWidget):
        tab = assetWidget
        grid = tab.findChild(QtWidgets.QGridLayout, (tab.objectName() + 'GridLayout'))

        num, ok = QtWidgets.QInputDialog.getInt(assetWidget, "integer input dualog", "enter a number")
        if ok:
            number = str(num)

            for index in range(grid.count()):
                gridItem = grid.itemAt(index).widget()
                quantity = gridItem.findChild(QtWidgets.QLineEdit, gridItem.layout().itemAt(2).widget().objectName())
                quantity.setText(number)

    def setMaxItems(self, sender):
        sender.parent().layout().itemAt(2).widget().setText('99')

    def resetItems(self, sender):
        sender.parent().layout().itemAt(2).widget().setText('0')

    def infoWindow(self, message, type):
        if type == 'info':
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setText("Info")
            messageBox.setInformativeText(message)
            messageBox.setWindowTitle("Info")
            messageBox.exec_()
        elif type == 'warning':
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setText("Error")
            messageBox.setInformativeText(message)
            messageBox.setWindowTitle("Warning")
            messageBox.exec_()

    def retranslateUi(self, bundleMenu):
        _translate = QtCore.QCoreApplication.translate
        bundleMenu.setWindowTitle(_translate("bundleMenu", "bundleMenu - " + self.bundleName))
        self.levelNameLabel.setText(_translate("bundleMenu", "level name"))
        self.folderNameLabel.setText(_translate("bundleMenu", "folder name"))
        self.idLabel.setText(_translate("bundleMenu", "id"))
        self.likesLabel.setText(_translate("bundleMenu", "likes"))
        self.minPlayersLabel.setText(_translate("bundleMenu", "minPlayers"))
        self.maxPlayersLabel.setText(_translate("bundleMenu", "maxPlayers"))
        self.bundleMenuTabWidget.setTabText(self.bundleMenuTabWidget.indexOf(self.config),
                                            _translate("bundleMenu", "config"))
        self.bundleMenuTabWidget.setTabText(self.bundleMenuTabWidget.indexOf(self.inventoryMainWidget),
                                            _translate("bundleMenu", "inventory"))
        self.bundleMenuTabWidget.setTabText(self.bundleMenuTabWidget.indexOf(self.levelAndSkymap),
                                            _translate("bundleMenu", "skymap"))

class Ui_AddLevelWindow(object):
    def __init__(self, win, prevWin):
        self.addLevelWindow = win
        self.prevWin = prevWin
        self.setupUi(win)
        self.addLevelWindow.show()

    def openWindow(self, bundleName, currentPath, prevWin):
        self.window = MainWindowCloseRmDir(prevWin, currentPath)
        Ui_bundleMenu(self.window, bundleName, currentPath)

    def setupUi(self, AddLevelWindow):
        AddLevelWindow.setObjectName("Add Level")
        AddLevelWindow.setFixedSize(400, 200)
        AddLevelWindow.setWindowTitle("Add Level")

        self.centralwidget = QtWidgets.QWidget(AddLevelWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setGeometry(0, 0, 400, 200)

        self.mainWidget = QtWidgets.QWidget(self.centralwidget)
        self.mainWidget.setObjectName('mainWidget')
        self.mainWidget.setGeometry(0, 20, 400, 100)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.mainWidget)
        self.horizontalLayout.setObjectName('horizontalLayout')

        self.levelLineEdit = QtWidgets.QLineEdit()
        self.levelLineEdit.setObjectName('levelLineEdit')
        self.horizontalLayout.addWidget(self.levelLineEdit)

        self.levelAddButton = QtWidgets.QPushButton(clicked = lambda: self.openFile())
        self.levelAddButton.setObjectName('levelAddButton')
        self.levelAddButton.setText('add level')
        self.horizontalLayout.addWidget(self.levelAddButton)

        self.createLevelButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.mcConverter(self.prevWin))
        self.createLevelButton.setObjectName('createLevelButton')
        self.createLevelButton.setGeometry(150, 120, 100, 50)
        self.createLevelButton.setText('create')
        self.createLevelButton.setEnabled(False)

        AddLevelWindow.setCentralWidget(self.centralwidget)

    def openFile(self):
        self.fileDialog = QtWidgets.QFileDialog()
        self.level = self.fileDialog.getExistingDirectory()
        self.levelLineEdit.setText(self.level)
        if self.levelLineEdit.text() != '':
            self.createLevelButton.setEnabled(True)
        print(self.level)

    def mcConverter(self, prevWin):
        folderToConvert = self.level
        mcLevel = os.path.basename(folderToConvert)
        levelPath = os.path.join(Paths.bundles, 'level1')

        print(folderToConvert)
        print(mcLevel)

        os.mkdir(levelPath)
        os.mkdir(os.path.join(levelPath, 'world'))
        subprocess.call('start /wait ' + Paths.tools + '\minecraft_converter ' + Paths.assets +
                        '\world\skin.dat "' + folderToConvert + '" ' + levelPath, shell=True, cwd=os.getcwd())

        subprocess.call('start /wait ' + Paths.tools + '\zip.exe ' + '-9 -m -j -r ' +
                        os.path.join(levelPath, 'world', 'level.zip') + ' ' + levelPath, shell=True, cwd=os.getcwd())

        for each in os.listdir(Paths.template):
            if os.path.isfile(os.path.join(Paths.template, each)):
                shutil.copyfile(os.path.join(Paths.template, each),
                                os.path.join(levelPath, each))
            elif os.path.isdir(os.path.join(Paths.template, each)):
                if each == 'world':
                    for i in os.listdir(os.path.join(Paths.template, 'world')):
                        if os.path.isfile(os.path.join(Paths.template, 'world', i)):
                            shutil.copyfile(os.path.join(Paths.template, 'world', i),
                                            os.path.join(levelPath, 'world', i))
                        else:
                            shutil.copytree(os.path.join(Paths.template, 'world', i),
                                            os.path.join(levelPath, 'world', i))
                else:
                    shutil.copytree(os.path.join(Paths.template, each),
                                    os.path.join(levelPath, each))

        with open(os.path.join(levelPath, 'config.json'), 'r') as config:
            currConfig = json.load(config)
        currConfig['name'] = mcLevel

        with open(os.path.join(levelPath, 'config.json'), 'w') as config:
            json.dump(currConfig, config, indent=2, separators=(',', ':'))

        self.openWindow(bundleName=os.path.basename(levelPath), currentPath=levelPath, prevWin=prevWin)
        self.addLevelWindow.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    bundleSetup = QtWidgets.QMainWindow()
    Paths.getDir('Release')
    Ui_bundleSetup(bundleSetup)
    bundleSetup.show()
    sys.exit(app.exec_())