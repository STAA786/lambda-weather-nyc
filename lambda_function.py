import json
import os
import urllib.request
import urllib.error
import urllib.parse

def lambda_handler(event, context):
    try:
        api_key = os.environ.get('API_KEY')

        if not api_key:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({"error": "API_KEY not found"})
            }

        # Safe encoding of city name
        city = urllib.parse.quote("New York")
        country_code = "US"

        api_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city},{country_code}&appid={api_key}&units=imperial"
        )

        with urllib.request.urlopen(api_url, timeout=10) as response:
            weather_data = json.loads(response.read().decode())

        result = {
            "city": "New York, US",
            "temperature": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "humidity": weather_data["main"]["humidity"],
            "description": weather_data["weather"][0]["description"],
        }

        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            'body': json.dumps(result)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {"Content-Type": "application/json"},
            'body': json.dumps({
                "error": "Internal server error",
                "details": str(e),
                "status": "failed"
            })
        }
