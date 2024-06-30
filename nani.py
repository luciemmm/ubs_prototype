
import requests

def fetch_weather():
    api_url = 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc'
    
    try:
        response = requests.get(api_url, headers={"Accept": "application/json"})
        
        if response.status_code != 200:
            raise Exception('Network response was not ok')
        
        data = response.json()
        print(data["icon"])
        
    except Exception as error:
        print("There was a problem with the fetch operation:", error)

# Call the function to fetch and print the weather data
fetch_weather()