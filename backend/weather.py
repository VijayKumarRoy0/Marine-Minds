import requests
import datetime

WEATHERAPI_KEY = "56a716adc0844f0488a171614250209"

def get_last_hours_weather(city, hours=2):
    now = datetime.datetime.utcnow()
    date_str = now.strftime("%Y-%m-%d")

    url = f"http://api.weatherapi.com/v1/history.json?key={WEATHERAPI_KEY}&q={city}&dt={date_str}"
    res = requests.get(url).json()

    if "forecast" not in res:
        return {"error": res}

    current_hour = now.hour
    last_hours = []

    for i in range(hours):
        h = current_hour - i
        if h < 0:
            continue
        hour_data = res["forecast"]["forecastday"][0]["hour"][h]
        last_hours.append({
            "time": hour_data["time"],
            "condition": hour_data["condition"]["text"],
            "rain_mm": hour_data["precip_mm"],
            "temp_c": hour_data["temp_c"]
        })

    return last_hours

# ----------- Test -----------
if __name__ == "__main__":
    city = "rajpura"   # city name direct daal
    weather = get_last_hours_weather(city, hours=2)
    print("Last 2 hours weather:")
    for w in weather:
        print(w)
