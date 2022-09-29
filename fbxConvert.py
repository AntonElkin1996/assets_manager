from PyQt5 import QtGui, QtWidgets, QtCore
import os
import subprocess
import shutil
import json
from managerPaths import Paths
from staticMethods import StaticMethods

class Ui_FbxConverter(object):
    def __init__(self, win, app):
        self.app = app
        self.win = win
        self.setupUi(win)
        self.files = []
        self.currentName = str
        with open(Paths.objectsDb, 'r') as objectsDb:
            self.objectsDbDict = json.load(objectsDb)
        self.objectsDbList = []
        for eachObj in self.objectsDbDict['objects']:
            self.objectsDbList.append(eachObj)
        win.show()

    def setupUi(self, fbxConverter):
        fbxConverter.resize(350, 300)
        fbxConverter.setObjectName('fbxConverterWindow')
        fbxConverter.setWindowTitle('fbx_converter')

        self.centralwidget = QtWidgets.QWidget(fbxConverter)
        self.centralwidget.setObjectName('centralwidget')

        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.centralLayout.setContentsMargins(20, 20, 20, 20)

        self.selectWidget = QtWidgets.QWidget(self.centralwidget)
        self.selectWidget.setObjectName('selectWidget')

        self.selectLayout = QtWidgets.QHBoxLayout()
        self.selectLayout.setObjectName('selectLayout')
        self.selectLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.buttonWidget = QtWidgets.QWidget(self.selectWidget)
        self.buttonWidget.setObjectName('buttonWidget')

        self.buttonsLayout = QtWidgets.QVBoxLayout()
        self.buttonsLayout.setObjectName('buttonsLayout')
        self.buttonsLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.fbxListWidget = QtWidgets.QListWidget(self.selectWidget)
        self.fbxListWidget.setObjectName('fbxListWidget')
        self.fbxListWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.fbxListWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.addModelsButton = QtWidgets.QPushButton(self.centralwidget)
        self.addModelsButton.setObjectName('addModelsButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.addModelsButton.setFont(font)
        self.addModelsButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.addModelsButton.setText('Add Models')
        self.addModelsButton.setMinimumHeight(35)
        self.addModelsButton.clicked.connect(lambda: self.addModels())

        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setObjectName('deleteButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.deleteButton.setFont(font)
        self.deleteButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.deleteButton.setText('Delete')
        self.deleteButton.setMinimumHeight(35)
        self.deleteButton.clicked.connect(lambda: self.deleteModelFromList(self.fbxListWidget.selectedItems()))

        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setObjectName('clearButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.clearButton.setFont(font)
        self.clearButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.clearButton.setText('Clear')
        self.clearButton.setMinimumHeight(35)
        self.clearButton.clicked.connect(lambda: self.clearList())

        self.buttonsLayout.addWidget(self.addModelsButton, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.buttonsLayout.addWidget(self.deleteButton, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.buttonsLayout.addWidget(self.clearButton, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.buttonWidget.setLayout(self.buttonsLayout)

        self.selectLayout.addWidget(self.fbxListWidget, 6)
        self.selectLayout.addWidget(self.buttonWidget, 4)

        self.selectWidget.setLayout(self.selectLayout)

        ######################################################################################

        modelTypes = ['avatar', 'objects', 'creatures']

        self.checkboxesWidget = QtWidgets.QWidget(self.centralwidget)
        self.checkboxesWidget.setObjectName('checkboxesWidget')

        self.checkboxesLayout = QtWidgets.QHBoxLayout()
        self.checkboxesLayout.setObjectName('checkboxesLayout')
        self.checkboxesLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.objDbCheckbox = QtWidgets.QCheckBox(self.checkboxesWidget)
        self.objDbCheckbox.setObjectName('objDbCheckbox')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.objDbCheckbox.setFont(font)
        self.objDbCheckbox.setText('Add to objects prototype')
        self.objDbCheckbox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.objDbCheckbox.setEnabled(False)

        self.objCmCheckbox = QtWidgets.QCheckBox(self.checkboxesWidget)
        self.objCmCheckbox.setObjectName('objCmCheckbox')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.objCmCheckbox.setFont(font)
        self.objCmCheckbox.setText('Add to creation mode')
        self.objCmCheckbox.setEnabled(False)
        self.objCmCheckbox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.checkboxesLayout.addWidget(self.objDbCheckbox)
        self.checkboxesLayout.addWidget(self.objCmCheckbox)

        self.checkboxesWidget.setLayout(self.checkboxesLayout)

        self.modelTypeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.modelTypeComboBox.setObjectName('modelTypeComboBox')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.modelTypeComboBox.setFont(font)
        self.modelTypeComboBox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.modelTypeComboBox.addItems(modelTypes)
        self.modelTypeComboBox.currentTextChanged.connect(lambda: self.activateCheckboxes())

        self.convertButton = QtWidgets.QPushButton(self.centralwidget)
        self.convertButton.setObjectName('convertButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.convertButton.setFont(font)
        self.convertButton.setText('Convert')
        self.convertButton.setMinimumSize(100, 50)
        self.convertButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.convertButton.setEnabled(True)
        self.convertButton.clicked.connect(lambda: self.convert())

        self.centralLayout.addWidget(self.selectWidget)
        self.centralLayout.addWidget(self.checkboxesWidget, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.centralLayout.addWidget(self.modelTypeComboBox)
        self.centralLayout.addWidget(self.convertButton, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.centralwidget.setLayout(self.centralLayout)

        fbxConverter.setCentralWidget(self.centralwidget)


    def activateCheckboxes(self):
        if self.modelTypeComboBox.currentText() == 'objects':
            self.objDbCheckbox.setEnabled(True)
            self.objCmCheckbox.setEnabled(True)
        else:
            self.objDbCheckbox.setEnabled(False)
            self.objCmCheckbox.setEnabled(False)


    def clearList(self):
        self.fbxListWidget.clear()
        self.files.clear()
        self.convertButton.setEnabled(False)

    def createNewObjForDb(self, name):
        obj = {}
        params = {}
        asset = {}
        animation = {}

        animation['animation'] = 'Idle'
        animation['loop'] = 1
        animation['speed'] = 1.0

        asset['animation'] = animation
        asset['model'] = 'objects::' + name
        asset['tintColorId'] = 2

        params['class'] = 'InteractiveObject'
        params['asset'] = asset

        obj['name'] = name
        obj['description'] = name.capitalize()
        obj['placement'] = 'limited'
        obj['type'] = 'object'
        obj['params'] = params

        return obj

    def isExistInObjDb(self, name):
        with open(Paths.objectsDb, 'r') as objectsDb:
            objectsDbDict = json.load(objectsDb)

        for eachObj in objectsDbDict['objects']:
            if eachObj['name'] == name:
                return True
        return False

    def deleteModelFromList(self, items):
        if not items:
            return
        for eachItem in items:
            self.fbxListWidget.takeItem(self.fbxListWidget.row(eachItem))
            i = 0
            while i < len(self.files):
                if eachItem.text() == os.path.basename(self.files[i]):
                    self.files.pop(i)
                else:
                    i += 1
        print(self.files)
        if self.fbxListWidget.count() == 0:
            self.convertButton.setEnabled(False)

    def addModels(self):
        fileDialog = QtWidgets.QFileDialog()
        currentFiles = fileDialog.getOpenFileNames(filter='FBX (*.fbx)')[0]
        for each in currentFiles:
            self.files.append(each)
        if len(currentFiles) != 0:
            for eachModel in currentFiles:
                name = os.path.basename(eachModel)
                self.fbxListWidget.addItem(name)
            self.convertButton.setEnabled(True)
        print(self.files)

    def callExistsQuestionBox(self, name):
        questionBox = QtWidgets.QMessageBox()
        questionBox.setWindowTitle('Exists')
        questionBox.setIcon(QtWidgets.QMessageBox.Question)
        questionBox.setText('Models ' + name + ' already exists. Do you want to replace?')
        questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        return questionBox

    def convert(self):
        cmState = StaticMethods.getCreationModeInventoryState(Paths.creationModeInventory)
        try:
            os.mkdir(os.path.join(os.getcwd(), 'Temp'))
        except FileExistsError:
            pass
        
        if self.modelTypeComboBox.currentText() == 'avatar':
            for eachModel in self.files:
                name = os.path.basename(eachModel).rsplit('.')[0].lower()
                if os.path.exists(os.path.join(Paths.assets, 'actors', name + '.glb')):
                    button = self.callExistsQuestionBox(name).exec()
                    if button == QtWidgets.QMessageBox.Yes:
                        os.remove(os.path.join(Paths.assets, 'actors', name + '.glb'))
                        subprocess.call(
                            'start /wait ' + Paths.tools + r'\fbx2gltf.exe --binary --verbose --fbx-temp-dir .\Temp -i "' +
                            os.path.normpath(eachModel) + '" -o ' + os.path.normpath(os.path.join(Paths.assets, 'actors', name + '.glb')),
                            shell=True, cwd=os.getcwd())
                    else:
                        pass
                else:
                    subprocess.call(
                        'start /wait ' + Paths.tools + r'\fbx2gltf.exe --binary --verbose --fbx-temp-dir .\Temp -i "' +
                        os.path.normpath(eachModel) + '" -o ' + os.path.normpath(os.path.join(Paths.assets, 'actors', name + '.glb')),
                        shell=True, cwd=os.getcwd())
        else:
            for eachModel in self.files:
                name = os.path.basename(eachModel).rsplit('.')[0].lower()
                if os.path.exists(os.path.join(Paths.assets, 'actors', self.modelTypeComboBox.currentText(), name + '.glb')):
                    button = self.callExistsQuestionBox(name).exec()
                    if button == QtWidgets.QMessageBox.Yes:
                        os.remove(os.path.join(Paths.assets, 'actors', self.modelTypeComboBox.currentText(), name + '.glb'))
                        subprocess.call(
                            'start /wait ' + Paths.tools + r'\fbx2gltf.exe --binary --verbose --fbx-temp-dir .\Temp -i "' +
                           os.path.normpath(eachModel) + '" -o ' + os.path.normpath(os.path.join(Paths.assets, 'actors',
                                                              self.modelTypeComboBox.currentText(), name + '.glb')),
                            shell=True, cwd=os.getcwd())
                        if self.objCmCheckbox.isChecked():
                            StaticMethods.addObjectInCreationModeInventory(cmState, name, 'objects')

                        if self.objDbCheckbox.isChecked():
                            if self.isExistInObjDb(name) == False:
                                self.objectsDbList.append(self.createNewObjForDb(name))
                    else:
                        pass
                else:
                    subprocess.call(
                        'start /wait ' + Paths.tools + r'\fbx2gltf.exe --binary --verbose --fbx-temp-dir .\Temp -i ' +
                        os.path.normpath(eachModel) + ' -o ' + os.path.normpath(os.path.join(Paths.assets, 'actors',
                                                          self.modelTypeComboBox.currentText(), name + '.glb')),
                        shell=True, cwd=os.getcwd())
                    if self.objCmCheckbox.isChecked():
                        StaticMethods.addObjectInCreationModeInventory(cmState, name, 'objects')

                    if self.objDbCheckbox.isChecked():
                        if self.isExistInObjDb(name) == False:
                            self.objectsDbList.append(self.createNewObjForDb(name))

        if self.objDbCheckbox.isChecked():
            self.objectsDbDict['objects'] = self.objectsDbList
            with open(Paths.objectsDb, 'w') as objectsDb:
                json.dump(self.objectsDbDict, objectsDb, indent=3, ensure_ascii=False, separators=(',', ':'))

        StaticMethods.updateCreationModeInventoryFile(cmState, Paths.creationModeInventory)

        self.objDbCheckbox.setChecked(False)
        self.objCmCheckbox.setChecked(False)
        self.fbxListWidget.clear()
        self.files.clear()
        shutil.rmtree(os.path.join(os.getcwd(), 'Temp'))

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
    Ui_FbxConverter(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())



