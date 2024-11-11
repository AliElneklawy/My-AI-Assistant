# AI-Powered Personal Assistant Telegram Bot

A sophisticated Telegram chatbot powered by Google's Gemini AI that serves as a virtual personal assistant. The bot is trained on custom knowledge bases (websites, documents, and personal information) to provide accurate information and responses about me while maintaining natural conversation flow.

## Features

- 🤖 **Powered by Google's Gemini AI**: Utilizing state-of-the-art language model for natural and intelligent responses
- 📚 **Custom Knowledge Base**: Trained on personal information, websites, and documents
- 🌐 **Website Crawler**: Automatically extracts information from personal/professional websites
- 💡 **Smart Context Understanding**: Uses advanced text embeddings to find relevant information
- 💬 **Conversation History**: Maintains chat history for contextual responses
- ⚡ **Real-time Processing**: Quick response times with efficient text processing
- 📝 **Document Processing**: Supports PDF and TXT file formats for training data

## Prerequisites

- Python 3.x
- Telegram Bot Token
- Google Gemini API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AliElneklawy/personal-assistant-bot.git
cd personal-assistant-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Create a .env file in the project root directory with the following variables:
```bash
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

## Usage

1. Set up:
      - Place personal documents (PDF/TXT) in the `data` directory
      - Configure personal website URLs in the bot initialization
      - Edit the prompt in `train_gemini.py`

2. Run the bot:
```bash
python bot.py
```

## Key Components

 - `bot.py`: Handles Telegram bot setup and message routing
 - `train_gemini.py`: Manages AI model training, knowledge base creation, and response generation
 - `main.py`: Start the bot
