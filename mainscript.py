import requests
import telegram
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

TOKEN = "6366204223:AAHQWICNWDitE3bvB8nigMjDiMzfq_cIWmU"

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

CHOOSING, TYPING_REPLY = range(2)

# Placeholder function to fetch tech news headlines using News API
def fetch_tech_news():
    news_api_key = "989b60d41f614ce1ac74fa9eefd1c5d0"
    news_api_url = "https://newsapi.org/v2/top-headlines"
    news_params = {
        "country": "us",
        "category": "technology",
        "apiKey": news_api_key,
    }
    
    response = requests.get(news_api_url, params=news_params)
    news_data = response.json()

    news_headlines = ""
    for article in news_data.get("articles", []):
        news_headlines += f"- [{article['title']}]({article['url']})\n"

    return news_headlines

# Placeholder function to fetch a random joke
def fetch_random_joke():
    response = requests.get("https://v2.jokeapi.dev/joke/Any?type=single")
    joke_data = response.json()

    if "joke" in joke_data:
        return joke_data["joke"]
    else:
        return "I couldn't fetch a joke at the moment. Try again later."

# Placeholder function to fetch a random inspirational quote
def fetch_random_quote():
    response = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
    quote_data = response.json()

    if "quoteText" in quote_data and "quoteAuthor" in quote_data:
        return f'"{quote_data["quoteText"]}" - {quote_data["quoteAuthor"]}'
    else:
        return "I couldn't fetch a quote at the moment. Try again later."

def fetch_weather(city_name):
    api_key = "183e7ff9b493bc983128603ec112b849"  # Replace with your actual OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # You can change this to "imperial" if you prefer Fahrenheit
    }
    
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    
    if response.status_code == 200:
        main_info = weather_data["main"]
        weather_description = weather_data["weather"][0]["description"]
        temperature = main_info["temp"]
        humidity = main_info["humidity"]
        
        return {
            "description": weather_description,
            "temperature": temperature,
            "humidity": humidity
        }
    else:
        return None

# Command handler for /start
def start(update: telegram.Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! I'm your chatbot. Type /help to see available commands.")

# Command handler for /help
def help_command(update: telegram.Update, context: CallbackContext) -> None:
    help_text = (
        "Here are the available commands:\n"
        "/start - Start a new conversation\n"
        "/help - Display this help message\n"
        "/joke - Get a random joke\n"
        "/quote - Get an inspirational quote\n"
        "/cancel - Cancel the current conversation\n"
        "/news - Get the latest tech news\n"
    )
    update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

# Command handler for /joke
def joke(update: telegram.Update, context: CallbackContext) -> None:
    joke_text = fetch_random_joke()
    update.message.reply_text(joke_text)

# Command handler for /quote
def quote(update: telegram.Update, context: CallbackContext) -> None:
    quote_text = fetch_random_quote()
    update.message.reply_text(quote_text)

# Command handler for /news
def tech_news(update: telegram.Update, context: CallbackContext) -> None:
    news_headlines = fetch_tech_news()
    update.message.reply_text(news_headlines, parse_mode=ParseMode.MARKDOWN)

# Command handler for /weather
def weather(update: telegram.Update, context: CallbackContext) -> None:
    update.message.reply_text("Please enter the city name for weather information.")
    return CHOOSING

# Function to handle user's reply to /weather command
def received_information(update: telegram.Update, context: CallbackContext) -> int:
    user_input = update.message.text
    weather_info = fetch_weather(user_input)

    if weather_info:
        description = weather_info["description"]
        temperature = weather_info["temperature"]
        humidity = weather_info["humidity"]

        response = (
            f"Weather in {user_input}: {description}\n"
            f"Temperature: {temperature}°C\n"
            f"Humidity: {humidity}%"
        )
    else:
        response = "Weather information not available."

    update.message.reply_text(response)
    return ConversationHandler.END

# Placeholder function to handle cancel command
def cancel(update: telegram.Update, context: CallbackContext) -> int:
    update.message.reply_text("Conversation has been cancelled.")
    return ConversationHandler.END

# Add conversation handler for weather command
weather_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("weather", weather)],
    states={
        CHOOSING: [MessageHandler(Filters.text & ~Filters.command, received_information)]
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

# Add handlers to the dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('joke', joke))
dispatcher.add_handler(CommandHandler('quote', quote))
dispatcher.add_handler(CommandHandler('news', tech_news))
#weather function is not completed yet so the code for it has been removed 
dispatcher.add_handler(CommandHandler('weather', weather))
dispatcher.add_handler(CommandHandler('cancel', cancel))
dispatcher.add_handler(weather_conv_handler)

# Start the bot
if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
