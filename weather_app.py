import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                              QPushButton, QLineEdit, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Import API key from config file
try:
    from config import OPENWEATHER_API_KEY

except ImportError:
    OPENWEATHER_API_KEY = None

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # CREATING LABELS
        self.city_label = QLabel("Enter the city:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather 🔍", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
    

    def initUI(self):
        self.setWindowTitle("Weather App ⛅")
        self.setGeometry(100, 100, 400, 500)

        # Set window icon
        self.setWindowIcon(QIcon("luffy_wallpaper.jpeg"))
        
        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        # Center align text
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # Set object names for styling
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        # Apply styles
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton{
                font-size: 30px;
                font-weight: 10;
                background-color: #a2d7fc;
            }
            QPushButton:hover{
                background-color: #8cc5f0;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 60px;
            }
        """)
        
        # Connect button click and Enter key press
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)
    
    def get_weather(self):
        # Check if API key is configured
        if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "your_api_key_here":
            self.display_error("API Key not configured!\n\nPlease add your API key\nto config.py file.")
            return
        
        # Validate input
        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city name")
            return
        
        # Clear previous results
        self.clear_results()
        
        # API call with metric units (Celsius)
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.display_weather(data)
            
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error(f"{response.status_code} Bad Request.\nPlease check your input.")
                case 401:
                    self.display_error(f"{response.status_code} Unauthorized.\nInvalid API key.")
                case 403:
                    self.display_error(f"{response.status_code} Forbidden.\nAccess is denied.")
                case 404:
                    self.display_error(f"{response.status_code} Not Found.\nCity not found.")
                case 429:
                    self.display_error(f"{response.status_code} Too Many Requests.\nAPI rate limit exceeded.")
                case 500:
                    self.display_error(f"{response.status_code} Internal Server Error.\nPlease try again later.")
                case 502:
                    self.display_error(f"{response.status_code} Bad Gateway.\nInvalid response from server.")
                case 503:
                    self.display_error(f"{response.status_code} Service Unavailable.\nServer is down.")
                case 504:
                    self.display_error(f"{response.status_code} Gateway Timeout.\nNo response from the server.")
                case _:
                    self.display_error(f"HTTP error occurred.\n{response.status_code}")
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\n\nCheck your internet connection.")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\n\nThe request timed out.")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects\n\nCheck the URL.")
        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n\n{req_error}")
    
    
    def clear_results(self):
        self.temperature_label.clear()
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_error(self, message):
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.emoji_label.clear()
        self.description_label.clear()
    
    def display_weather(self, data):
        # Temperature is already in Celsius due to units=metric
        temp_C = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        self.temperature_label.setText(f"{temp_C:.0f}°C")
        self.temperature_label.setStyleSheet("font-size: 75px;")
        self.description_label.setText(weather_description.title())
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
    
    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "☔"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 781:
            return "🌫️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "☀️"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())