import paho.mqtt.subscribe as subscribe
import pandas as pd
import datetime as dt

NUM_OF_READINGS = 5
MEASUREMENT_TITLES = ["aitime", "aitemperature", "aihumidity", "aigas", "aico2"]

# Create filename id:
date_now = dt.datetime.now()
date_str = date_now.strftime('%d%m%Y')
nicla_ID = "n1"
mkr_ID = "m1"
filename_csv = mkr_ID + nicla_ID + date_str

topics = MEASUREMENT_TITLES
data_table = []

for _ in range(0, (NUM_OF_READINGS+1), 1):
    data = []
    m = subscribe.simple(topics, hostname="test.mosquitto.org", retained=False, msg_count=len(topics))
    for a in m:
            data.append(float(a.payload))

    measurements = {}
    measurements["time"] = data[0]
    measurements["temperature"] = data[1]
    measurements["humidity"] = data[2]
    measurements["gas"] = data[3]
    measuremnents["co2"] = data[4]

    data_table.append(measurements)

# data_table to csv
df = pd.DataFrame(data_table)
df.to_csv(f"measurements/{filename_csv}.csv", index=False)

print("CSV file has been saved successfully.")
