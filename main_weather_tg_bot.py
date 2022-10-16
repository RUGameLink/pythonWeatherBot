import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши название города и я пришлю тебе погоду!:)")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smiley = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождик \U00002614",
        "Drizzle": "Дождик \U00002614",
        "Thunderstorm": "Грозище \U000026A1",
        "Snow": "Снежок \U0001F328",
        "Mist": "Туманчик \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smiley:
            wd = code_to_smiley[weather_description]
        else:
            wd = "Посмотри в окно"

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        length_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"\U0001F3D9 Город {city}\n"
              f" Температура {cur_weather} °C {wd}\n"
              f"\U0001F4A7 Влажность {humidity} %\n"
              f" Давление {pressure} мм.рт.ст.\n"
              f"\U0001F32C Скорость ветра {wind} м/с\n"
              f"\U0001F305 Время рассвета: {sunrise_timestamp}\n"
              f"\U0001F307 Время заката: {sunset_timestamp}\n"
              f"\U0001F55C День длился: {length_of_day}")
    except:
        await message.reply("\U00002620 Проверьте название города!")


if __name__ == '__main__':
    executor.start_polling(dp)