import paho.mqtt.subscribe as subscribe
import pandas as pd
import time
import json
from datetime import datetime

from weather_api import WeatherAPI
from edit_metadata import MetadataInterface


NUM_OF_READINGS = 5
MEASUREMENT_TITLES = ['aitime', 'aitemperature', 'aihumidity', 'aigas', 'aibco2']


def get_experiment_number():
    try:
        # Try to open the file and read the current experiment number
        with open(file="experiment_nr.txt", mode='r') as file:
            experiment_number = int(file.read())
    except FileNotFoundError:
        experiment_number = 1
    finally:
        with open(file="experiment_nr.txt", mode='w') as file:
            nr = experiment_number + 1
            file.write(str(nr))
    return experiment_number


# Get experiment sepcs
sensor_location = input("Location of sensor: ")
duration_hours = int(input("Number of HOURS to collect readings: "))
duration_sec = duration_hours * 3600

# Create experiment id
date_now = datetime.now()
date_str = date_now.strftime('%d%m%Y')
nicla_ID = "n1"
mkr_ID = "m1"
exp_nr = str(get_experiment_number())
experiment_ID = mkr_ID + nicla_ID + date_str + "-" + exp_nr
filename_csv = experiment_ID + ".csv"

# create metadata
template = {experiment_ID:{
         "NiclaID": nicla_ID,
         "MKRID": mkr_ID,
         "Location": sensor_location,
         "Date_Start": date_now.strftime('%d-%m-%Y'),
         "Time_Start": date_now.strftime('%H:%M'),
         "Duration": duration_hours,
         "Weather_Description": WeatherAPI.get_weather(),
         }}

# template to data
MetadataInterface().save_metadata(metadata=template)

topics = MEASUREMENT_TITLES
data_table = []
reading_nr = 0

# Begin program
input("Press [ENTER] to proceed")

start_time = time.time()
elapsed_time = 0
while elapsed_time < duration_sec:
    try:
        reading_nr += 1
        data = []
        m = subscribe.simple(topics, hostname="pf-eveoxy0ua6xhtbdyohag.cedalo.cloud", retained=False, msg_count=len(topics))
        elapsed_time = time.time() - start_time

        for a in m:
                data.append(float(a.payload))

        print("reading no.", reading_nr)
        print(data)
        time_left = (duration_sec - elapsed_time)/60
        print("time left", round(time_left, 1), "min")

        measurements = {}
        measurements["Time"] = round(elapsed_time, 1)
        measurements["Temperature"] = data[1]
        measurements["Humidity"] = data[2]
        measurements["Gas"] = data[3]
        measurements["CO2"] = data[4]

        data_table.append(measurements)

    except Exception as e:
        # Save current data
        print("\nError occured, saving current data to csv file.")
        df = pd.DataFrame(data_table)
        df.to_csv(f"measurements/{filename_csv}", index=False)
        print("CSV file has been saved successfully.")
        # Print error message
        print(f"\n{e}\n")


# data_table to csv
df = pd.DataFrame(data_table)
df.to_csv(f"measurements/{filename_csv}", index=False)
print("CSV file has been saved successfully.")
