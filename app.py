from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests

# Flask app
app = Flask(__name__)
CORS(app)

# Database setup (SQLite for now)
DATABASE_URL = "sqlite:///database.db"  # You can change to PostgreSQL with appropriate URL
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    user_message = Column(String, nullable=False)
    bot_reply = Column(String, nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Weather API settings
API_KEY = "e19fddda334aea4ce4290f8daa9334f7"  # Replace with your actual OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to get weather data from OpenWeatherMap API
def get_weather(city_name):
    complete_url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric"
    print(f"Weather API URL: {complete_url}")  # Log URL for debugging

    response = requests.get(complete_url)

    # Log response status and data for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Data: {response.text}")

    if response.status_code == 200:
        data = response.json()
        main = data["main"]
        weather = data["weather"][0]

        temp = main["temp"]
        description = weather["description"]

        return f"The weather in {city_name} is {description} with a temperature of {temp}°C."
    else:
        return "Sorry, I couldn't fetch the weather data right now."

# Routes
@app.route('/chat', methods=['POST'])
def chat():
    # Handle POST request for sending a message
    data = request.get_json()
    user_message = data.get('message')

    # Weather request logic
    if "weather" in user_message.lower():
        # Extract city name from the user message
        city_name = user_message.lower().split("weather in")[-1].strip()
        print(f"City Name Extracted: {city_name}")  # Log the extracted city name
        
        # Call the get_weather function to fetch weather data
        bot_reply = get_weather(city_name)
    else:
        # Simple bot response logic for non-weather related messages
        if "hello" in user_message.lower():
            bot_reply = "Hello! How can I help you today?"
        else:
            bot_reply = "I'm sorry, I didn't understand that."

    # Save to database
    chat_entry = Chat(user_message=user_message, bot_reply=bot_reply)
    session.add(chat_entry)
    session.commit()

    return jsonify({"reply": bot_reply})

@app.route('/chat', methods=['GET'])
def get_chat_history():
    # Handle GET request for fetching the chat history
    chats = session.query(Chat).all()
    chat_history = [{"user_message": chat.user_message, "bot_reply": chat.bot_reply} for chat in chats]
    
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(debug=True)
