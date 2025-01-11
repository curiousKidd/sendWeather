import requests

# def get_tomorrow_weather():
#      # 날씨 API 설정
#     weather_api_key = os.environ.get("weather_api_key")
#     location = "Seoul"
#     forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={weather_api_key}&units=metric"

#     # 날씨 API 호출
#     weather_response = requests.get(forecast_url)
#     if weather_response.status_code != 200:
#         return "날씨 정보를 가져오는 데 실패했습니다."

#     # 날씨 정보 가져오기
#     weather_data = weather_response.json()

#     # 내일 데이터 필터링
    
#     tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
#     tomorrow_data = [entry for entry in weather_data["list"] if entry["dt_txt"].startswith(tomorrow)]

#     # 내일 날씨 요약 생성
#     if not tomorrow_data:
#         return "내일 날씨 정보를 찾을 수 없습니다."

#     temps = [entry["main"]["temp"] for entry in tomorrow_data]
#     conditions = [entry["weather"][0]["description"] for entry in tomorrow_data]
#     max_temp = max(temps)
#     min_temp = min(temps)
#     common_condition = max(set(conditions), key=conditions.count)
#      # GPT 요약 요청 (옵션)  
#     summary = f"서울의 날씨는 최고온도 {max_temp}도, 최저온도 {min_temp}도, 날씨는 {common_condition}입니다."
#     print("summary = ", summary)
#     return summary