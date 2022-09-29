from PyQt5 import QtCore, QtWidgets, QtGui
import os
import shutil
import json
from managerPaths import Paths
from staticMethods import StaticMethods

class Ui_SvnWorkspaceSync(object):
    def __init__(self, win, app):
        self.app = app
        self.svnWorkspaceSyncWin = win
        self.pathsToSync = []
        self.checkboxObjList = []
        self.setupUi()
        self.svnWorkspaceSyncWin.show()

    def setupUi(self):
        self.svnWorkspaceSyncWin.resize(350, 350)
        self.svnWorkspaceSyncWin.setMaximumSize(500, 500)
        self.svnWorkspaceSyncWin.setObjectName('svnWorkspaceSyncWin')
        self.svnWorkspaceSyncWin.setWindowTitle('SVN Workspace Sync')

        self.centralWidget = QtWidgets.QWidget(self.svnWorkspaceSyncWin)
        self.centralWidget.setObjectName('centralWidget')

        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.selectionWidget = QtWidgets.QWidget(self.centralWidget)
        self.selectionWidget.setObjectName('selectionWidget')

        self.selectionLayout = QtWidgets.QHBoxLayout()
        self.selectionLayout.setObjectName('selectionLayout')
        self.selectionLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.selectionButtonsWidget = QtWidgets.QWidget(self.selectionWidget)
        self.selectionButtonsWidget.setObjectName('selectionButtonsWidget')

        self.selectionButtonsLayout = QtWidgets.QVBoxLayout()
        self.selectionButtonsLayout.setObjectName('selectionButtonsLayout')
        self.selectionButtonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.itemsListWidget = QtWidgets.QListWidget(self.centralWidget)
        self.itemsListWidget.setObjectName('fbxListWidget')
        self.itemsListWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.itemsListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.addModelsButton = QtWidgets.QPushButton(self.centralWidget)
        self.addModelsButton.setObjectName('addModelsButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.addModelsButton.setFont(font)
        self.addModelsButton.setText('Add files')
        self.addModelsButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.addModelsButton.clicked.connect(lambda: self.addModels())

        self.addDirButton = QtWidgets.QPushButton(self.centralWidget)
        self.addDirButton.setObjectName('addDirButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.addDirButton.setFont(font)
        self.addDirButton.setText('Add directories')
        self.addDirButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.addDirButton.clicked.connect(lambda: self.addDirs())

        self.deleteButton = QtWidgets.QPushButton(self.centralWidget)
        self.deleteButton.setObjectName('deleteButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.deleteButton.setFont(font)
        self.deleteButton.setText('Delete')
        self.deleteButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.deleteButton.clicked.connect(lambda: self.deleteModelFromList(self.itemsListWidget.selectedItems()))

        self.clearButton = QtWidgets.QPushButton(self.centralWidget)
        self.clearButton.setObjectName('clearButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.clearButton.setFont(font)
        self.clearButton.setText('Clear')
        self.clearButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.clearButton.clicked.connect(lambda: self.clearList())

        self.selectionButtonsLayout.addWidget(self.addModelsButton)
        self.selectionButtonsLayout.addWidget(self.addDirButton)
        self.selectionButtonsLayout.addWidget(self.deleteButton)
        self.selectionButtonsLayout.addWidget(self.clearButton)

        self.selectionButtonsWidget.setLayout(self.selectionButtonsLayout)

        self.selectionLayout.addWidget(self.itemsListWidget)
        self.selectionLayout.addWidget(self.selectionButtonsWidget)

        self.selectionWidget.setLayout(self.selectionLayout)

        self.checkBoxesAreaWidget = QtWidgets.QWidget(self.centralWidget)
        self.checkBoxesAreaWidget.setObjectName('checkBoxesAreaWidget')

        self.checkBoxesAreaLayout = QtWidgets.QVBoxLayout()
        self.checkBoxesAreaLayout.setObjectName('checkBoxesAreaLayout')
        self.checkBoxesAreaLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.checkBoxWidget = QtWidgets.QWidget(self.centralWidget)
        self.checkBoxWidget.setObjectName('checkBoxWidget')

        self.checkBoxWidgetLayout = QtWidgets.QGridLayout()
        self.checkBoxWidgetLayout.setObjectName('checkBoxWidgetLayout')
        self.checkBoxWidgetLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        x = 0
        y = 0
        for each in self.fillCheckboxArea():
            checkbox = QtWidgets.QCheckBox()
            checkbox.setObjectName(each)
            font = QtGui.QFont()
            font.setFamily("Oswald Light")
            font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
            checkbox.setFont(font)
            checkbox.setText(each)
            checkbox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
            checkbox.clicked.connect(lambda bool, name=each, currCheckbox=checkbox: self.check(name, currCheckbox.isChecked()))
            obj = {}
            obj['name'] = each
            obj['state'] = False
            if each == 'Release':
                obj['path'] = each
            else:
                obj['path'] = os.path.join('Art_workspace', each)
            self.checkboxObjList.append(obj)
            self.checkBoxWidgetLayout.addWidget(checkbox, x, y, 1, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
            y += 1
            if y > 4:
                x += 1
                y = 0

        self.checkBoxWidget.setLayout(self.checkBoxWidgetLayout)

        self.selectAllButton = QtWidgets.QPushButton(self.centralWidget)
        self.selectAllButton.setObjectName('selectAllButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.selectAllButton.setFont(font)
        self.selectAllButton.setText('Select all')
        self.selectAllButton.setMinimumWidth(100)
        self.selectAllButton.setMaximumWidth(120)
        self.selectAllButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.selectAllButton.clicked.connect(lambda: self.selectAll())

        self.checkBoxesAreaLayout.addWidget(self.checkBoxWidget)
        self.checkBoxesAreaLayout.addWidget(self.selectAllButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.checkBoxesAreaWidget.setLayout(self.checkBoxesAreaLayout)

        self.syncButtonsWidget = QtWidgets.QWidget(self.centralWidget)
        self.syncButtonsWidget.setObjectName('syncButtonsWidget')

        self.syncButtonsLayout = QtWidgets.QHBoxLayout()
        self.syncButtonsLayout.setObjectName('syncButtonsLayout')
        self.syncButtonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.syncButtonsLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.copyButton = QtWidgets.QPushButton(self.syncButtonsWidget)
        self.copyButton.setObjectName('copyButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.copyButton.setFont(font)
        self.copyButton.setText('COPY')
        self.copyButton.setMinimumSize(100, 35)
        self.copyButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.copyButton.clicked.connect(lambda: self.copyFiles())

        self.deleteSyncButton = QtWidgets.QPushButton(self.syncButtonsWidget)
        self.deleteSyncButton.setObjectName('deleteSyncButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.deleteSyncButton.setFont(font)
        self.deleteSyncButton.setText('DELETE SYNC')
        self.deleteSyncButton.setMinimumSize(100, 35)
        self.deleteSyncButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.deleteSyncButton.clicked.connect(lambda: self.deleteSync())

        spacerH1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                        QtWidgets.QSizePolicy.Policy.Fixed)
        spacerH2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding,
                                         QtWidgets.QSizePolicy.Policy.Fixed)

        self.syncButtonsLayout.addItem(spacerH1)
        self.syncButtonsLayout.addWidget(self.copyButton)
        self.syncButtonsLayout.addWidget(self.deleteSyncButton)
        self.syncButtonsLayout.addItem(spacerH2)

        self.syncButtonsWidget.setLayout(self.syncButtonsLayout)

        self.centralLayout.addWidget(self.selectionWidget)
        self.centralLayout.addWidget(self.checkBoxesAreaWidget)
        self.centralLayout.addWidget(self.syncButtonsWidget)

        self.centralWidget.setLayout(self.centralLayout)

        self.svnWorkspaceSyncWin.setCentralWidget(self.centralWidget)

    def deleteSync(self):
        if not self.pathsToSync:
            return
        for each in self.pathsToSync:
            for i in self.checkboxObjList:
                pathToCMInventory = os.path.join(os.getcwd(), i['path'], 'assets', 'CreationModeInventory.json')
                cmState = StaticMethods.getCreationModeInventoryState(pathToCMInventory)
                if i['state'] == True:
                    if os.path.isdir(each):
                        begin = os.getcwd()
                        end = 'assets' + each.rsplit('assets')[1]
                        path = os.path.join(begin, i['path'], end)
                        if os.path.normpath(each) != os.path.normpath(path):
                            try:
                                shutil.rmtree(path)
                            except FileNotFoundError:
                                pass
                    else:
                        fileExtention = os.path.splitext(each)[1]
                        if fileExtention == '.exe':
                            begin = os.getcwd()
                            path = os.path.join(begin, i['path'], os.path.basename(each))
                        else:
                            begin = os.getcwd()
                            end = 'assets' + each.rsplit('assets')[1]
                            path = os.path.join(begin, i['path'], end)

                        if os.path.normpath(each) != os.path.normpath(path):
                            try:
                                os.remove(path)
                            except FileNotFoundError:
                                pass

                        name = os.path.basename(each).rsplit('.')[0].lower()
                        assetType = os.path.split(os.path.dirname(each))[1]
                        pathToTextureDest = os.path.normpath(
                            os.path.join(os.getcwd(), i['path'], 'assets', 'textures', 'objects', name))
                        pathToIconDest = os.path.normpath(
                            os.path.join(os.getcwd(), i['path'], 'assets', 'icons', assetType, name + '.png'))
                        pathToBundles = os.path.normpath(
                            os.path.join(os.getcwd(), i['path'], 'assets', 'bundles'))

                        if assetType == 'objects':
                            StaticMethods.deleteObjectFromCreationModeInventory(cmState, [name], assetType)
                            if self.isExistInObjDb(name, assetType, i['path'], 'ObjectsPrototypes.json'):
                                self.deleteAssetFromDb(assetType, name, i['path'], 'ObjectsPrototypes.json')

                        ############ проверка и удаление из инвентаря бандлов #################
                            self.cleanBundleInventory(name, assetType, pathToBundles)
                        #######################################################################

                            try:
                                shutil.rmtree(pathToTextureDest)
                            except FileNotFoundError:
                                pass
                            try:
                                os.remove(pathToIconDest)
                            except FileNotFoundError:
                                pass

                        elif assetType == 'particles':
                            StaticMethods.deleteObjectFromCreationModeInventory(cmState, [name], assetType)
                            if self.isExistInObjDb(name, assetType, i['path'], 'ObjectsPrototypes.json'):
                                self.deleteAssetFromDb(assetType, name, i['path'], 'ObjectsPrototypes.json')

                            ############ проверка и удаление из инвентаря бандлов #################
                            self.cleanBundleInventory(name, assetType, pathToBundles)
                            #######################################################################

                            try:
                                os.remove(pathToIconDest)
                            except FileNotFoundError:
                                pass

                        elif assetType == 'blocks':
                            StaticMethods.deleteObjectFromCreationModeInventory(cmState, [name], assetType)
                            if self.isExistInObjDb(name, assetType, i['path'], 'CubePrototypes.json'):
                                self.deleteAssetFromDb(assetType, name, i['path'], 'CubePrototypes.json')

                            ############ проверка и удаление из инвентаря бандлов #################
                            self.cleanBundleInventory(name, assetType, pathToBundles)
                            #######################################################################

                StaticMethods.updateCreationModeInventoryFile(cmState, pathToCMInventory)

            for each in self.pathsToSync:
                normPath = os.path.normpath(each)
                cwd = os.getcwd()
                cutCwd = normPath.rsplit(cwd)[1]
                splitChar = '\\'
                dirArray = cutCwd.split(splitChar)
                print(dirArray)
                wd = None
                if dirArray[1] == 'Release':
                    wd = dirArray[1]
                elif dirArray[1] == 'Art_workspace':
                    wd = dirArray[2]
                for i in self.checkboxObjList:
                    if i['name'] == wd:
                        if i['state'] == True:
                            if os.path.isdir(each):
                                try:
                                    shutil.rmtree(each)
                                except FileNotFoundError:
                                    pass
                            else:
                                try:
                                    os.remove(each)
                                except FileNotFoundError:
                                    pass

        self.pathsToSync.clear()
        self.checkboxObjList.clear()

        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setText("Info")
        messageBox.setInformativeText('Done!')
        messageBox.setWindowTitle("Info")
        messageBox.exec_()

        self.setupUi()
        self.svnWorkspaceSyncWin.update()

    def cleanBundleInventory(self, name, assetType, pathToBundles):
        for eachBundle in os.listdir(pathToBundles):
            pathToInventoryJson = os.path.join(pathToBundles, eachBundle, 'game', 'inventory.json')

            with open(pathToInventoryJson, 'r', encoding='utf8') as inventoryJson:
                inventoryJsonDict = json.load(inventoryJson)

            newInventoryJsonList = []
            for eachObj in inventoryJsonDict:
                nameInJson = str(eachObj['name'])
                nameLower = nameInJson.lower()
                if nameLower.rsplit('::')[0] == assetType:
                    nameClean = nameLower.rsplit(assetType + '::')[1]
                    if nameClean != name:
                        newInventoryJsonList.append(eachObj)
                else:
                    newInventoryJsonList.append(eachObj)

            with open(pathToInventoryJson, 'w', encoding='utf8') as inventoryJson:
                json.dump(newInventoryJsonList, inventoryJson, indent=2, separators=(',', ':'))

    def deleteAssetFromDb(self, assetType, name, path, prototype):
        pathToDB = os.path.join(os.getcwd(), path, 'assets', prototype)

        with open(pathToDB, 'r', encoding='utf8') as objectsDb:
            objectsDbDict = json.load(objectsDb)
        assetList = []
        for each in objectsDbDict[assetType]:
            if name != each['name']:
                assetList.append(each)

        objectsDbDict[assetType] = assetList

        with open(pathToDB, 'w', encoding='utf8') as objectsDb:
            json.dump(objectsDbDict, objectsDb, indent=3, ensure_ascii=False, separators=(',', ':'))

    def addDirs(self):
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        fileDialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)

        fileView = fileDialog.findChild(QtWidgets.QListView, 'listView')
        if fileView:
            fileView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        fTreeView = fileDialog.findChild(QtWidgets.QTreeView)
        if fTreeView:
            fTreeView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        paths = []
        if fileDialog.exec():
            paths = fileDialog.selectedFiles()


        if len(paths) != 0:
            i = 0
            while i < len(paths):
                if os.path.basename(paths[i]) == os.path.split(os.path.dirname(paths[len(paths)-1]))[1]:
                    paths.pop(i)
                else:
                    i += 1

            for each in paths:
                self.itemsListWidget.addItem(os.path.basename(each))
                self.pathsToSync.append(each)

            self.addModelsButton.setEnabled(False)



        print(self.pathsToSync)

    def selectAll(self):
        for i in range(len(self.checkboxObjList)):
            self.checkBoxWidgetLayout.itemAt(i).widget().setChecked(True)
        for i in self.checkboxObjList:
            i['state'] = True

    def copyFiles(self):
        print(self.pathsToSync)
        print(self.checkboxObjList)
        if not self.pathsToSync:
            return
        for each in self.pathsToSync:
            for i in self.checkboxObjList:
                pathToCMInventory = os.path.join(os.getcwd(), i['path'], 'assets', 'CreationModeInventory.json')
                cmState = StaticMethods.getCreationModeInventoryState(pathToCMInventory)
                if i['state'] == True:
                    if os.path.isdir(each):
                        begin = os.getcwd()
                        end = 'assets' + each.rsplit('assets')[1]
                        path = os.path.join(begin, i['path'], end)
                        if os.path.normpath(each) != os.path.normpath(path):
                            try:
                                shutil.copytree(each, path)
                            except FileExistsError:
                                shutil.rmtree(path)
                                shutil.copytree(each, path)
                        else:
                            pass
                    else:
                        fileExtention = os.path.splitext(each)[1]
                        if fileExtention == '.exe':
                            begin = os.getcwd()
                            path = os.path.join(begin, i['path'], os.path.basename(each))
                        else:
                            begin = os.getcwd()
                            end = 'assets' + each.rsplit('assets')[1]
                            path = os.path.join(begin, i['path'], end)

                        try:
                            shutil.copyfile(each, path)
                        except FileExistsError:
                            os.remove(path)
                            shutil.copyfile(each, path)
                        except shutil.SameFileError:
                            pass

                        name = os.path.basename(each).rsplit('.')[0].lower()
                        assetType = os.path.split(os.path.dirname(each))[1]
                        pathToTextureSender = os.path.normpath(
                            os.path.join(each.rsplit('assets')[0], 'assets', 'textures', 'objects', name))
                        pathToTextureDest = os.path.normpath(
                            os.path.join(os.getcwd(), i['path'], 'assets', 'textures', 'objects', name))
                        pathToIconSender = os.path.normpath(
                            os.path.join(each.rsplit('assets')[0], 'assets', 'icons', assetType, name + '.png'))
                        pathToIconDest = os.path.normpath(
                            os.path.join(os.getcwd(), i['path'], 'assets', 'icons', assetType, name + '.png'))

                        if assetType == 'objects':
                            StaticMethods.addObjectInCreationModeInventory(cmState, name, assetType)

                            if not self.isExistInObjDb(name, assetType, i['path'], 'ObjectsPrototypes.json'):
                                self.addAssetInDb(assetType, self.createNewObjForDb(name), i['path'], 'ObjectsPrototypes.json')

                            if os.path.normpath(pathToTextureSender) != os.path.normpath(pathToTextureDest):
                                try:
                                    shutil.copytree(pathToTextureSender, pathToTextureDest)
                                except FileExistsError:
                                    shutil.rmtree(pathToTextureDest)
                                    shutil.copytree(pathToTextureSender, pathToTextureDest)
                                except FileNotFoundError:
                                    pass
                            else:
                                pass

                            try:
                                shutil.copyfile(pathToIconSender, pathToIconDest)
                            except shutil.SameFileError:
                                pass
                            except FileExistsError:
                                os.remove(pathToIconDest)
                                shutil.copyfile(pathToIconSender, pathToIconDest)
                            except FileNotFoundError:
                                pass

                        elif assetType == 'particles':
                            StaticMethods.addObjectInCreationModeInventory(cmState, name, assetType)

                            if not self.isExistInObjDb(name, assetType, i['path'], 'ObjectsPrototypes.json'):
                                self.addAssetInDb(assetType, self.createNewParticleForDb(name), i['path'], 'ObjectsPrototypes.json')

                            try:
                                shutil.copyfile(pathToIconSender, pathToIconDest)
                            except shutil.SameFileError:
                                pass
                            except FileExistsError:
                                os.remove(pathToIconDest)
                                shutil.copyfile(pathToIconSender, pathToIconDest)
                            except FileNotFoundError:
                                pass

                        elif assetType == 'blocks':
                            StaticMethods.addObjectInCreationModeInventory(cmState, name, assetType)

                            if not self.isExistInObjDb(name, assetType, i['path'], 'CubePrototypes.json'):
                                self.addAssetInDb(assetType, self.createNewBlockForDb(name), i['path'], 'CubePrototypes.json')

                StaticMethods.updateCreationModeInventoryFile(cmState, pathToCMInventory)

        self.pathsToSync.clear()
        self.checkboxObjList.clear()

        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setText("Info")
        messageBox.setInformativeText('Done!')
        messageBox.setWindowTitle("Info")
        messageBox.exec_()

        self.setupUi()
        self.svnWorkspaceSyncWin.update()

    def createNewObjForDb(self, name):
        obj = {}
        params = {}
        asset = {}
        animation = {}

        animation['animation'] = 'Idle'
        animation['loop'] = 1
        animation['speed'] = 1.0

        asset['animation'] = animation
        asset['model'] = 'objects::' + name.lower()
        asset['tintColorId'] = 2

        params['class'] = 'InteractiveObject'
        params['asset'] = asset

        obj['name'] = name.lower()
        obj['description'] = name.lower().capitalize()
        obj['placement'] = 'limited'
        obj['type'] = 'object'
        obj['params'] = params

        return obj

    def isExistInObjDb(self, name, assetType, path, prototype):
        pathToDB = os.path.join(os.getcwd(), path, 'assets', prototype)

        with open(pathToDB, 'r', encoding='utf8') as objectsDb:
            objectsDbDict = json.load(objectsDb)

        for eachObj in objectsDbDict[assetType]:
            if eachObj['name'] == name:
                return True
        return False

    def createNewParticleForDb(self, name):
        particle = {}
        particle['particleId'] = name.lower()
        particle['mode'] = 2

        params = {}
        params['class'] = 'InteractiveObject'
        params['particle'] = particle

        obj = {}
        obj['name'] = name.lower()
        obj['description'] = name.lower().capitalize()
        obj['placement'] = 'limited'
        obj['type'] = 'object'
        obj['params'] = params

        return obj

    def createNewBlockForDb(self, name):
        obj = {}
        params = {}
        params['blockId'] = name.lower()
        obj['name'] = name.lower()
        obj['description'] = 'block: ' + name.lower()
        obj['type'] = 'block'
        obj['params'] = params

        return obj

    def addAssetInDb(self, assetType, obj, path, prototype):
        pathToDB = os.path.join(os.getcwd(), path, 'assets', prototype)

        with open(pathToDB, 'r', encoding='utf8') as objectsDb:
            objectsDbDict = json.load(objectsDb)
        assetList = []
        for each in objectsDbDict[assetType]:
            assetList.append(each)

        assetList.append(obj)

        objectsDbDict[assetType] = assetList

        with open(pathToDB, 'w', encoding='utf8') as objectsDb:
            json.dump(objectsDbDict, objectsDb, indent=3, ensure_ascii=False, separators=(',', ':'))

    def check(self, name, state):
        for each in self.checkboxObjList:
            if each['name'] == name:
                each['state'] = state

    def fillCheckboxArea(self):
        checkboxList = []
        checkboxList.append('Release')
        for eachDir in os.listdir(Paths.artWorkspace):
            checkboxList.append(eachDir)
        return checkboxList

    def addModels(self):
        fileDialog = QtWidgets.QFileDialog()
        currentFiles = fileDialog.getOpenFileNames()[0]
        for each in currentFiles:
            self.pathsToSync.append(each)
        if len(currentFiles) != 0:
            for eachModel in currentFiles:
                name = os.path.basename(eachModel)
                self.itemsListWidget.addItem(name)
            self.addDirButton.setEnabled(False)

    def deleteModelFromList(self, items):
        if not items:
            return
        for eachItem in items:
            self.itemsListWidget.takeItem(self.itemsListWidget.row(eachItem))
            i = 0
            while i < len(self.pathsToSync):
                if eachItem.text() == os.path.basename(self.pathsToSync[i]):
                    self.pathsToSync.pop(i)
                else:
                    i += 1
        if self.itemsListWidget.count() == 0:
            self.addModelsButton.setEnabled(True)
            self.addDirButton.setEnabled(True)

    def clearList(self):
        self.itemsListWidget.clear()
        self.pathsToSync.clear()
        self.addDirButton.setEnabled(True)
        self.addModelsButton.setEnabled(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    Ui_SvnWorkspaceSync(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())