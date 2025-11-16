import json
import os
import urllib.request
import urllib.error

def lambda_handler(event, context):
    """
    AWS Lambda handler function to fetch current weather data for New York City.
    
    This function integrates with OpenWeatherMap API to retrieve real-time
    temperature, humidity, and weather conditions for NYC.
    
    Args:
        event (dict): API Gateway event object containing request information
        context (object): Lambda context object with runtime information
    
    Returns:
        dict: API Gateway compatible response with status code, headers, and body
        
    Environment Variables:
        API_KEY (str): OpenWeatherMap API authentication key
    """
    
    try:
        # Retrieve API key from Lambda environment variables
        api_key = os.environ.get('API_KEY')
        
        # Validate API key exists
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
        
        # Define target city parameters
        city = "New York"
        country_code = "US"
        
        # Construct OpenWeatherMap API URL
        # Using imperial units for Fahrenheit temperature
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=imperial"
        
        # Make HTTP request to OpenWeatherMap API
        with urllib.request.urlopen(api_url, timeout=10) as response:
            # Parse JSON response
            weather_data = json.loads(response.read().decode())
        
        # Extract relevant weather information
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        temp_min = weather_data['main']['temp_min']
        temp_max = weather_data['main']['temp_max']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        timestamp = weather_data['dt']
        
        # Construct formatted response object
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
        
        # Return successful response
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
        # Handle HTTP errors from OpenWeatherMap API
        error_code = http_err.code
        error_message = 'API request failed'
        
        if error_code == 401:
            error_message = 'Invalid API key - Please verify your OpenWeatherMap API key'
        elif error_code == 404:
            error_message = 'City not found in OpenWeatherMap database'
        elif error_code == 429:
            error_message = 'API rate limit exceeded - Please try again later'
        
        return {
            'statusCode': error_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': error_message,
                'error_code': error_code,
                'status': 'failed'
            })
        }
    
    except urllib.error.URLError as url_err:
        # Handle network connectivity issues
        return {
            'statusCode': 503,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Network connectivity issue',
                'message': 'Unable to reach OpenWeatherMap API',
                'details': str(url_err),
                'status': 'failed'
            })
        }
    
    except KeyError as key_err:
        # Handle missing keys in API response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Invalid API response format',
                'message': 'OpenWeatherMap API returned unexpected data structure',
                'missing_key': str(key_err),
                'status': 'failed'
            })
        }
    
    except Exception as general_err:
        # Handle all other unexpected errors
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred',
                'error_type': type(general_err).__name__,
                'error_details': str(general_err),
                'status': 'failed'
            })
        }
