import json
import requests
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

CLIENT_ID = os.getenv("KAKAO_REST_API_KEY") # 발급받은 restAPI KEY
REDIRECT_URI =  "http://localhost:3000" # 등록한 Redirect URI
OAUTH_CODE = os.getenv("KAKAO_OAUTH") # 발급받은 OAuth KEY
scope = "talk_message,friends"  # 필요한 권한 추가

# 카카오 로그인 인증 || 1회성 코드 발급
def kakao_get_code():
    auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}"

    print("다음 URL에 접속해 인증하세요:")
    print(auth_url)


# 카카오 OAuth URL
def kakao_oauth_token():
    # 카카오 토큰 발급 URL
    token_url = "https://kauth.kakao.com/oauth/token"
    # token_url = f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&code={OAUTH_CODE}"

    # POST 요청 데이터
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": OAUTH_CODE,
    }
    
    
    response = requests.post(token_url, data=data)
    print(response.json())
    tokens = response.json()

    # Access Token과 Refresh Token 확인
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    # 유효기간 짧음 4h
    print("Access Token:", access_token)

    # 유효기간 김 60d
    print("Refresh Token:", refresh_token)

    save_tokens(access_token, refresh_token)


# 토큰 저장
def save_tokens(access_token, refresh_token):
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    with open("tokens.json", "w") as f:
        json.dump(tokens, f)


# 토큰 로드 함수
def load_tokens():
    try:
        with open("tokens.json", "r") as f:
            tokens = json.load(f)
        return tokens
    except FileNotFoundError:
        return None

# access_token 재발급 || 리프레시 토큰 활용
def refresh_access_token(refresh_token):
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": refresh_token,
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        new_tokens = response.json()
        access_token = new_tokens.get("access_token")
        
        # Refresh Token이 새로 발급되었을 경우 업데이트
        if "refresh_token" in new_tokens:
            refresh_token = new_tokens["refresh_token"]

        # 토큰 저장
        save_tokens(access_token, refresh_token)
        return access_token
    else:
        print("토큰 갱신 실패:", response.json())
        return None


# 메시지 전송
def send_kakao_message(message_text):
    tokens = load_tokens()
    if not tokens:
        print("토큰이 없습니다. 처음 인증을 진행하세요.")
        return

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # 토큰 갱신
    if not access_token:  # 토큰이 없는 경우
        access_token = refresh_access_token(refresh_token)

    # 메시지 API 호출
    message_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    data = {
        "template_object": json.dumps(
            {
            "object_type": "text",
            "text": message_text,
            "link": {
                "web_url": "https://weather.com",
                "mobile_web_url": "https://weather.com"
            }
        })  
    }

    response = requests.post(message_url, headers=headers, data=data)
    if response.status_code == 200:
        print("메시지가 성공적으로 전송되었습니다!")
    elif response.status_code == 401:  # Unauthorized (토큰 만료)
        print("Access Token이 만료되었습니다. 갱신을 시도합니다.")
        access_token = refresh_access_token(refresh_token)
        if access_token:
            send_kakao_message(message_text)
    else:
        print("메시지 전송 실패:", response.json())


# 친구 메시지 발송
def send_kakao_friend_message(message_text):
    tokens = load_tokens()
    if not tokens:
        print("토큰이 없습니다. 처음 인증을 진행하세요.")
        return

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # 토큰 갱신
    if not access_token:  # 토큰이 없는 경우
        access_token = refresh_access_token(refresh_token)

    friends = get_kakao_friend()

    # 메시지 API 호출
    message_url = "	https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    uuids = []

    if friends:
        for friend in friends:
            uuids.append(friend.get("uuid"))


    data = {
        "receiver_uuids": json.dumps(uuids),
        "template_object": json.dumps(
            {
            "object_type": "text",
            "text": message_text,
            "link": {
                "web_url": "https://weather.com",
                "mobile_web_url": "https://weather.com"
            }
        })  
    }

    response = requests.post(message_url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"{friend['profile_nickname']} 메시지가 성공적으로 전송되었습니다!")

    elif response.status_code == 401:  # Unauthorized (토큰 만료)
        print("Access Token이 만료되었습니다. 갱신을 시도합니다.")
        access_token = refresh_access_token(refresh_token)
        if access_token:
            send_kakao_friend_message(message_text)
    else:
        print(f"{friend['profile_nickname']} 메시지 전송 실패:", response.json())


# 친구 목록 가져오기
def get_kakao_friend():
    tokens = load_tokens()
    if not tokens:
        print("토큰이 없습니다. 처음 인증을 진행하세요.")
        return

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    # 토큰 갱신
    if not access_token:  # 토큰이 없는 경우
        access_token = refresh_access_token(refresh_token)

    # 메시지 API 호출
    url = "https://kapi.kakao.com/v1/api/talk/friends"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("친구 목록 가져오기 실패:", response.json())


    return response.json().get("elements") 

    
# kakao_get_code()

# kakao_oauth_token()

# get_kakao_friend()


# send_kakao_friend_message("test")