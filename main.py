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
from utils import file_reader

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
        self.ui.buttonChooseDir.clicked.connect(self.choose_folder)
        self.ui.buttonShow.clicked.connect(self.display_data)
        self.ui.buttonExport.clicked.connect(self.export_file)
        self.ui.menuOpen.triggered.connect(self.choose_folder)
        self.ui.menuExport.triggered.connect(self.export_file)
        self.ui.menuExit.triggered.connect(sys.exit)

    def choose_folder(self):
        folder_browser = QFileDialog()

        folder_browser.setFileMode(QFileDialog.Directory)
        a = folder_browser.getExistingDirectory(self, 'Choose Folder', os.path.dirname(__file__))
        if a:
            # Returns pathName with the '/' separators converted to separators
            # that are appropriate for the underlying operating system.
            # On Windows, toNativeSeparators("c:/winnt/system32") returns
            # "c:\winnt\system32".

            a = QDir.toNativeSeparators(a)
            self.clear_table()
            self.extract_lab_value_choice(a)

    # Opens all files in the given directory (param: path).
    # Checks all existing lab-Values in the files and fills the QComboBox with entries of all lab-Values.
    def extract_lab_value_choice(self, path):
        index = self.ui.labValues
        # Clear the QComboBox
        for i in range(index.count()):
            index.setCurrentIndex(i)
            index.removeItem(0)

        try:
            list_values = []
            # For all files in the directory
            for file in os.listdir(path):
                # print(file)

                file_path = os.path.join(path, file)

                # If the element is a file
                if not os.path.isdir(file_path):

                    # Checks the filetype and calls the corresponding method to open and edit the files
                    if (".xlsx" in file or ".xls" in file) and file[0] != ".":
                        # Read files and return all existing labValues in the opened file
                        list_values = file_reader.read_excel_file(file_path, list_values)

                    elif ".csv" in file and file[0] != ".":
                        list_values = file_reader.read_csv_file(file_path, list_values)
            if len(list_values) == 0:
                error.information(self, "Keine Dateien gefunden",
                                  "Es wurden keine Excel- oder CSV-Dateien im ausgewählten Ordner gefunden. "
                                  "Bitte wählen Sie einen anderen Ordner aus.", error.Ok)
                self.choose_folder()
            else:
                cleared_values = list(set(list_values))
                cleared_values.sort()
                for value in cleared_values:
                    index.insertItem(index.count(), str(value))
                self.ui.sourceDirText.setText(path)
        except ImportError:
            error.critical(self, "Fehler beim Laden der Datei",
                           "Beim Laden einer Datei ist ein Fehler aufgetreten. Bitte stellen Sie sicher, dass die "
                           "ausgewählten Datein die korrekte Tabellenstruktur aufweisen.",
                           error.Ok)

    def clear_table(self):
        lab_table = self.ui.labValueTable

        for i in range(lab_table.rowCount()):
            lab_table.removeRow(0)
        for i in range(lab_table.columnCount()):
            lab_table.removeColumn(0)
        lab_table.setRowCount(0)

    def display_data(self):

        if self.ui.labValues.count() <= 0:
            error.information(self, "Kein Ordner ausgewählt", "Bitte wählen Sie zuerst einen Ordner aus.", error.Ok)

        elif self.ui.labValues.currentIndex() == -1:

            error.information(self, "Kein Laborwert ausgewählt", "Bitte wählen Sie zuerst einen Laborwert aus.",
                              error.Ok)

        else:
            self.clear_table()
            lab_table = self.ui.labValueTable

            cur_row = lab_table.rowCount()
            lab_table.insertRow(cur_row)
            for i in range(0, 8):
                lab_table.insertColumn(i)

            lab_table.setItem(cur_row, 0, QtWidgets.QTableWidgetItem("Name"))
            lab_table.setItem(cur_row, 1, QtWidgets.QTableWidgetItem("Geurtsdatum"))
            lab_table.setItem(cur_row, 2, QtWidgets.QTableWidgetItem("Fallnummer"))
            lab_table.setItem(cur_row, 3, QtWidgets.QTableWidgetItem("Station"))
            lab_table.setItem(cur_row, 4, QtWidgets.QTableWidgetItem("Analyse"))
            lab_table.setItem(cur_row, 5, QtWidgets.QTableWidgetItem("Referenz"))
            lab_table.setItem(cur_row, 6, QtWidgets.QTableWidgetItem("Einheit"))
            lab_table.setItem(cur_row, 7, QtWidgets.QTableWidgetItem("Befunde"))

            for file in os.listdir(self.ui.sourceDirText.text()):

                file_path = os.path.join(self.ui.sourceDirText.text(), file)
                # print(file_path)

                if not os.path.isdir(file_path):
                    if (".xlsx" in file or ".xls" in file) and file[0] != ".":

                        df = pd.read_excel(file_path, header=None)
                        tests = df.iloc[8:]

                        row1 = lab_table.rowCount()
                        row2 = row1 + 1
                        for pos, row in tests.iterrows():
                            if row[0] == self.ui.labValues.currentText():
                                lab_table.insertRow(row1)
                                lab_table.insertRow(row2)
                                lab_table.setItem(row2, 0, QtWidgets.QTableWidgetItem(str(df.iloc[0][1])))
                                lab_table.setItem(row2, 1, QtWidgets.QTableWidgetItem(str(df.iloc[1][1])))
                                lab_table.setItem(row2, 2, QtWidgets.QTableWidgetItem(str(df.iloc[2][1])))
                                lab_table.setItem(row2, 3, QtWidgets.QTableWidgetItem(str(df.iloc[3][1])))
                                lab_table.setItem(row2, 4, QtWidgets.QTableWidgetItem(str(row[0])))
                                lab_table.setItem(row2, 5, QtWidgets.QTableWidgetItem(str(row[1])))
                                lab_table.setItem(row2, 6, QtWidgets.QTableWidgetItem(str(row[2])))

                                lab_result_values = row[3:]
                                value_date = df.iloc[5][3:]
                                counter = 7

                                # Create row and insert the lab-result dates
                                for i in range(len(lab_result_values)):
                                    # print(lab_result_values[i + 3])
                                    if not pd.isnull(lab_result_values[i + 3]):
                                        if lab_table.columnCount() - 1 < counter:
                                            lab_table.insertColumn(counter)
                                        lab_table.setItem(row1, counter,
                                                          QtWidgets.QTableWidgetItem(str(value_date[i + 3])))
                                        lab_table.setItem(row2, counter,
                                                          QtWidgets.QTableWidgetItem(str(lab_result_values[i + 3])))
                                        counter += 1

                                break

                    elif ".csv" in file and file[0] != ".":
                        with open(file_path, "r", newline="") as excel:
                            reader = csv.reader(excel, delimiter=",", quotechar='"')

                            file_list = []

                            for line in reader:
                                file_list.append(line)

                            row1 = lab_table.rowCount()
                            row2 = row1 + 1

                            lab_results = file_list[8:]

                            # Find the target lab result
                            for line in lab_results:
                                if line[0] == self.ui.labValues.currentText():
                                    lab_table.insertRow(row1)
                                    lab_table.insertRow(row2)
                                    lab_table.setItem(row2, 0, QtWidgets.QTableWidgetItem(file_list[0][1]))
                                    lab_table.setItem(row2, 1, QtWidgets.QTableWidgetItem(file_list[1][1]))
                                    lab_table.setItem(row2, 2, QtWidgets.QTableWidgetItem(file_list[2][1]))
                                    lab_table.setItem(row2, 3, QtWidgets.QTableWidgetItem(file_list[3][1]))
                                    lab_table.setItem(row2, 4, QtWidgets.QTableWidgetItem(line[0]))
                                    lab_table.setItem(row2, 5, QtWidgets.QTableWidgetItem(line[1]))
                                    lab_table.setItem(row2, 6, QtWidgets.QTableWidgetItem(line[2]))

                                    lab_result_values = line[3:]
                                    value_date = file_list[5][3:]
                                    counter = 7
                                    # Create row and insert the lab-result dates
                                    for i in range(len(lab_result_values)):

                                        if lab_result_values[i] != "":
                                            if lab_table.columnCount() - 1 < counter:
                                                lab_table.insertColumn(counter)
                                            lab_table.setItem(row1, counter, QtWidgets.QTableWidgetItem(value_date[i]))
                                            lab_table.setItem(row2, counter,
                                                              QtWidgets.QTableWidgetItem(lab_result_values[i]))
                                            counter += 1

                                    break

    def export_file(self):
        lab_table = self.ui.labValueTable
        if lab_table.rowCount() == 0:
            error.information(self,
                              "Tabelle ist leer",
                              "Die Tabelle ist leer. Bitte befüllen Sie diese erst, "
                              "indem Sie einen Laborwert auswählen und auf den Button 'Anzeigen' klicken.",
                              error.Ok)
        else:
            folder_browser = QFileDialog()
            root_path = os.path.join(os.path.dirname(__file__), "Export", datetime.now().strftime(
                "%d-%m-%Y_%H.%M") + "_Export_" + self.ui.labValues.currentText())

            a = folder_browser.getSaveFileName(self, 'Save file as', root_path, "Excel-file (*.xlsx *.xls)")

            if a[0] != '':

                # Returns pathName with the '/' separators converted to separators
                # that are appropriate for the underlying operating system.
                # On Windows, toNativeSeparators("c:/winnt/system32") returns
                # "c:\winnt\system32".

                a = QDir.toNativeSeparators(a[0])
                export_list = []

                for i in range(lab_table.rowCount()):

                    row = []
                    for j in range(lab_table.columnCount()):

                        value = lab_table.item(i, j)
                        if value:
                            row.append(lab_table.item(i, j).text())
                        else:
                            row.append("")
                    export_list.append(row)

                data_frame = pd.DataFrame(export_list)

                # print(data_frame)
                try:
                    with ExcelWriter(a, date_format='dd.mm.yyyy', datetime_format='dd.mm.yyyy hh:mm:ss') as writer:
                        data_frame.to_excel(writer, index=False, header=False)
                except PermissionError:
                    error.critical(self, "Fehler beim Speichern der Datei",
                                   "Die Datei kann nicht überschrieben werden. "
                                   "Sie ist möglicherweise schreibgeschützt oder aktuell geöffnet "
                                   "oder Sie verfügen nicht über die erforderliche Berechtigung.", error.Ok)


window = MainWindow()
window.show()
error = QtWidgets.QMessageBox()

sys.exit(app.exec_())
