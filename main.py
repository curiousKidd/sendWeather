from openai import OpenAI
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv


# .env 파일에서 환경 변수 로드
load_dotenv()

def get_tomorrow_weather():
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
    
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow_data = [entry for entry in weather_data["list"] if entry["dt_txt"].startswith(tomorrow)]

    # 내일 날씨 요약 생성
    if not tomorrow_data:
        return "내일 날씨 정보를 찾을 수 없습니다."

    temps = [entry["main"]["temp"] for entry in tomorrow_data]
    conditions = [entry["weather"][0]["description"] for entry in tomorrow_data]
    max_temp = max(temps)
    min_temp = min(temps)
    common_condition = max(set(conditions), key=conditions.count)
     # GPT 요약 요청 (옵션)  
    summary = f"서울의 날씨는 최고온도 {max_temp}도, 최저온도 {min_temp}도, 날씨는 {common_condition}입니다."
    print("summary = ", summary)
    return summary

def get_tomorrow_weather_kma(location: str):
    # 기상청 API 키 가져오기
    # service_key = os.environ.get("KMA_API_KEY")  # 환경변수에 API 키 저장
    service_key = os.getenv("KMA_API_KEY")

    # 격자 좌표 (서울: x=60, y=127)
    grid = {
        "Seoul": {"x": 60, "y": 127},
        # 다른 지역 추가 가능
    }

    if location not in grid:
        return "지원하지 않는 지역입니다."

    x, y = grid[location]["x"], grid[location]["y"]

    # 내일 날짜 계산
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

    # 기상청 API URL 생성
    base_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        "serviceKey": service_key,
        "numOfRows": 1000,  # 요청 항목 수 (적절히 설정)
        "pageNo": 1,
        "dataType": "JSON",
        "base_date": datetime.now().strftime("%Y%m%d"),
        "base_time": "0500",  # 기상청 예보 기준 시간
        "nx": x,
        "ny": y,
    }

    # 기상청 API 호출
    response = requests.get(base_url, params=params)
    # HTTP 상태 코드 확인
    if response.status_code != 200:
        print(f"HTTP 상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text}")
        return "기상청 API 호출에 실패했습니다."

    # JSON 응답 처리
    try:
        weather_data = response.json()
    except ValueError:
        print("JSON 디코딩에 실패했습니다.")
        print(f"응답 내용: {response.text}")
        return "API 응답을 처리할 수 없습니다."

    # API 결과 상태 확인
    if "response" not in weather_data or weather_data["response"]["header"]["resultCode"] != "00":
        print(f"기상청 API 오류 코드: {weather_data.get('response', {}).get('header', {}).get('resultCode', '알 수 없음')}")
        return "기상청 API에서 데이터를 가져오는 데 실패했습니다."

    # 응답 데이터 파싱
    weather_data = response.json()
    if "response" not in weather_data or weather_data["response"]["header"]["resultCode"] != "00":
        return "기상청 API에서 데이터를 가져오는 데 실패했습니다."

    items = weather_data["response"]["body"]["items"]["item"]

    # 내일 날씨 데이터 필터링
    tomorrow_data = [item for item in items if item["fcstDate"] == tomorrow]

    if not tomorrow_data:
        return "내일 날씨 정보를 찾을 수 없습니다."
    
    summary = []
    
    time_slots = sorted(set(item["fcstTime"] for item in tomorrow_data))  # 모든 예보 시간
    for time in time_slots:
        # 시간대별 데이터 필터링
        time_data = [item for item in tomorrow_data if item["fcstTime"] == time]
        temp = next((item["fcstValue"] for item in time_data if item["category"] == "TMP"), None)
        pty = next((item["fcstValue"] for item in time_data if item["category"] == "PTY"), None)
        sky = next((item["fcstValue"] for item in time_data if item["category"] == "SKY"), None)

        # 강수 형태, 하늘 상태 해석
        pty_map = {"0": "강수 없음", "1": "비", "2": "비/눈", "3": "눈", "4": "소나기"}
        sky_map = {"1": "맑음", "3": "구름 많음", "4": "흐림"}

        summary.append({
            "time": time,
            "temp": f"{temp}℃" if temp else "데이터 없음",
            "pty": pty_map.get(pty, "알 수 없음"),
            "sky": sky_map.get(sky, "알 수 없음")
        })

    return summary


def get_open_ai():
    location = "Seoul"
    summary = get_tomorrow_weather_kma(location)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

    # GPT에 질문 생성 및 응답 받기
    response = client.chat.completions.create(
        # model="gpt-4o-mini",
        model="gpt-3.5-turbo",
        messages=[
        #     {
        #         "role": "system",
        #         "content": (
        #             "너는 날씨 정보를 요약하고, 사용자의 하루를 위한 적절한 옷차림과 날씨 팁을 제공하는 어시스턴트야. "
        #             "답변은 다음 형식으로 작성해: "
        #             "1) 날씨 요약: 오늘의 날씨는 흐림이며, 최고온도는 10도 최저온도는 0도 입니다. 강수확률은 30퍼 입니다."
        #             "2) 맞춤 코멘트: 날씨가 추운 편이나, 다소 더울 수 있으므로, 두꺼운 패딩 대신 따뜻한 옷과 얇은 겉옷을 챙기는 건 어떠신가요?"
        #         )
        #     },
        #     {
        #         "role": "user",
        #         "content": (
        #             f"다음 정보를 간단히 요약하고, "
        #             f"적절한 코멘트를 추가해 줘: {summary}"
        #         )
        #     }
            {"role": "system", "content": "너는 간단히 요약하고 날씨 팁을 제공하는 어시스턴트야."},
            {"role": "user", "content": f"다음 정보를 요약해줘: {'오늘의 날씨는 맑음 입니다.'}"}
        ],
        
        max_tokens=100,
        temperature=0
    )

    # 응답 출력 또는 카카오톡 메시지로 보내기
    return response.choices[0].message.content

def send_kakao_message(message, user_id):
    kakao_api_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer YOUR_KAKAO_ACCESS_TOKEN"}  # 대체 텍스트
    
    data = {
        "template_object": {
            "object_type": "text",
            "text": message,
            "link": {"web_url": "https://your-website.com"}
        }
    }

    response = requests.post(kakao_api_url, headers=headers, json=data)
    return response.status_code

# 예시 호출
weather_message = get_open_ai()
print(weather_message)