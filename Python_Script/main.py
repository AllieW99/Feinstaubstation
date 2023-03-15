import pandas as pd
import sqlite3
import os
import shutil
from datetime import datetime, timedelta


def query_database(timestamp, datatype):
    returned_data = [""] * 3
    abfrage = ""
    einheit = ""

    if datatype == "Feinstaub P1":
        abfrage = (f'SELECT MIN(P1), MAX(P1), AVG(P1) '
                   'FROM Feinstaub '
                   'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)
        einheit = " µg/m^3"

    if datatype == "Feinstaub P2":
        abfrage = (f'SELECT MIN(P2), MAX(P2), AVG(P2) '
                   'FROM Feinstaub '
                   'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)
        einheit = " µg/m^3"

    if datatype == "Temperatur":
        abfrage = ('SELECT MIN(temperature), MAX(temperature), AVG(temperature) '
                   'FROM Temperatur_Luftdruck '
                   'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)
        einheit = " °C"

    if datatype == "Luftfeuchtigkeit":
        abfrage = ('SELECT MIN(humidity), MAX(humidity), AVG(humidity) '
                   'FROM Temperatur_Luftdruck '
                   'WHERE DATE(timestamp) = DATE(\'{}\') '
                   'AND humidity > 1 '
                   'AND humidity < 99').format(timestamp)
        einheit = " %"

    con = sqlite3.connect("../Database/Feinstaubprojekt.sqlite")
    cur = con.cursor()

    for row in cur.execute(abfrage):
        try:
            returned_data[0] = str(round(row[0], 2)) + einheit
            returned_data[1] = str(round(row[1], 2)) + einheit
            returned_data[2] = str(round(row[2], 2)) + einheit
        except TypeError:
            returned_data[0] = "N/A"
            returned_data[1] = "N/A"
            returned_data[2] = "N/A"

    con.close()
    return returned_data


def update_database():
    # connect to database
    conn = sqlite3.connect('../Database/Feinstaubprojekt.sqlite')
    c = conn.cursor()

    # get the newest date
    try:
        c.execute("SELECT MAX(timestamp) FROM Feinstaub")
        last_entry_feinstaub = c.fetchone()[0]
        last_entry_feinstaub = datetime.strptime(last_entry_feinstaub, '%Y-%m-%dT%H:%M:%S')
        c.execute("SELECT MAX(timestamp) FROM Temperatur_Luftdruck")
        last_entry_temp_luftdruck = c.fetchone()[0]
        last_entry_temp_luftdruck = datetime.strptime(last_entry_temp_luftdruck, '%Y-%m-%dT%H:%M:%S')

        if last_entry_temp_luftdruck >= last_entry_feinstaub:
            oldest_date = last_entry_temp_luftdruck + timedelta(days=1)
        else:
            oldest_date = last_entry_feinstaub + timedelta(days=1)

        oldest_date = oldest_date.strftime("%Y-%m-%d")
    except Exception as e:
        print(e)
        return "Update failed"

    # Download CSV data
    download_script_path = "../Download_Script/Feinstaub_CSV_Downloader.ps1"
    download_path = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(download_path, 'Resources')
    ps_command = f"powershell.exe {download_script_path} -Path {download_path} -Start_Date {oldest_date}"
    os.system(ps_command)

    csv_folder = download_path
    today = datetime.today()
    date = datetime.strptime(oldest_date, "%Y-%m-%d")

    # update database
    while date < today:
        date = date.strftime("%Y-%m-%d")
        path_3659 = csv_folder + "/CSV/3659/" + f"{date}_sds011_sensor_3659.csv"

        if os.path.exists(path_3659):
            dataframe = pd.read_csv(path_3659, sep=";")
            dataframe = dataframe[["timestamp", "P1", "P2"]]

            for row in dataframe.itertuples():
                c.execute("INSERT OR IGNORE INTO Feinstaub(timestamp, P1, P2) VALUES (?, ?, ?)",
                          (row.timestamp, row.P1, row.P2))

        date = datetime.strptime(date, "%Y-%m-%d")
        date = date + timedelta(days=1)

    date = oldest_date
    date = datetime.strptime(date, "%Y-%m-%d")

    while date < today:
        date = date.strftime("%Y-%m-%d")
        path_3660 = csv_folder + "/CSV/3660/" + f"{date}_dht22_sensor_3660.csv"

        if os.path.exists(path_3660):
            dataframe = pd.read_csv(path_3660, sep=";")
            dataframe = dataframe[["temperature", "humidity", "timestamp"]]

            for row in dataframe.itertuples():
                c.execute(
                    "INSERT OR IGNORE INTO Temperatur_Luftdruck(timestamp, humidity, temperature) VALUES (?, ?, ?)",
                    (row.timestamp, row.temperature, row.humidity))

        date = datetime.strptime(date, "%Y-%m-%d")
        date = date + timedelta(days=1)

    # remove downloaded data
    try:
        shutil.rmtree(download_path + "\CSV")
    except:
        pass

    conn.commit()
    conn.close()
    return "Database updated successfully"
