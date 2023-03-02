import sqlite3


def query_database(timestamp, datatype):
    returned_data = [""] * 3
    abfrage = ""

    if datatype == "Feinstaub P1":
        abfrage = (f'SELECT MIN(P1), MAX(P1), AVG(P1) '
                   'FROM Feinstaub '
                   'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)

    if datatype == "Feinstaub P2":
        abfrage = (f'SELECT MIN(P2), MAX(P2), AVG(P2) '
                   'FROM Feinstaub '
                   'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)

    if datatype == "Temperatur":
        abfrage = ('SELECT MIN(temperature), MAX(temperature), AVG(temperature) '
                   'FROM Temperatur_Luftdruck '
                   'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)

    if datatype == "Luftfeuchtigkeit":
        abfrage = ('SELECT MIN(humidity), MAX(humidity), AVG(humidity) '
                   'FROM Temperatur_Luftdruck '
                   'WHERE DATE(timestamp) = DATE(\'{}\') '
                   'AND humidity > 1 '
                   'AND humidity < 99').format(timestamp)

    con = sqlite3.connect("../Database/Feinstaubprojekt.sqlite")
    cur = con.cursor()

    for row in cur.execute(abfrage):
        returned_data[0] = round(row[0], 2)
        returned_data[1] = round(row[1], 2)
        returned_data[2] = round(row[2], 2)

    con.close()
    return returned_data
