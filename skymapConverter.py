from PyQt5 import QtCore, QtWidgets, QtGui
import os
import subprocess
from managerPaths import Paths
from staticMethods import StaticMethods

class Ui_SkymapConverter(object):
    def __init__(self, win, app):
        self.app = app
        self.skyboxToConvert = []
        self.iblToConvert = []
        self.setupUi(win)
        win.show()

    def setupUi(self, skymapConverter):
        skymapConverter.resize(350, 300)
        skymapConverter.setObjectName('skymapConverterWindow')
        skymapConverter.setWindowTitle('skymapConverter')

        self.centralwidget = QtWidgets.QWidget(skymapConverter)
        self.centralwidget.setObjectName('centralwidget')

        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setObjectName('centralLayout')
        self.centralLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.centralLayout.setContentsMargins(20, 20, 20, 20)

        ###########################################################################

        self.skyboxWidget = QtWidgets.QWidget(self.centralwidget)
        self.skyboxWidget.setObjectName('skyboxWidget')

        self.skyboxLayout = QtWidgets.QVBoxLayout()
        self.skyboxLayout.setObjectName('skyboxLayout')
        self.skyboxLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.skyboxLabel = QtWidgets.QLabel(self.skyboxWidget)
        self.skyboxLabel.setObjectName('skyboxLabel')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.skyboxLabel.setFont(font)
        self.skyboxLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.skyboxLabel.setText('SKYBOX CONVERTER')
        self.skyboxLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.boxLayoutWidget = QtWidgets.QWidget(self.skyboxWidget)
        self.boxLayoutWidget.setObjectName('formLayoutWidget')

        self.boxLayout = QtWidgets.QHBoxLayout()
        self.boxLayout.setObjectName('formLayout')
        self.boxLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.skyboxLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.skyboxLineEdit.setObjectName('skyboxLineEdit')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.skyboxLineEdit.setFont(font)
        self.skyboxLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.skyboxAddButton = QtWidgets.QPushButton(self.centralwidget)
        self.skyboxAddButton.setObjectName('skyboxAddButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.skyboxAddButton.setFont(font)
        self.skyboxAddButton.setText('Add file')
        self.skyboxAddButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.skyboxAddButton.clicked.connect(lambda: self.chooseSkymapToConvert(self.skyboxToConvert, self.skyboxLineEdit))

        self.boxLayout.addWidget(self.skyboxLineEdit, 8)
        self.boxLayout.addWidget(self.skyboxAddButton, 2)

        self.boxLayoutWidget.setLayout(self.boxLayout)

        ################################################################################################

        self.bottomWidget = QtWidgets.QWidget(self.skyboxWidget)
        self.bottomWidget.setObjectName('bottomWidget')

        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout.setObjectName('bottomLayout')
        self.bottomLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.skyboxDestComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.skyboxDestComboBox.setObjectName('skyboxDestComboBox')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.skyboxDestComboBox.setFont(font)
        self.skyboxDestComboBox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
        self.skyboxDestComboBox.addItems(self.getDestComboBoxList())

        self.skyboxConvertButton = QtWidgets.QPushButton(self.centralwidget)
        self.skyboxConvertButton.setObjectName('skyboxConvertButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.skyboxConvertButton.setFont(font)
        self.skyboxConvertButton.setText('Convert')
        self.skyboxConvertButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                               QtWidgets.QSizePolicy.Policy.Expanding)
        self.skyboxConvertButton.clicked.connect(lambda: self.convert(self.skyboxToConvert, self.skyboxLineEdit,
                                                                      'skybox', 'ibl', self.skyboxDestComboBox.currentText()))

        spacerH1 = QtWidgets.QSpacerItem(50, 40, QtWidgets.QSizePolicy.Policy.Fixed,
                                         QtWidgets.QSizePolicy.Policy.Fixed)

        self.bottomLayout.addWidget(self.skyboxDestComboBox)
        self.bottomLayout.addItem(spacerH1)
        self.bottomLayout.addWidget(self.skyboxConvertButton)

        self.bottomWidget.setLayout(self.bottomLayout)

        self.skyboxLayout.addWidget(self.skyboxLabel)
        self.skyboxLayout.addWidget(self.boxLayoutWidget)
        self.skyboxLayout.addWidget(self.bottomWidget)

        self.skyboxWidget.setLayout(self.skyboxLayout)

        #######################################################################

        self.hLine = QtWidgets.QFrame(self.centralwidget)
        self.hLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.hLine.setLineWidth(1)

        #########################################################################

        self.iblWidget = QtWidgets.QWidget(self.centralwidget)
        self.iblWidget.setObjectName('iblWidget')

        self.iblLayout = QtWidgets.QVBoxLayout()
        self.iblLayout.setObjectName('iblLayout')
        self.iblLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.iblLabel = QtWidgets.QLabel(self.iblWidget)
        self.iblLabel.setObjectName('iblLabel')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.iblLabel.setFont(font)
        self.iblLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.iblLabel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.iblLabel.setText('IBL CONVERTER')

        self.midLayoutWidget = QtWidgets.QWidget(self.iblWidget)
        self.midLayoutWidget.setObjectName('midLayoutWidget')

        self.midLayout = QtWidgets.QHBoxLayout()
        self.midLayout.setObjectName('midLayout')
        self.midLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.iblLineEdit = QtWidgets.QLineEdit(self.midLayoutWidget)
        self.iblLineEdit.setObjectName('iblLineEdit')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.iblLineEdit.setFont(font)
        self.iblLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        self.iblAddButton = QtWidgets.QPushButton(self.midLayoutWidget)
        self.iblAddButton.setObjectName('iblAddButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.iblAddButton.setFont(font)
        self.iblAddButton.setText('Add file')
        self.iblAddButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.iblAddButton.clicked.connect(lambda: self.chooseSkymapToConvert(self.iblToConvert, self.iblLineEdit))

        self.midLayout.addWidget(self.iblLineEdit, 8)
        self.midLayout.addWidget(self.iblAddButton, 2)

        self.midLayoutWidget.setLayout(self.midLayout)

        self.iblBottomWidget = QtWidgets.QWidget(self.iblWidget)
        self.iblBottomWidget.setObjectName('iblBottomWidget')

        self.iblBottomLayout = QtWidgets.QHBoxLayout()
        self.iblBottomLayout.setObjectName('iblBottomLayout')
        self.iblBottomLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.iblDestComboBox = QtWidgets.QComboBox(self.iblBottomWidget)
        self.iblDestComboBox.setObjectName('iblDestComboBox')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.iblDestComboBox.setFont(font)
        self.iblDestComboBox.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.iblDestComboBox.addItems(self.getDestComboBoxList())

        self.iblConvertButton = QtWidgets.QPushButton(self.iblBottomWidget)
        self.iblConvertButton.setObjectName('iblConvertButton')
        font = QtGui.QFont()
        font.setFamily("Oswald Light")
        font.setPointSize(StaticMethods.setFontSizeCaption(self.app))
        self.iblConvertButton.setFont(font)
        self.iblConvertButton.setText('Convert')
        self.iblConvertButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.iblConvertButton.clicked.connect(lambda: self.convert(self.iblToConvert, self.iblLineEdit,
                                                                   'ibl', 'skybox', self.iblDestComboBox.currentText()))

        spacerH2 = QtWidgets.QSpacerItem(50, 40, QtWidgets.QSizePolicy.Policy.Fixed,
                                         QtWidgets.QSizePolicy.Policy.Fixed)

        self.iblBottomLayout.addWidget(self.iblDestComboBox)
        self.iblBottomLayout.addItem(spacerH2)
        self.iblBottomLayout.addWidget(self.iblConvertButton)

        self.iblBottomWidget.setLayout(self.iblBottomLayout)

        self.iblLayout.addWidget(self.iblLabel)
        self.iblLayout.addWidget(self.midLayoutWidget)
        self.iblLayout.addWidget(self.iblBottomWidget)

        self.iblWidget.setLayout(self.iblLayout)

        self.centralLayout.addWidget(self.skyboxWidget)
        self.centralLayout.addWidget(self.hLine)
        self.centralLayout.addWidget(self.iblWidget)

        self.centralwidget.setLayout(self.centralLayout)

        skymapConverter.setCentralWidget(self.centralwidget)

    def getDestComboBoxList(self):
        destList = []
        destList.append('World')
        for eachDir in os.listdir(Paths.bundles):
            destList.append(eachDir)
        return destList

    def chooseSkymapToConvert(self, path, lineEdit):
        fileDialog = QtWidgets.QFileDialog()
        fileToConvert = fileDialog.getOpenFileName(filter='HDR (*.hdr *.hdri)')[0]
        path.append(fileToConvert)
        lineEdit.setText(os.path.basename(fileToConvert))

    def convert(self, path, lineEdit, mapToSave, mapToDelete, dest):
        if dest == 'World':
            destinationPath = Paths.world
        else:
            destinationPath = os.path.normpath(os.path.join(Paths.bundles, dest, 'world'))

        if os.path.exists(os.path.join(destinationPath, 'skymap_' + mapToSave + '.ktx')):
            questionBox = QtWidgets.QMessageBox()
            questionBox.setWindowTitle('Delete')
            questionBox.setIcon(QtWidgets.QMessageBox.Question)
            questionBox.setText(mapToSave.capitalize() + ' already exists. Do you want to replace?')
            questionBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            button = questionBox.exec()

            if button == QtWidgets.QMessageBox.Yes:
                os.remove(os.path.join(destinationPath, 'skymap_' + mapToSave + '.ktx'))
                subprocess.call('start /wait ' + Paths.tools + '\cmgen.exe -x "' + \
                                destinationPath + '" --format=ktx --size=256 "' + os.path.normpath(path[0]) + '"',
                                shell=True, cwd=Paths.tools)
                os.remove(os.path.join(destinationPath, 'world_' + mapToDelete + '.ktx'))
                os.rename(os.path.join(destinationPath, 'world_' + mapToSave + '.ktx'),
                          os.path.join(destinationPath, 'skymap_' + mapToSave + '.ktx'))
                messageBox = QtWidgets.QMessageBox()
                messageBox.setIcon(QtWidgets.QMessageBox.Information)
                messageBox.setText("Info")
                messageBox.setInformativeText('Done!')
                messageBox.setWindowTitle("Info")
                messageBox.exec_()

                path.clear()
                lineEdit.clear()
        else:
            subprocess.call('start /wait ' + Paths.tools + '\cmgen.exe -x "' + \
                            destinationPath + '" --format=ktx --size=256 "' + os.path.normpath(path[0]) + '"',
                            shell=True, cwd=Paths.tools)
            os.remove(os.path.join(destinationPath, 'world_' + mapToDelete + '.ktx'))
            os.rename(os.path.join(destinationPath, 'world_' + mapToSave + '.ktx'),
                      os.path.join(destinationPath, 'skymap_' + mapToSave + '.ktx'))
            messageBox = QtWidgets.QMessageBox()
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
            messageBox.setText("Info")
            messageBox.setInformativeText('Done!')
            messageBox.setWindowTitle("Info")
            messageBox.exec_()

            path.clear()
            lineEdit.clear()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    Paths.getDir('Release')
    Ui_SkymapConverter(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
