import pandas as pd
import sqlite3


def xls_to_sql(name):
    connection = sqlite3.connect('shows.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Sites
                  (Name TEXT, Url TEXT, Xpath TEXT)''')
    datafile = pd.read_excel(name, sheet_name='Data')
    datafile.to_sql('Sites', connection, if_exists='replace', index=False)
    return datafile
