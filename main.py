from openai import OpenAI
import requests
import os


def get_tomorrow_weather():
    # chat gpt를 활용하면... 개발할 수없을까?
    # 왜 안돼.....
    # 짜증이 나기 시작하네

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 

    # 날씨 API 설정
    weather_api_key = os.environ.get("weather_api_key")
    location = "Seoul"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}"

    weather_response = requests.get(weather_url)

    print(weather_response.json())

    # GPT API 설정

    # 날씨 정보 가져오기
    weather_data = weather_response.json()

    # print(weather_data)

    # GPT에 질문 생성 및 응답 받기
    text = f"""Seoul의 현재 날씨는 다음과 같습니다: {weather_data}. 이에 대한 요약을 해주세요.
    답변 형식은 서울의 날씨는 최고온도 *도, 최저온도 *도 날씨는 **(안개, 맑음, 눈 기타 등등)입니다.
    """
    response = client.completions.create(
            # model="gpt-4o-mini",
            model="gpt-3.5-turbo-instruct",
            prompt=text,
            max_tokens=200
        )

    # 응답 출력 또는 카카오톡 메시지로 보내기
    return response.choices[0].text


weather_message = get_tomorrow_weather()

print(weather_message)