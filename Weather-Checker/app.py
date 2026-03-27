from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Your key - keep it here only
API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            # Using the API_KEY variable and https for better security
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
            
            try:
                response = requests.get(url).json()
                
                if response.get('cod') == 200:
                    weather_data = {
                        'city': response['name'],
                        'temp': response['main']['temp'],
                        'desc': response['weather'][0]['description'],
                        'icon': response['weather'][0]['icon'],
                        'humidity': response['main']['humidity']
                    }
                else:
                    # This will show you the ACTUAL error from the API (e.g., 'Invalid API key')
                    error_msg = response.get('message', 'City not found')
                    weather_data = {'error': error_msg.capitalize()}
            except Exception as e:
                weather_data = {'error': 'Could not connect to the weather service.'}

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)