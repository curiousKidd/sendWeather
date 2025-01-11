# 베이스 이미지 선택
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install flask

# 프로젝트 파일 복사
COPY . .

# 환경 변수 파일 복사 (선택사항)
COPY .env .

# 컨테이너 시작 시 실행할 명령어
CMD ["python", "main.py"]