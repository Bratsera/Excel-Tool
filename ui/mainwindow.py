# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonExport = QtWidgets.QPushButton(self.centralwidget)
        self.buttonExport.setObjectName("buttonExport")
        self.gridLayout.addWidget(self.buttonExport, 5, 1, 1, 1)
        self.buttonChooseDir = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonChooseDir.setFont(font)
        self.buttonChooseDir.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.buttonChooseDir.setObjectName("buttonChooseDir")
        self.gridLayout.addWidget(self.buttonChooseDir, 0, 0, 1, 3)
        self.labValueTable = QtWidgets.QTableWidget(self.centralwidget)
        self.labValueTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.labValueTable.setColumnCount(0)
        self.labValueTable.setObjectName("labValueTable")
        self.labValueTable.setRowCount(0)
        self.gridLayout.addWidget(self.labValueTable, 4, 0, 1, 3)
        self.labValues = QtWidgets.QComboBox(self.centralwidget)
        self.labValues.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.labValues.setEditable(True)
        self.labValues.setCurrentText("")
        self.labValues.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.labValues.setFrame(True)
        self.labValues.setModelColumn(0)
        self.labValues.setObjectName("labValues")
        self.gridLayout.addWidget(self.labValues, 2, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.sourceDirText = QtWidgets.QLabel(self.centralwidget)
        self.sourceDirText.setText("")
        self.sourceDirText.setObjectName("sourceDirText")
        self.gridLayout.addWidget(self.sourceDirText, 1, 1, 1, 2)
        self.buttonShow = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonShow.setFont(font)
        self.buttonShow.setObjectName("buttonShow")
        self.gridLayout.addWidget(self.buttonShow, 2, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuExit = QtWidgets.QAction(MainWindow)
        self.menuExit.setObjectName("menuExit")
        self.menuOpen = QtWidgets.QAction(MainWindow)
        self.menuOpen.setObjectName("menuOpen")
        self.menuExport = QtWidgets.QAction(MainWindow)
        self.menuExport.setObjectName("menuExport")
        self.menu.addAction(self.menuOpen)
        self.menu.addAction(self.menuExport)
        self.menu.addAction(self.menuExit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.labValues.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonExport.setText(_translate("MainWindow", "Tabelle exportieren"))
        self.buttonChooseDir.setText(_translate("MainWindow", "Quellordner auswählen"))
        self.labValues.setPlaceholderText(_translate("MainWindow", "Laborwert auswählen:"))
        self.label.setText(_translate("MainWindow", "Ausgewählter Pfad:"))
        self.buttonShow.setText(_translate("MainWindow", "Anzeigen"))
        self.label_2.setText(_translate("MainWindow", "Befund-Liste:"))
        self.menu.setTitle(_translate("MainWindow", "Datei"))
        self.menuExit.setText(_translate("MainWindow", "Beenden"))
        self.menuOpen.setText(_translate("MainWindow", "Ordner öffnen"))
        self.menuExport.setText(_translate("MainWindow", "Tabelle exportieren"))
