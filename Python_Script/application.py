from tkinter import *
from tkinter import ttk
from main import query_database
from main import update_database
from graph import get_graph
from pdf import create_pdf
import re


def get_data():
    try:
        if not re.match("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", date.get()):
            raise ValueError("Invalid date")
        if datatype.get() == "":
            raise ValueError("Choose datatype")
        date_value = date.get()
        datatype_value = datatype.get()
        data_array = query_database(date_value, datatype_value)
        get_graph(date_value, datatype_value)
        graph = PhotoImage(file='Resources/graph.png')
        image.configure(image=graph)
        image.image = graph
        minimum.set(data_array[0])
        maximum.set(data_array[1])
        average.set(data_array[2])
        info.set("Done")
        root.update()
    except ValueError as e:
        info.set(e.args[0])
        root.update()
        pass
    root.after(2000, info.set(""))


def export_pdf():
    try:
        date_value = date.get()
        datatype_value = datatype.get()
        minimum_value = minimum.get()
        maximum_value = maximum.get()
        average_value = average.get()
        graph = 'Resources/graph.png'
        if minimum_value is not None and minimum_value != "" and minimum_value != "N/A":
            create_pdf(date_value, datatype_value, minimum_value, maximum_value, average_value, graph)
            info.set("Data exported successfully")
            root.update()
        else:
            info.set("No data to export")
            root.update()
    except:
        info.set("Export failed")
        root.update()
        pass
    root.after(2000, info.set(""))


def update_data():
    info.set("Loading...")
    root.update()
    try:
        info.set(update_database())
        root.update()
    except:
        info.set("Update failed")
        root.update()
        pass
    root.after(2000, info.set(""))


root = Tk()
root.title("Feinstaubdaten")

style = ttk.Style()
style.configure("TFrame", background="#262626")
mainframe = ttk.Frame(root, padding="5 5 12 12", style="TFrame")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

date = StringVar()
date_entry = ttk.Entry(mainframe, width=10, textvariable=date)
date_entry.grid(column=1, row=1, sticky=(W, E))

datatype = StringVar()
datatype_entry = ttk.Combobox(mainframe, state="readonly", textvariable=datatype,
                              values=('Feinstaub P1', 'Feinstaub P2', 'Temperatur', 'Luftfeuchtigkeit'))
datatype_entry.grid(column=1, row=2, sticky=(W, E))

minimum = StringVar()
ttk.Label(mainframe, textvariable=minimum, background="#262626", foreground="white").grid(column=1, row=3, sticky=E)

maximum = StringVar()
ttk.Label(mainframe, textvariable=maximum, background="#262626", foreground="white").grid(column=1, row=4, sticky=E)

average = StringVar()
ttk.Label(mainframe, textvariable=average, background="#262626", foreground="white").grid(column=1, row=5, sticky=E)

info = StringVar()
ttk.Label(mainframe, textvariable=info, background="#262626", foreground="green").grid(column=1, columnspan=2, row=6, sticky=W)

style.configure('U.TButton', background='yellow', forground='yellow')
style.configure('D.TButton', background='green')
style.configure('E.TButton', background='red')

ttk.Button(mainframe, text="Get data", command=get_data, width=20, style='D.TButton').grid(column=2, row=7, sticky=W)
ttk.Button(mainframe, text="Export", command=export_pdf, width=10, style='E.TButton').grid(column=1, row=7, sticky=W)
ttk.Button(mainframe, text="Update", command=update_data, width=10, style='U.TButton').grid(column=1, row=7, sticky=E)

placeholder = PhotoImage(file="Resources/placeholder.png")
image = Label(master=mainframe, image=placeholder, width=400, height=200)
image.grid(column=0, rowspan=7, row=1, sticky=NW)

ttk.Label(mainframe, text="Date (YYYY-MM-DD)", background="#262626", foreground="white").grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text="Datatype", background="#262626", foreground="white").grid(column=2, row=2, sticky=W)
ttk.Label(mainframe, text="Minimum", background="#262626", foreground="white").grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="Maximum", background="#262626", foreground="white").grid(column=2, row=4, sticky=W)
ttk.Label(mainframe, text="Average", background="#262626", foreground="white").grid(column=2, row=5, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

date_entry.focus()
root.mainloop()
