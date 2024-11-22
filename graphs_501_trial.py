import matplotlib as mpl
from pandas import read_csv
import numpy as np
mpl.rcParams['axes.formatter.useoffset'] = False
import matplotlib.pyplot as plt

def dataplot(data_in, column_name, x_label, y_label):

    lower_bound_2 = data_in['gas_y'].quantile(0.0001)
    upper_bound_2 = data_in['gas_y'].quantile(0.9999)
    lower_bound_1 = data_in['gas_x'].quantile(0.0001)
    lower_bound_1 - data_in['gas_x'].quantile(0.9999)

    data_temperature_clean_2 = data_in[(data_in["gas_y"] > lower_bound_2) & (data_in["gas_y"] < upper_bound_2)]
    data_temperature_clean_1 = data_in[(data_in["gas_x"] > lower_bound_2) & (data_in["gas_x"] < upper_bound_2)]
    clean_data_merged = pd.merge(data_temperature_clean_1, data_temperature_clean_2, on='reading number', how='inner')

    fig1, ax1 = plt.subplots()
    ax1.scatter(data_merged['reading number'], data_merged['gas_x'], label='m2n2 Data', color='#17becf')
    ax1.scatter(data_merged['reading number'], data_merged['gas_y'], label='m1n1 Data', color='#ff7f0e')
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.set_title(f'Raw Data of {y_label}')
    filename = f'trial-{column_name}.png'
    plt.legend()
    plt.savefig(filename, dpi=200, bbox_inches='tight')

    fig2, ax2 = plt.subplots()
    ax2.scatter(data_temperature_clean_2["reading number"], data_temperature_clean_2['gas_y'], label='m1n1 Data', color="#9467bd")
    ax2.scatter(data_temperature_clean_1["reading number"], data_temperature_clean_1['gas_x'], label='m2n2 Data', color="#e377c2")
    ax2.set_xlabel(x_label)
    ax2.set_ylabel(y_label)
    ax2.set_title(f'Clean Data of {y_label}')
    filename = f'trial-{column_name}-clean.png'
    plt.legend()
    plt.savefig(filename, dpi=200, bbox_inches='tight')

    plt.show()

data1 = read_csv("/Users/44738/Documents/GitHub/desktop-tutorial/comp501/measurements/m2n220112024-1.csv")
data2 = read_csv("/Users/44738/Documents/GitHub/desktop-tutorial/comp501/measurements/m1n120112024-1.csv")
data_merged = pd.merge(data1, data2, on='reading number', how='inner')

dataplot(data_merged, "gas", "Time (s)", "Gas (Pa)")
dataplot(data_merged, "humidity", "Time (s)", "Humidity")