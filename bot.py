from telegram import Update
from train_gemini import Gemini
from telegram.ext import (ContextTypes, 
                          CommandHandler, 
                          filters,
                          Application,
                          MessageHandler)


class CustomerServiceBot:
    def __init__(self, bot_token, gemini_api, url, training_data_dir) -> None:
        self.gimini = Gemini(gemini_api, url, training_data_dir)
        self.application = Application.builder().token(bot_token).build()
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, 
                                                    self.handle_query))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_first_name = update.effective_user.first_name
        welcome_msg = f"Hello {user_first_name}! Welcome to our company. How can I assist you?"
        
        await update.message.reply_text(welcome_msg)

    async def handle_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_msg: str = update.message.text
        response = self.gimini.get_response(user_msg)
        await update.message.reply_text(response)

    def run(self):
        print('======== Bot is running ========')
        self.application.run_polling()
