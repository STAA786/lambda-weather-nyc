import json
import os
import urllib.request
import urllib.error

def lambda_handler(event, context):
    """
    AWS Lambda handler function to fetch current weather data for New York City.
    """

    try:
        # Get API key
        api_key = os.environ.get('API_KEY')

        if not api_key:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'API_KEY environment variable not configured',
                    'message': 'Please configure OpenWeatherMap API key in Lambda environment variables'
                })
            }

        # City vars
        city = "New York"
        country_code = "US"

        # Build URL
        api_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city},{country_code}&appid={api_key}&units=imperial"
        )

        # Call API
        with urllib.request.urlopen(api_url, timeout=10) as response:
            weather_data = json.loads(response.read().decode())

        # Extract fields
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        timestamp = weather_data['dt']

        weather_result = {
            'city': f"{city}, {country_code}",
            'temperature': f"{temperature}°F",
            'feels_like': f"{feels_like}°F",
            'temp_min': f"{temp_min}°F",
            'temp_max': f"{temp_max}°F",
            'humidity': f"{humidity}%",
            'description': description.title(),
            'timestamp': timestamp,
            'source': 'OpenWeatherMap API',
            'status': 'success'
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(weather_result, indent=2)
        }

    except urllib.error.HTTPError as http_err:
        error_code = http_err.code
        error_message = 'API request failed'

        if error_code == 401:
            error_message = 'Invalid API key'
        elif error_code == 404:
            error_message = 'City not found'
        elif error_code == 429:
            error_message = 'API rate limit exceeded'

        return {
            'statusCode': error_code,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': error_message, 'error_code': error_code, 'status': 'failed'})
        }

    except urllib.error.URLError as url_err:
        return {
            'statusCode': 503,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'error': 'Network connectivity issue',
                'details': str(url_err),
                'status': 'failed'
            })
        }

    except KeyError as key_err:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'error': 'Invalid API response format',
                'missing_key': str(key_err),
                'status': 'failed'
            })
        }

    except Exception as general_err:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(general_err),
                'status': 'failed'
            })
        }
