import sqlite3

print("Please enter date in format YYYY-MM-DD:")
timestamp = "2022-03-14" # input()
print("Please enter wanted datatype out of Feinstaub_P1/Feinstaub_P2/Temperatur/Luftfeuchtigkeit:")
datatype = "Feinstaub_P1" # input()
abfrage = ""

if datatype == "Feinstaub_P1":
    abfrage = (f'SELECT MIN(P1), MAX(P1), AVG(P1) '
               'FROM Feinstaub '
               'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)

if datatype == "Feinstaub_P2":
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
               'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)

con = sqlite3.connect("../Database/Feinstaubprojekt")
cur = con.cursor()

for row in cur.execute(abfrage):
    print("Min: ", round(row[0], 2))
    print("Max: ", round(row[1], 2))
    print("Avg: ", round(row[2], 2))
