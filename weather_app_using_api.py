# Weather App
# S
# Built with Python | Uses API to display the weather info just by providing the place

import requests
#Converts place name to latitude and longitude
def get_coordinates(city):
    """
        Converts city name to latitude and longitude
        using Open-Meteo Geocoding API.
        Returns (lat, lon) or (None, None) if city not found.
        """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("No internet connection!")
        return None, None
    data = response.json()
    if "results" not in data:
        return None, None
    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]
    return lat, lon
#Displays weather data for given latitude and longitude
def get_weather(lat, lon):
    """
    Fetches current weather data for given coordinates
    using Open-Meteo Forecast API.
    Returns weather dictionary or None if request fails.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("No internet connection!")
        return None, None
    data = response.json()
    return data["current_weather"]
#Displays weather code in readable format
def get_condition(code):
    """
        Converts Open-Meteo weather code (integer)
        to a human-readable weather condition string.
        Weather codes reference: https://open-meteo.com/en/docs
        """
    if code == 0:
        return "Clear sky"
    elif code <= 3:
        return "Partly cloudy"
    elif code <= 67:
        return "Rainy "
    elif code <= 77:
        return "Snowy "
    else:
        return "Thunderstorm "

def main():
    city_name = input("Enter city name: ")
    lat, lon = get_coordinates(city_name)
    if lat is None:
        print("City not found!")
        return
    weather= get_weather(lat, lon)
    temp = weather["temperature"]
    wind = weather["windspeed"]
    code = weather["weathercode"]
    print(f"Temperature: {temp}°C")
    print(f"Wind Speed : {wind} km/h")
    print(f"Condition  : {get_condition(code)}")

main()