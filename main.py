import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timedelta

import weather
import kakao


# .env 파일에서 환경 변수 로드
load_dotenv()

def get_main():
    # 예시 호출
    weather_message = get_open_ai_message()
    # print(weather_message)

    kakao.send_kakao_message(weather_message)

def get_open_ai_message():
    location = "Seoul"
    summary = weather.get_tomorrow_weather(location)

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

    # API 키 설정
    api_key = os.getenv("OPENAI_API_KEY")
    print("api_key = ",api_key)
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set!")

    client = OpenAI(api_key=api_key) 

    # GPT에 질문 생성 및 응답 받기
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        # model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "너는 날씨 정보를 요약하고, 사용자의 하루를 위한 적절한 옷차림과 날씨 팁을 제공하는 어시스턴트야. "
                    "답변은 다음 형식으로 작성해: "
                    "1) 날씨 요약: YYYY-MM-DD 날씨는 흐림이며, 최고온도는 10도 최저온도는 0도 입니다. 강수확률은 30퍼 입니다."
                    "2) 맞춤 코멘트: 날씨가 추운 편이나, 다소 더울 수 있으므로, 두꺼운 패딩 대신 따뜻한 옷과 얇은 겉옷을 챙기는 건 어떠신가요?"
                )
            },
            {
                "role": "user",
                "content": (
                    f"다음 정보를 간단히 요약하고, "
                    f"적절한 코멘트를 추가해 줘: {summary}"
                )
            }
            # {"role": "system", "content": "너는 간단히 요약하고 날씨 팁을 제공하는 어시스턴트야."},
            # {"role": "user", "content": f"다음 정보를 요약해줘: {'오늘의 날씨는 맑음 입니다.'}"}
        ],
        
        max_tokens=150,
        temperature=0
    )

    # 응답 출력 또는 카카오톡 메시지로 보내기
    return response.choices[0].message.content



# 예시 호출
get_main()