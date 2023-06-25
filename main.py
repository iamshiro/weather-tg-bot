import json
import yaml
import telebot
import requests

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

bot_token = config['bot_token']
weather_api_key = config['weather_api_key']
bot = telebot.TeleBot(bot_token)
weather_API = weather_api_key


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую!!!')
    bot.send_message(message.chat.id, 'Напишите название города')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сейчас погода: {temp}')
    else:
        bot.reply_to(message, 'Город указан не верно')


bot.polling(none_stop=True)
