from dotenv import load_dotenv
import os
from bot import CustomerServiceBot

if __name__ == "__main__":
    load_dotenv()
    
    url = 'your_url'
    training_data_dir = 'your_training_data_dir'

    bot_token = os.getenv('MY_BOT_TOKEN')
    gemini_api = os.getenv('GEMINI_API')

    bot = CustomerServiceBot(bot_token, gemini_api, url, training_data_dir)
    bot.run()