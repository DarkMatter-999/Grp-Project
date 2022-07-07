import requests
import urllib
import json
import time

API_KEY = "ffc03b88a036ec41ba303e70aef02177"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"


class Weather:
    def __init__(self):
        self.city_cache = {}

    def getweather(self, city):

        city = city.lower()
        print(self.city_cache)

        if city not in self.city_cache.keys():
            return self.getweather_notime(city)

        elif time.time() - self.city_cache[city]["time"] > 3600:
            return self.getweather_notime(city)

        else:
            return self.city_cache[city.lower()]


    def getweather_notime(self, city):
        params = {
                "q": city,
                "appid": API_KEY
            }

        url = BASE_URL + urllib.parse.urlencode(params)

        req = requests.get(url)

        data = json.loads(req.text)

        if data["cod"] == "404":
            return False

        impdata = {"weather": data['weather'][0]['main'], "icon" :data['weather'][0]['icon'], "temp": data['main']['feels_like'], "time": time.time()}

        self.city_cache[city.lower()] = impdata

        return self.city_cache[city.lower()]