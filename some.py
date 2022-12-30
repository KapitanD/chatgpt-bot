import os

import telebot
import openai
import replicate
from telegram import ChatAction

openai.api_key = os.getenv("OPENAI_API_TOKEN")

image_gen_model = replicate.models.get("stability-ai/stable-diffusion")
image_gen_version = image_gen_model.versions.get("f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1")

# Replace TOKEN with your bot's token
bot = telebot.TeleBot(os.getenv("TELEGRAM_API_TOKEN"))

# Replace CHANNEL_NAME and CHANNEL_ID with the name and ID of your channel
CHANNEL_NAME = "Тech Dvizh"
CHANNEL_ID = "@techdvizh"

def verify_subscription(bot: telebot.TeleBot):
    def decorator_verify(func):
        def wrapper_verify(*args, **kwargs):
            is_member = bot.get_chat_member(CHANNEL_ID, args[0].chat.id)
            if is_member.status in ["creator", "administrator", "member"]:
                # The user is a member of the channel
                return func(*args, **kwargs)
            else:
                # The user is not a member of the channel
                bot.send_message(args[0].chat.id, "Вы не подписались на Telegram-канал. Подписаться: https://t.me/+XU3w9Qsgxks3YTgy")
        return wrapper_verify
    return decorator_verify

def get_gpt_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )

    return response["choices"][0]["text"]

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        # Send a message to the user
        bot.send_message(message.chat.id, "Добро пожаловать в бот! Чтобы воспользоваться нашими услугами, вы должны быть подписчиком нашего Telegram-канала. Пожалуйста, присоединяйтесь к нашему каналу, чтобы продолжить. Подписаться: https://t.me/+XU3w9Qsgxks3YTgy ")

help_message = """Наш бот умеет две вещи - отвечать на вопросы и генерировать картинки из текста

/start - вывод стартового сообщения
/help - вывод этого сообщения
/image text - генерация картинки из текста
text - разговор с ботом
"""

@bot.message_handler(commands=['help'])
def help(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, help_message)

@bot.message_handler(commands=['image'])
@verify_subscription(bot)
def image(message):
    if message.chat.type == 'private':
        bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        response = image_gen_version.predict(prompt=message.text)

        if len(response) != 0:
            image_url = response[0]
            # Send the generated image to the user
            bot.send_photo(chat_id=message.chat.id, photo=image_url)
        else:
            # Print an error message if there was a problem with the request
            bot.send_message(chat_id=message.chat.id, text="Sorry, there was an error generating the image. Please try again.")

@bot.message_handler()
@verify_subscription(bot)
def chat(message):
    response_text = get_gpt_response(message.text)
    bot.send_message(message.chat.id, response_text)

bot.polling()