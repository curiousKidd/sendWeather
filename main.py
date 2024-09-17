import openai
import requests


def get_tomorrow_weather():
    # chat gpt를 활용하면... 개발할 수없을까?

    # 날씨 API 설정
    weather_api_key = "43604b3735cff561b8407ea5f50d6acc"
    location = "Seoul"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}"

    print("111111111111111111")
    print("111111111111111111")

    # GPT API 설정
    openai.api_key = "YOUR_OPENAI_API_KEY"

    # 날씨 정보 가져오기
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    # GPT에 질문 생성 및 응답 받기
    question = f"Seoul의 현재 날씨는 다음과 같습니다: {weather_data}. 이에 대한 요약을 해주세요."
    response = openai.Completion.create(engine="text-davinci-004", prompt=question, max_tokens=100)

    # 응답 출력 또는 카카오톡 메시지로 보내기
    return response['choices'][0]['text']
