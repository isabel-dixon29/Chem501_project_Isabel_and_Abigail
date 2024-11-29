# --- UNDER CONSTRUCTION --- #

import json
import tkinter as tk

def search_experiment():
    try:
        with open(file="metadata.json", mode="r") as json_file:
            content = json.load(json_file)
    except FileNotFoundError as e:
        print("There is no metadata yet.")
        return None
    
    try:
        exp_ID = exp_input.get().strip()
        exp_data = content[exp_ID]
    except KeyError:
        print("Invalid Experiment ID.")
    else:
        row_c = 1
        for key, value in exp_data.items():
            label = tk.Label(text=f"{key}: ")
            label.grid(column=0, row=row_c)
            button = tk.Entry()
            button.grid(column=1, row=row_c)
            button.insert(0, value)
            row_c += 1   

window = tk.Tk()
window.title("Search Metadata")
window.geometry("500x500")

exp_label = tk.Label(text="Metadata for experiment: ", font=('Arial',12,'normal'))
exp_label.grid(column=0, row=0)

exp_input = tk.Entry()
exp_input.grid(column=1, row=0)

exp_button = tk.Button(text="Search", font=('Arial',12,'normal'), command=search_experiment)
exp_button.grid(column=2, row=0)

window.mainloop()
