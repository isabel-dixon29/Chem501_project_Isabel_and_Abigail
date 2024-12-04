import matplotlib as mpl
from pandas import read_csv
import numpy as np
mpl.rcParams['axes.formatter.useoffset'] = False
import matplotlib.pyplot as plt

def dataplot(data_in1, data_in2, column_name, x_label, y_label):

    lower_bound_1 = data_in1[column_name].quantile(0.0001)
    upper_bound_1 = data_in1[column_name].quantile(0.9999)
    lower_bound_2 = data_in2[column_name].quantile(0.0001)
    upper_bound_2 = data_in2[column_name].quantile(0.9999)

    data_temperature_clean_1 = data_in1[(data_in1[column_name] > lower_bound_1) & (data_in1[column_name] < upper_bound_1)]
    data_temperature_clean_2 = data_in2[(data_in2[column_name] > lower_bound_2) & (data_in2[column_name] < upper_bound_2)]

    fig1, ax1 = plt.subplots()
    ax1.scatter(data_in1["Time"], data_in1[column_name], label="m2n2 Data", color="#17becf")
    ax1.scatter(data_in2["Time"], data_in2[column_name], label="m1n1 Data", color="#ff7f0e")
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.set_title(f'Raw Data of {y_label}')
    filename = f'date-{column_name}.png'
    plt.legend()
    plt.savefig(filename, dpi=200, bbox_inches='tight')

    fig2, ax2 = plt.subplots()
    ax2.scatter(data_temperature_clean_1["Time"], data_temperature_clean_1[column_name], label='m2n2 Data', color="#e377c2")
    ax2.scatter(data_temperature_clean_2["Time"], data_temperature_clean_2[column_name], label="m1n1 Data", color="#ff7f0e")
    ax2.set_xlabel(x_label)
    ax2.set_ylabel(y_label)
    ax2.set_title(f'Clean Data of {y_label}')
    if column_name == "CO2":
        ax2.set_ylim(0, 4000)
    filename = f'date-{column_name}-clean.png'
    plt.legend()
    plt.savefig(filename, dpi=200, bbox_inches='tight')

    plt.show()

data1 = read_csv("fill_in_csv_route")
data2 = read_csv("fill_in_csv_route")

dataplot(data1, data2, "Gas", "Time (s)", "Gas")
dataplot(data1, data2,  "Humidity", "Time (s)", "Humidity")
dataplot(data1, data2, "Temperature", "Time (s)", "Temperature (C)")
dataplot(data1, data2, "CO2", "Time (s)", "CO2")
