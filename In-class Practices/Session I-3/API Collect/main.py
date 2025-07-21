import requests

#location in beijing
latitude = 39.799316615492074
longitude = 116.40726087741393

api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,windspeed_10m"

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()

    current_data = data.get('current')
    if current_data:
        time = current_data.get('time')
        temperature = current_data.get('temperature_2m')
        windspeed = current_data.get('windspeed_10m')
        print(f"Time: {time}")
        print(f"Temperature: {temperature}°C")
        print(f"Windspeed: {windspeed} m/s")
    else:
        print("Current data not found in the response.")
else:
    print(f"Error: Unable to fetch data from API. Status code: {response.status_code}")