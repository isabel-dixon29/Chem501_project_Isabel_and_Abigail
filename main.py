"""Main file: 
Run to begin new experiment for collecting Temperature, humidity, gas, & CO2 readings.

Will save metadata & measured readings automatically."""

import paho.mqtt.subscribe as subscribe
import pandas as pd
import time
from datetime import datetime

from weather_api import WeatherAPI
from edit_metadata import MetadataInterface
from measurement_GUI import MeasurementInterface


MEASUREMENT_TITLES = ['aitemperature', 'aihumidity', 'aigas', 'aibco2']
HOSTNAME = "hostname.cloud"


def get_experiment_number():
    """Assigns an experiment number to a new experiment. Uses 'experiment_nr.txt'
    file to keep a updated record of the current number of experiments.
    
    Returns: experiment number (int)"""
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


# Open Measurement GUI
new_experiment = MeasurementInterface()
run_experiment = new_experiment.start_new_experiment

if run_experiment:
    # get experiment inputs from Measurement Interface
    sensor_location = new_experiment.location
    try:
        duration_hours = int(new_experiment.duration)
    except ValueError:
        raise ValueError("Invalid Duration, must input an integer")
    else:
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

    # save metadata
    MetadataInterface().save_metadata(metadata=template, ID=experiment_ID)

    topics = MEASUREMENT_TITLES
    data_table = []
    reading_nr = 0
    start_time = time.time()
    elapsed_time = 0

    # While loop to collect readings for duration
    while elapsed_time < duration_sec:
        try:
            reading_nr += 1
            data = []

            m = subscribe.simple(topics, hostname=HOSTNAME, retained=False, msg_count=len(topics))
            elapsed_time = time.time() - start_time

            for a in m:
                    data.append(float(a.payload))

            print("reading no.", reading_nr)
            print(data)
            time_left = (duration_sec - elapsed_time)/60
            print("time left", round(time_left, 1), "min")

            measurements = {}
            measurements["Time"] = round(elapsed_time, 1)
            measurements["Temperature"] = data[0]
            measurements["Humidity"] = data[1]
            measurements["Gas"] = data[2]
            measurements["CO2"] = data[3]
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
    new_experiment.save_popup(ID=experiment_ID)
