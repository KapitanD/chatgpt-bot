import openai
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import os

# Set up OpenAI API client
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up Telegram bot
bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])

def handle_message(message, context):
  # Get the chat ID and message text from the received message
  chat_id = message.effective_chat.id
  text = message.message.text

  # Use the GPT-3 API to generate a response to the message
  
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=text,
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\n"]
)

  # Extract the response text from the API response
  response_text = response["choices"][0]["text"]

  # Send the response back to the Telegram chat
  bot.send_message(chat_id=chat_id, text=response_text)

# Set up the Telegram bot to listen for messages
updater = Updater(bot=bot)
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()