# 베이스 이미지 선택
FROM python:3.9-slim

# Timezone 데이터 설치 및 한국 시간 설정
RUN apt-get update && apt-get install -y tzdata
ENV TZ=Asia/Seoul

# Flask 설치 (필요 시)
# RUN pip install flask

# Cron 설치
RUN apt-get install -y cron
RUN apt-get install -y vim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 환경 변수 파일 복사 (선택사항)
COPY .env /app/.env

# 크론탭 파일 복사 및 권한 설정
COPY crontab /etc/cron.d/my-cron-job
# RUN chmod 0644 crontab /etc/cron.d/my-cron-job
RUN crontab /etc/cron.d/my-cron-job

# # 컨테이너 시작 시 실행할 명령어
# CMD ["python", "main.py"]

# Cron 로그 파일 생성
RUN touch /var/log/cron.log


# Cron 시작 및 백그라운드 실행
# CMD export $(cat /app/.env | xargs) && cron && tail -f /var/log/cron.log
CMD ["bash", "-c", "cron && tail -f /var/log/cron.log"]

