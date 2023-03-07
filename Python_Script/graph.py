import sqlite3
import pandas as pd
from PIL import Image
import matplotlib  # needed dependency for panda


def get_graph(timestamp, datatype):
    query = ""
    einheit = ""
    if datatype == "Feinstaub P1":
        query = (f'SELECT P1, TIME(timestamp) '
                 'FROM Feinstaub '
                 'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)
        einheit = " µg/m^3"
        datatype = "P1"

    if datatype == "Feinstaub P2":
        query = (f'SELECT P2, TIME(timestamp) '
                 'FROM Feinstaub '
                 'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)
        einheit = " µg/m^3"
        datatype = "P2"

    if datatype == "Temperatur":
        query = ('SELECT temperature, TIME(timestamp) '
                 'FROM Temperatur_Luftdruck '
                 'WHERE DATE(timestamp) = DATE(\'{}\')').format(timestamp)
        einheit = " °C"
        datatype = "temperature"

    if datatype == "Luftfeuchtigkeit":
        query = ('SELECT humidity, TIME(timestamp) '
                 'FROM Temperatur_Luftdruck '
                 'WHERE DATE(timestamp) = DATE(\'{}\') '
                 'AND humidity > 1 '
                 'AND humidity < 99').format(timestamp)
        einheit = " %"
        datatype = "humidity"

    my_conn = sqlite3.connect("../Database/Feinstaubprojekt.sqlite")

    try:
        df = pd.read_sql(query, my_conn)
        plot = df.plot.line(title=datatype + " in " + einheit, x='TIME(timestamp)', y=datatype, fontsize=7, figsize=(4, 2))
        fig = plot.get_figure()
        fig.savefig("Resources/graph.png")
    except TypeError:
        image = Image.open('Resources/placeholder.png')
        image.save('Resources/graph.png')
        pass

    my_conn.close()
