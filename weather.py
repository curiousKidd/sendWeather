import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

def get_tomorrow_weather(location: str):
    
    # 날씨 정보 api 호출
    weather_data = get_weather_api(location)

    
    items = weather_data["response"]["body"]["items"]["item"]

    # 내일 날짜 계산
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")

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


def get_weather_api(location: str):
    # 기상청 API 키 가져오기
    # service_key = os.environ.get("KMA_API_KEY")  # 환경변수에 API 키 저장
    service_key = os.getenv("WEATHER_API_KEY")

    # 격자 좌표 (서울: x=60, y=127)
    grid = {
        "Seoul": {"x": 60, "y": 127},
        # 다른 지역 추가 가능
    }

    if location not in grid:
        return "지원하지 않는 지역입니다."

    x, y = grid[location]["x"], grid[location]["y"]

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
    
    return weather_data
