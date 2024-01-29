
import os
from config import URL, DB_PATH
from script.etl import CheeseScrapping
from script.computation import CheeseMeasure
from config import ROOT, CHEESE_ODS_TABLE
import matplotlib as plt
from tkinter import Tk, Label, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd


def cheese_scrapping():

    cheese_scrapping = CheeseScrapping(URL)
    cheese_extraction = cheese_scrapping.extract()
    cheese_transformation = cheese_scrapping.transform(cheese_extraction)
    
    return cheese_scrapping.load(DB_PATH, CHEESE_ODS_TABLE, cheese_transformation)


def launch_etl_testing():

    os.system(f"python -m pytest --csv cache/test-result.csv")
    result = pd.read_csv('cache/test-result.csv')
    mask = result['status'] == 'passed'

    return (result.loc[mask].shape[0] / result.shape[0])*100


scrapping = CheeseScrapping(URL)
extraction = scrapping.extract()
transformation = scrapping.transform(extraction)
final_dataframe = scrapping.load(DB_PATH, CHEESE_ODS_TABLE, transformation)
computation = CheeseMeasure(final_dataframe)
last_refresh_date = final_dataframe['update_date'].max()
accuracy = launch_etl_testing()

window = Tk()
window.title('Cheese APP')
plt.use('TkAgg')
fig = Figure(figsize=(6, 6))
ax = fig.add_subplot(111)
computation.countby_families(ax)

refresh_label = Label(window, text=f"Dernier rafraichissement de données : {last_refresh_date}")
refresh_label.pack()

quality_label = Label(window, text=f"Qualité des données : {accuracy} %")
quality_label.pack()

refresh_button = Button(window, text='Actualiser les données', command=cheese_scrapping)
refresh_button.pack()

quality_button = Button(window, text='Exécution des tests', command=launch_etl_testing)
quality_button.pack()

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()
canvas.draw()

window.mainloop()
