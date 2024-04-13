import csv
import pandas as pd


def read_excel_file(file_path, list_values):
    df = pd.read_excel(file_path, header=None)

    tests = df.iloc[8:]

    for pos, row in tests.iterrows():
        is_value = False

        for value in row[3:]:
            if not pd.isnull(value):
                is_value = True
                break

        if is_value and row[0] not in list_values:
            list_values.append(str(row[0]))
    return list_values


def read_csv_file(file_path, list_values):
    with open(file_path, "r", newline="") as excel:

        reader = csv.reader(excel, delimiter=",", quotechar='"')

        file_list = []

        for line in reader:
            file_list.append(line)

        tests = file_list[8:]
        for row in tests:
            is_value = False
            for value in row[3:]:

                if value != "":
                    is_value = True
                    break

            if is_value and line[0] not in list_values:
                list_values.append(str(row[0]))

        return list_values
