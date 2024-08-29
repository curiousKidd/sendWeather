import requests
import os
from datetime import datetime, timedelta

# chat gpt를 활용하면... 개발할 수없을까?

# 서울의 위도와 경도
LATITUDE = 37.5665
LONGITUDE = 126.9780

URL = "https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Asia/Seoul"


def get_tomorrow_weather():
    response = requests.get(URL)
    data = response.json()

    # 내일의 날짜 구하기
    tomorrow_index = 1

    # 내일 날씨 정보 추출
    daily = data['daily']
    max_temp = daily['temperature_2m_max'][tomorrow_index]
    min_temp = daily['temperature_2m_min'][tomorrow_index]
    precipitation = daily['precipitation_sum'][tomorrow_index]

    weather_message = ("내일의 날씨:\n"
                       "최고 기온: {max_temp}°C\n"
                       "최저 기온: {min_temp}°C\n"
                       "강수량: {precipitation}mm")

    return weather_message
