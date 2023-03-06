import sqlite3


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
