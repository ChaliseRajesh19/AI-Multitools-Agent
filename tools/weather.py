"""Weather lookup tool using wttr.in."""
import requests
def getweather(location):
    url = f"http://wttr.in/{location}?format=%l:+%C+%t+Humidity:%h"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return f"Could not retrieve weather for {location}."