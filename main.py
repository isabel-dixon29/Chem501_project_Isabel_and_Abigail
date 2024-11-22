import paho.mqtt.subscribe as subscribe
import pandas as pd
import time
from datetime import datetime

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


# Create filename id:
date_now = datetime.now()
date_str = date_now.strftime('%d%m%Y')
nicla_ID = "n1"
mkr_ID = "m1"
exp_nr = str(get_experiment_number())
filename_csv = mkr_ID + nicla_ID + date_str + "-" + exp_nr


topics = MEASUREMENT_TITLES
data_table = []
start_time = time.time()
for _ in range(0, (NUM_OF_READINGS + 1), 1):
    data = []
    m = subscribe.simple(topics, hostname="pf-eveoxy0ua6xhtbdyohag.cedalo.cloud", retained=False, msg_count=len(topics))
    elapsed_time = time.time() - start_time

    for a in m:
            data.append(float(a.payload))

    print("reading no.", _)
    print(data)
    print(elapsed_time)

    measurements = {}
    measurements["time"] = round(elapsed_time, 1)
    measurements["temperature"] = data[1]
    measurements["humidity"] = data[2]
    measurements["gas"] = data[3]
    measurements["co2"] = data[4]

    data_table.append(measurements)

# data_table to csv
df = pd.DataFrame(data_table)
df.to_csv(f"measurements/{filename_csv}.csv", index=False)

print("CSV file has been saved successfully.")
