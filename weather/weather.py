import requests

def get_weather(city_name, api_key):
    """Fetch weather data for a given city."""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        
        # Extract weather information
        city = data['name']
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        # Display the weather details
        print(f"\nWeather in {city}:")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {weather}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
    except KeyError:
        print("Invalid city name or API key.")

if __name__ == "__main__":
    print("Welcome to the Weather App!")
    city = input("Enter the city name: ").strip()
    api_key = "f89e44c661844b9e95c95ece33a83bd7"  # Use your API key here
    get_weather(city, api_key)
