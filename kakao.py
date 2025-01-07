import json
import requests
import os

CLIENT_ID = os.getenv("KAKAO_REST_API_KEY") # 발급받은 restAPI KEY
REDIRECT_URI =  "http://localhost:3000" # 등록한 Redirect URI

def kakao_oauth_token():

    redirect_uri =  "http://localhost:3000"  

    # 카카오 토큰 발급 URL
    token_url = "https://kauth.kakao.com/oauth/token"

    # POST 요청 데이터
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code": "일회성 코드값",
    }

    response = requests.post(token_url, data=data)
    tokens = response.json()

    # Access Token과 Refresh Token 확인
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)


# 카카오 OAuth URL
def kakao_get_code():
    auth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code"

    print("다음 URL에 접속해 인증하세요:")
    print(auth_url)

# 토큰 저장
def save_tokens(access_token, refresh_token):
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    with open("tokens.json", "w") as f:
        json.dump(tokens, f)