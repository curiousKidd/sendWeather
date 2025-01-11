from flask import Flask, jsonify, request
import openAiApi

app = Flask(__name__)

# 기본 라우트 (홈 페이지)
@app.route('/')
def home():
    return "Python Flask 서버가 실행 중입니다!"

# 날씨 API 라우트
@app.route('/weather', methods=['GET'])
def weather():
   openAiApi.get_main()

if __name__ == '__main__':
    app.run(host='localhost', port=3000)
