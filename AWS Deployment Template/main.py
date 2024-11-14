from dotenv import load_dotenv
import os
from bot import CustomerServiceBot

if __name__ == "__main__":
    load_dotenv()
    
    url = 'your_url'
    s3_bucket = os.getenv('AWS_S3_BUCKET') #training data stored in s3 bucket
    s3_prefix = os.getenv('AWS_S3_PREFIX')

    bot_token = os.getenv('MY_BOT_TOKEN')
    gemini_api = os.getenv('GEMINI_API')

    bot = CustomerServiceBot(bot_token, gemini_api, url, s3_bucket, s3_prefix)
    bot.run()