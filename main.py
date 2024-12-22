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
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={weather_api_key}&units=metric"

    # 날씨 API 호출
    weather_response = requests.get(forecast_url)
    if weather_response.status_code != 200:
        return "날씨 정보를 가져오는 데 실패했습니다."

    # 날씨 정보 가져오기
    weather_data = weather_response.json()

    # 내일 데이터 필터링
    from datetime import datetime, timedelta
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow_data = [entry for entry in weather_data["list"] if entry["dt_txt"].startswith(tomorrow)]

    print("toto",tomorrow_data)

    # 내일 날씨 요약 생성
    # if not tomorrow_data:
    #     return "내일 날씨 정보를 찾을 수 없습니다."
    
    temps = [entry["main"]["temp"] for entry in tomorrow_data]
    conditions = [entry["weather"][0]["description"] for entry in tomorrow_data]
    max_temp = max(temps)
    min_temp = min(temps)
    common_condition = max(set(conditions), key=conditions.count)

    summary = f"서울의 날씨는 최고온도 {max_temp}도, 최저온도 {min_temp}도, 날씨는 {common_condition}입니다."

    # GPT 요약 요청 (옵션)
    


    # GPT에 질문 생성 및 응답 받기
    text = f"다음 정보를 간단히 요약해 주세요: {summary}"
    response = client.completions.create(
        # model="gpt-4o-mini",
        model="gpt-3.5-turbo",
        prompt=text,
        max_tokens=100,
        temperature=0
        )

    # 응답 출력 또는 카카오톡 메시지로 보내기
    return response.choices[0].text


weather_message = get_tomorrow_weather()

print(weather_message)