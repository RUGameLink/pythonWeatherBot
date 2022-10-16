import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):

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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        #pprint(data)

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

        length_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        print(f"\U0001F3D9 Город {city}\n"
              f"\U0000F321 Температура {cur_weather} °C {wd}\n"
              f"\U0001F4A7 Влажность {humidity} %\n"
              f"\U00003374 Давление {pressure} мм.рт.ст.\n"
              f"\U0001F32C Скорость ветра {wind} м/с\n"
              f"\U0001F305 Время рассвета: {sunrise_timestamp}\n"
              f"\U0001F307 Время заката: {sunset_timestamp}\n"
              f"\U0001F55C День длился: {length_of_day}")
    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()