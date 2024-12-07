# Chem501_project_Isabel_and_Abigail
<h1>Overview</h1>
<p>
The goal of our project is to determine how the air quality of a living space is affected by a shared kitchen. We have designed a tool to take measurements of temperature, humidity, gas, and CO2 over multiple hours in two locations. This program will automatically assign an experiment ID and create metadata for each experiment, to aid us in combining all data into an SQL database and plotting data points using matplotlib.
</p>

<h1>Description</h1>
<p>
Program to measure the air quality in an environment wirelessly: Use of Arduino Nicla sense me Sensor (& BSEC Sensor) and MKR to measure 1 reading per second of four values, temperature, humidity, gas, and CO2. Python file is used to collect measured values for initial storage in CSV file, metadata is created automatically and stored in a json file.
</p>

<h1>Requirements</h1>
<ul>
<li>Arduino sensors: Nicla Sense Me, and MKR WIFI 1010
</li>
<li>Python Packages: paho-mqtt, pandas, requests, sqllite, tkinter, numpy, matplotlib
</li>
<li>Open Weather App API Key (free)
</li>
</ul>

<h1>What's New</h1>
<p>
We have now added a module (edit_metadata.py) that allows users to search, update, & save metadata of a completed experiment using the experiment ID with a GUI!
</p>

