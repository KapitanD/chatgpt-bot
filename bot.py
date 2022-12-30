import requests
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Replace TOKEN with your bot's token
TOKEN = "5800666562:AAE27O-o8VnBBNdXJakx31lcHoo2slDxbdQ"

# Create an Updater object to handle updates from Telegram
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    # Print a message to the user when they start the bot
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am a bot that generates images for any queries. Just send me a message with your query and I will try to find an image for you.")

def image(update, context):
    # Get the message text
    query = update.message.text

    # Use the DALL-E API to generate an image for the query
    api_key = "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"
    endpoint = "https://api.openai.com/v1/images/generations"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = """
    {
        """
    data += f'"model": "image-alpha-001",'
    data += f'"prompt": "{query}",'
    data += """
        "num_images":1,
        "size":"256x256",
        "response_format":"url"
    }
    """

    response = requests.post(endpoint, headers=headers, data=data)
    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        # Send the generated image to the user
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
    else:
        # Print an error message if there was a problem with the request
        logging.debug(f"response: {response}")
        logging.debug(f"response.body: {response.text}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, there was an error generating the image. Please try again.")

# Add a command handler for the /start command
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

# Add a message handler for all other messages
image_handler = MessageHandler(Filters.text, image)
dispatcher.add_handler(image_handler)

# Start the bot
updater.start_polling()