from telegram import Update
from train_gemini import Gemini
from telegram.ext import (ContextTypes, 
                          CommandHandler, 
                          filters,
                          Application,
                          MessageHandler)


class CustomerServiceBot:
    def __init__(self, bot_token, gemini_api, url, s3_bucket, s3_prefix) -> None:
        self.gemini = Gemini(gemini_api, url, s3_bucket, s3_prefix)
        self.application = Application.builder().token(bot_token).build()
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, 
                                                    self.handle_query))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_first_name = update.effective_user.first_name
        user_id = update.effective_user.id
        print(f'{user_first_name} (id = {user_id}) joined the bot.')
        self.gemini.initialize_user_chat(user_id)

        welcome_msg = f"Hello {user_first_name}! Welcome to our company. How can I assist you?"
        
        await update.message.reply_text(welcome_msg)

    async def handle_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_msg: str = update.message.text
        user_id = update.message.id
        response = self.gemini.get_response(user_msg, user_id)
        await update.message.reply_text(response)

    def run(self):
        print('======== Bot is running ========')
        self.application.run_polling()
