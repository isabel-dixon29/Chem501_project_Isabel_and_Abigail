import paho.mqtt.subscribe as subscribe
import pandas as pd
import datetime as dt

NUM_OF_READINGS = 50
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
date_now = dt.datetime.now()
date_str = date_now.strftime('%d%m%Y')
nicla_ID = "n1"
mkr_ID = "m1"
exp_nr = str(get_experiment_number())
filename_csv = mkr_ID + nicla_ID + date_str + "-" + exp_nr

topics = MEASUREMENT_TITLES
data_table = []
print("begining for loop")
for _ in range(0, (NUM_OF_READINGS+1), 1):
    data = []
    m = subscribe.simple(topics, hostname="pf-eveoxy0ua6xhtbdyohag.cedalo.cloud", retained=False, msg_count=len(topics))
    print("m subscribed")
    for a in m:
            data.append(float(a.payload))
    print(data)

    measurements = {}
    measurements["time"] = data[0]
    measurements["temperature"] = data[1]
    measurements["humidity"] = data[2]
    measurements["gas"] = data[3]
    measurements["co2"] = data[4]

    data_table.append(measurements)

# data_table to csv
df = pd.DataFrame(data_table)
df.to_csv(f"measurements/{filename_csv}.csv", index=False)

print("CSV file has been saved successfully.")
