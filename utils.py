import pandas as pd
import sqlite3

ERROR_TYPE_MESSAGE = 'Неверный тип файла! Файл должен быть формата xlsx!'
ERROR_FILL_MESSAGE = 'Неверно заполнен файл! В файле должно быть три столбца!'


def xls_to_sql(name):
    """
    This function uploading info from xlsx file to sqlite base.

    param name: Name of file what needs to convert.
    return: Error message or result of uploading
    """
    if 'xlsx' not in name:
        return ERROR_TYPE_MESSAGE
    connection = sqlite3.connect('shows.db')
    datafile = pd.read_excel(name, sheet_name='Data')
    if datafile.shape[1] != 3:
        return ERROR_FILL_MESSAGE
    datafile.to_sql('Sites', connection, if_exists='replace', index=False)
    return datafile


