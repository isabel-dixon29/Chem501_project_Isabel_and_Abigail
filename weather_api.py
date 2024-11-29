"""File that contains the method to access Open Weather app's weather data.

Classes: WeatherAPI
"""
import os
import requests

class WeatherAPI:
    """Contains methods to access Open Weather App's weather data.

    Requirements: API key

    Methods: get_weather()
    """

    API_KEY = 'Openweatherapp_API_KEY'
    #API_KEY = os.environ.get(__key=OWM_API_KEY)
    PARAMETERS = {
                'appid':API_KEY,
                'cnt':1,
    }

    API_3_HOUR_CALL = 'https://api.openweathermap.org/data/2.5/forecast'

    def get_weather(lat=-2.972391, lon=53.407599):
        """Uses open weather map to get the weather description of the hour 
        following the start of the experiment.

        Parameters: lattitude (float), longitude (float)

        Returns: Weather description for the location of the experiment (str)
        """
        parameters = WeatherAPI.PARAMETERS
        parameters["lat"] = lat
        parameters["lon"] = lon

        response = requests.get(url=WeatherAPI.API_3_HOUR_CALL, params=parameters)
        response.raise_for_status()
        data = response.json()

        weather_data = data['list'][0]['weather'][0]
        weather_description = weather_data['description']
        return weather_description
