import sys
import os
import csv
import pandas as pd
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog
from qtpy import QtWidgets
from ui.mainwindow import Ui_MainWindow
from datetime import datetime
from pandas import ExcelWriter

app = QtWidgets.QApplication(sys.argv)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Labor-Export Tool")
        a = self.ui.labValues
        a.setCurrentIndex(-1)
        a.lineEdit().setPlaceholderText("Laborwert auswählen")
        self.ui.buttonChooseDir.clicked.connect(self.chooseFolder)
        self.ui.buttonShow.clicked.connect(self.fillTable)
        self.ui.buttonExport.clicked.connect(self.exportFile)
        self.ui.menuOpen.triggered.connect(self.chooseFolder)
        self.ui.menuExport.triggered.connect(self.exportFile)
        self.ui.menuExit.triggered.connect(sys.exit)

    def chooseFolder(self):
        folderBrowser = QFileDialog()

        folderBrowser.setFileMode(QFileDialog.Directory)
        a = folderBrowser.getExistingDirectory(self, 'Choose Folder', os.path.dirname(__file__))
        if a:
            # Returns pathName with the '/' separators converted to separators that are appropriate for the underlying operating system.
            # On Windows, toNativeSeparators("c:/winnt/system32") returns
            # "c:\winnt\system32".

            a = QDir.toNativeSeparators(a)
            self.clearTable()
            self.loadLabValueChoice(a)

    # Opens all files in the given directory (param: path).
    # Checks all existing lab-Values in the files and fills the QComboBox with entries of all lab-Values.
    def loadLabValueChoice(self, path):
        index = self.ui.labValues
        listValues = []

        # Clear the QComboBox
        for i in range(index.count()):
            index.setCurrentIndex(i)
            index.removeItem(0)

        # For all files in the directory
        for file in os.listdir(path):
            # print(file)

            filePath = os.path.join(path, file)

            # If the element is a file
            if not os.path.isdir(filePath):

                # Checks the filetype and calls the corresponding method to open and edit the files
                if (".xlsx" in file or ".xls" in file) and file[0] != ".":
                    # Read files and return all existing labValues in the opened file
                    listValues = self.readExcelFile(filePath, listValues)

                elif ".csv" in file and file[0] != ".":
                    listValues = self.readCsvFile(filePath, listValues)
        if len(listValues) == 0:
            error.information(self, "Keine Dateien gefunden",
                              "Es wurden keine Excel- oder CSV-Dateien im ausgewählten Ordner gefunden. "
                              "Bitte wählen Sie einen anderen Ordner aus.", error.Ok)
            self.chooseFolder()
        else:
            for value in listValues:
                index.insertItem(index.count(), str(value))
            self.ui.sourceDirText.setText(path)

    def readExcelFile(self, filePath, listValues):

        df = pd.read_excel(filePath, header=None)
        tests = df.iloc[8:]

        for pos, row in tests.iterrows():
            isValue = False

            for value in row[3:]:
                if not pd.isnull(value):
                    isValue = True
                    break

            if isValue and row[0] not in listValues:
                listValues.append(str(row[0]))
        return listValues

    def readCsvFile(self, filePath, listValues):

        with open(filePath, "r", newline="") as excel:

            reader = csv.reader(excel, delimiter=",", quotechar='"')

            fileList = []

            for line in reader:
                fileList.append(line)

            tests = fileList[8:]
            for row in tests:
                isValue = False
                for value in row[3:]:

                    if value != "":
                        isValue = True
                        break

                if isValue and line[0] not in listValues:
                    listValues.append(str(row[0]))

            return listValues

    def clearTable(self):
        labTable = self.ui.labValueTable

        for i in range(labTable.rowCount()):
            labTable.removeRow(0)
        for i in range(labTable.columnCount()):
            labTable.removeColumn(0)
        labTable.setRowCount(0)

    def fillTable(self):

        if self.ui.labValues.count() <= 0:
            error.information(self, "Kein Ordner ausgewählt", "Bitte wählen Sie zuerst einen Ordner aus.", error.Ok)

        elif self.ui.labValues.currentIndex() == -1:

            error.information(self, "Kein Laborwert ausgewählt", "Bitte wählen Sie zuerst einen Laborwert aus.",
                              error.Ok)

        else:
            self.clearTable()
            labTable = self.ui.labValueTable

            curRow = labTable.rowCount()
            labTable.insertRow(curRow)
            for i in range(0, 8):
                labTable.insertColumn(i)

            labTable.setItem(curRow, 0, QtWidgets.QTableWidgetItem("Name"))
            labTable.setItem(curRow, 1, QtWidgets.QTableWidgetItem("Geurtsdatum"))
            labTable.setItem(curRow, 2, QtWidgets.QTableWidgetItem("Fallnummer"))
            labTable.setItem(curRow, 3, QtWidgets.QTableWidgetItem("Station"))
            labTable.setItem(curRow, 4, QtWidgets.QTableWidgetItem("Analyse"))
            labTable.setItem(curRow, 5, QtWidgets.QTableWidgetItem("Referenz"))
            labTable.setItem(curRow, 6, QtWidgets.QTableWidgetItem("Einheit"))
            labTable.setItem(curRow, 7, QtWidgets.QTableWidgetItem("Befunde"))

            for file in os.listdir(self.ui.sourceDirText.text()):

                filePath = os.path.join(self.ui.sourceDirText.text(), file)
                # print(filePath)

                if not os.path.isdir(filePath):
                    if (".xlsx" in file or ".xls" in file) and file[0] != ".":

                        df = pd.read_excel(filePath, header=None)
                        tests = df.iloc[8:]
                        row1 = labTable.rowCount()
                        row2 = row1 + 1
                        for pos, row in tests.iterrows():
                            if row[0] == self.ui.labValues.currentText():
                                labTable.insertRow(row1)
                                labTable.insertRow(row2)
                                labTable.setItem(row2, 0, QtWidgets.QTableWidgetItem(str(df.iloc[0][1])))
                                labTable.setItem(row2, 1, QtWidgets.QTableWidgetItem(str(df.iloc[1][1])))
                                labTable.setItem(row2, 2, QtWidgets.QTableWidgetItem(str(df.iloc[2][1])))
                                labTable.setItem(row2, 3, QtWidgets.QTableWidgetItem(str(df.iloc[3][1])))
                                labTable.setItem(row2, 4, QtWidgets.QTableWidgetItem(str(row[0])))
                                labTable.setItem(row2, 5, QtWidgets.QTableWidgetItem(str(row[1])))
                                labTable.setItem(row2, 6, QtWidgets.QTableWidgetItem(str(row[2])))

                                labResultValues = row[3:]
                                valueDate = df.iloc[5][3:]
                                counter = 7

                                # Create row and insert the lab-result dates
                                for i in range(len(labResultValues)):
                                    # print(labResultValues[i + 3])
                                    if not pd.isnull(labResultValues[i + 3]):
                                        if labTable.columnCount() - 1 < counter:
                                            labTable.insertColumn(counter)
                                        labTable.setItem(row1, counter,
                                                         QtWidgets.QTableWidgetItem(str(valueDate[i + 3])))
                                        labTable.setItem(row2, counter,
                                                         QtWidgets.QTableWidgetItem(str(labResultValues[i + 3])))
                                        counter += 1

                                break

                    elif ".csv" in file and file[0] != ".":
                        with open(filePath, "r", newline="") as excel:
                            reader = csv.reader(excel, delimiter=",", quotechar='"')

                            fileList = []

                            for line in reader:
                                fileList.append(line)

                            row1 = labTable.rowCount()
                            row2 = row1 + 1

                            labResults = fileList[8:]

                            # Find the target lab result
                            for line in labResults:
                                if line[0] == self.ui.labValues.currentText():
                                    labTable.insertRow(row1)
                                    labTable.insertRow(row2)
                                    labTable.setItem(row2, 0, QtWidgets.QTableWidgetItem(fileList[0][1]))
                                    labTable.setItem(row2, 1, QtWidgets.QTableWidgetItem(fileList[1][1]))
                                    labTable.setItem(row2, 2, QtWidgets.QTableWidgetItem(fileList[2][1]))
                                    labTable.setItem(row2, 3, QtWidgets.QTableWidgetItem(fileList[3][1]))
                                    labTable.setItem(row2, 4, QtWidgets.QTableWidgetItem(line[0]))
                                    labTable.setItem(row2, 5, QtWidgets.QTableWidgetItem(line[1]))
                                    labTable.setItem(row2, 6, QtWidgets.QTableWidgetItem(line[2]))

                                    labResultValues = line[3:]
                                    valueDate = fileList[5][3:]
                                    counter = 7
                                    # Create row and insert the lab-result dates
                                    for i in range(len(labResultValues)):

                                        if labResultValues[i] != "":
                                            if labTable.columnCount() - 1 < counter:
                                                labTable.insertColumn(counter)
                                            labTable.setItem(row1, counter, QtWidgets.QTableWidgetItem(valueDate[i]))
                                            labTable.setItem(row2, counter,
                                                             QtWidgets.QTableWidgetItem(labResultValues[i]))
                                            counter += 1

                                    break

    def exportFile(self):
        labTable = self.ui.labValueTable
        if labTable.rowCount() == 0:
            error.information(self, "Tabelle ist leer", "Die Tabelle ist leer. Bitte befüllen Sie diese erst, "
                                                        "indem Sie einen Laborwert auswählen und auf den Button 'Anzeigen' klicken.",
                              error.Ok)
        else:
            folderBrowser = QFileDialog()
            rootPath = os.path.join(os.path.dirname(__file__), "Export", datetime.now().strftime(
                "%d-%m-%Y_%H.%M") + "_Export_" + self.ui.labValues.currentText())

            a = folderBrowser.getSaveFileName(self, 'Save file as', rootPath, "Excel-file (*.xlsx *.xls)")

            if a[0] != '':

                # Returns pathName with the '/' separators converted to separators that are appropriate for the underlying operating system.
                # On Windows, toNativeSeparators("c:/winnt/system32") returns
                # "c:\winnt\system32".

                a = QDir.toNativeSeparators(a[0])
                exportList = []

                for i in range(labTable.rowCount()):

                    row = []
                    for j in range(labTable.columnCount()):

                        value = labTable.item(i, j)
                        if value:
                            row.append(labTable.item(i, j).text())
                        else:
                            row.append("")
                    exportList.append(row)

                dataFrame = pd.DataFrame(exportList)

                # print(dataFrame)
                try:
                    with ExcelWriter(a, date_format='dd.mm.yyyy', datetime_format='dd.mm.yyyy hh:mm:ss') as writer:
                        dataFrame.to_excel(writer, index=False, header=False)
                except PermissionError:
                    error.critical(self, "Fehler beim Speichern der Datei",
                                   "Die Datei kann nicht überschrieben werden. "
                                   "Sie ist möglicherweise schreibgeschützt oder aktuell geöffnet "
                                   "oder Sie verfügen nicht über die erforderliche Berechtigung.", error.Ok)
                    self.exportFile()


window = MainWindow()
window.show()
error = QtWidgets.QMessageBox()

sys.exit(app.exec_())
