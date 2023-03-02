from tkinter import *
from tkinter import ttk
from main import query_database


def get_data():
    try:
        date_value = date.get()
        datatype_value = datatype.get()
        data_array = query_database(date_value, datatype_value)
        minimum.set(data_array[0])
        maximum.set(data_array[1])
        average.set(data_array[2])
    except ValueError:
        pass


root = Tk()
root.title("Feinstaubdaten")

mainframe = ttk.Frame(root, padding="5 5 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

date = StringVar()
date_entry = ttk.Entry(mainframe, width=10, textvariable=date)
date_entry.grid(column=1, row=1, sticky=(W, E))

datatype = StringVar()
datatype_entry = ttk.Combobox(mainframe, state="readonly", textvariable=datatype, values=('Feinstaub P1', 'Feinstaub P2', 'Temperatur', 'Luftfeuchtigkeit'))
datatype_entry.grid(column=1, row=2, sticky=(W, E))

minimum = StringVar()
ttk.Label(mainframe, textvariable=minimum).grid(column=1, row=3, sticky=E)

maximum = StringVar()
ttk.Label(mainframe, textvariable=maximum).grid(column=1, row=4, sticky=E)

average = StringVar()
ttk.Label(mainframe, textvariable=average).grid(column=1, row=5, sticky=E)

ttk.Button(mainframe, text="Get data", command=get_data).grid(column=2, row=6, sticky=W)

ttk.Label(mainframe, text="Date (YYYY-MM-DD)").grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text="Datatype").grid(column=2, row=2, sticky=W)
ttk.Label(mainframe, text="Minimum").grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="Maximum").grid(column=2, row=4, sticky=W)
ttk.Label(mainframe, text="Average").grid(column=2, row=5, sticky=W)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

date_entry.focus()

root.mainloop()
