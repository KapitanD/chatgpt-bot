import discord
import telegram
import requests
import os

# Set up Discord client
client = discord.Client()

# Set up Telegram bot
bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])

async def handle_message(message):
  # Get the chat ID and message text from the received message
  chat_id = message.chat.id
  text = message.text

  # Send the description to the Discord server through the Mijorney bot
  await client.send_message(
    client.get_channel("DISCORD_CHANNEL_ID"),
    f"Mijorney, generate image: {text}"
  )

  # Wait for the Mijorney bot to send the image URL back
  image_url = None
  while not image_url:
    async for message in client.logs_from(client.get_channel("DISCORD_CHANNEL_ID"), limit=1):
      if message.author.id == "MIJORNEY_BOT_ID":
        image_url = message.content
        break

  # Send the image URL back to the Telegram chat
  bot.send_message(chat_id=chat_id, text=image_url)

# Set up the Telegram bot to listen for messages
updater = telegram.ext.Updater(bot=bot)
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_polling()