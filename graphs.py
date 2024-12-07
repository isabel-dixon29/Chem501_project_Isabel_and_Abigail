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

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.scatter(data_in1["Time"], data_in1[column_name], label="Kitchen Counter", color="black", s=10)
    ax2.scatter(data_in2["Time"], data_in2[column_name], label="Kitchen Window", color="#17becf", s=10)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax2.set_ylabel(y_label)
    ax1.set_title(f'Raw Data of {y_label}')
    ax2.set_title(f"Raw Data of {y_label}")
    filename = f'date-{column_name}-raw.png'
    fig1.legend(fontsize="8", loc="upper left")
    plt.savefig(filename, dpi=200, bbox_inches='tight')

    fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(12, 6))
    ax3.scatter(data_temperature_clean_1["Time"], data_temperature_clean_1[column_name], label='Kitchen Counter', color="purple", s=10)
    ax4.scatter(data_temperature_clean_2["Time"], data_temperature_clean_2[column_name], label="Kitchen Window", color="#ff7f0e", s=10)
    ax3.set_xlabel(x_label)
    ax3.set_ylabel(y_label)
    ax4.set_ylabel(y_label)
    ax3.set_title(f'Clean Data of {y_label}')
    ax4.set_title(f'Clean Data of {y_label}')
    if column_name == "CO2":
        ax3.set_ylim(1, 4000)
        ax4.set_ylim(1, 4000)
    filename = f'date-{column_name}-clean.png'
    fig2.legend(fontsize="8", loc="upper left")
    plt.savefig(filename, dpi=200, bbox_inches='tight')

    if column_name == "Humidity":
        window_size = 3
        y_no_zeros1 = np.where(data_in1[column_name] == 0, np.nan, data_in1[column_name])
        y_no_zeros2 = np.where(data_in2[column_name] == 0, np.nan, data_in2[column_name])

    else:
        window_size = 4
        y_no_zeros1 = np.where(data_in1[column_name] < 100, np.nan, data_in1[column_name])
        y_no_zeros2 = np.where(data_in2[column_name] < 100, np.nan, data_in2[column_name])
    rolling_avg1 = np.convolve(np.nan_to_num(y_no_zeros1, nan=np.nan), np.ones(window_size) / window_size, mode='valid')
    rolling_avg2 = np.convolve(np.nan_to_num(y_no_zeros2, nan=np.nan), np.ones(window_size) / window_size, mode='valid')

    rolling_avg3 = np.convolve(rolling_avg1, np.ones(window_size) / window_size, mode='valid')
    rolling_avg4 = np.convolve(rolling_avg2, np.ones(window_size) / window_size, mode='valid')

    rolling_avg5 = np.convolve(rolling_avg3, np.ones(window_size) / window_size, mode='valid')
    rolling_avg6 = np.convolve(rolling_avg4, np.ones(window_size) / window_size, mode='valid')

    rolling_avg7 = np.convolve(rolling_avg5, np.ones(window_size) / window_size, mode='valid')
    rolling_avg8 = np.convolve(rolling_avg6, np.ones(window_size) / window_size, mode='valid')

    rolling_avg9 = np.convolve(rolling_avg7, np.ones(window_size) / window_size, mode='valid')
    rolling_avg10 = np.convolve(rolling_avg8, np.ones(window_size) / window_size, mode='valid')

    fig3, (ax5, ax6) = plt.subplots(1, 2, figsize=(12, 6))
    ax5.scatter(data_in1["Time"][window_size*5-5:], rolling_avg9, label=f"{window_size}-Point Rolling Average (Kitchen Counter)", color='red', s=10)
    ax6.scatter(data_in2["Time"][window_size*5-5:], rolling_avg10, label=f"{window_size}-Point Rolling Average (Kitchen Window)", color='gold', s=10)
    ax5.set_xlabel(x_label)
    ax5.set_ylabel(y_label)
    ax6.set_ylabel(y_label)
    ax5.set_title(f'Rolling Average of {y_label}')
    ax6.set_title(f'Rolling Average of {y_label}')
    if column_name == "CO2":
        ax5.set_ylim(1, 4000)
        ax6.set_ylim(1, 4000)
    elif column_name == "Humidity":
        ax5.set_ylim(1, 70)
        ax6.set_ylim(1, 70)
    filename = f'date-ra-{column_name}.png'
    fig1.legend(fontsize="8", loc="upper left")
    plt.savefig(filename, dpi=200, bbox_inches='tight')

    plt.show()

data1 = read_csv("fill_in_csv_route")
data2 = read_csv("fill_in_csv_route")

dataplot(data1, data2, "Gas", "Time (s)", "Gas")
dataplot(data1, data2,  "Humidity", "Time (s)", "Humidity")
dataplot(data1, data2, "Temperature", "Time (s)", "Temperature (C)")
dataplot(data1, data2, "CO2", "Time (s)", "CO2")
