import requests
import urllib

API_KEY = "ffc03b88a036ec41ba303e70aef02177"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

def getweather(city):
    params = {
        "q": city,
        "appid": API_KEY
    }

    url = BASE_URL + urllib.parse.urlencode(params)

    req = requests.get(url)
    print(req.text)