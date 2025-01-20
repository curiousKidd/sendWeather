# 날씨 알림톡

다음날의 날씨를 카카오톡 메시지로 전송하여 날씨 확인을 편리하게 만들어주는 Python 기반 프로젝트입니다. 이 프로젝트는 Python과 OpenAI를 활용하여 구현되었으며, Docker와 Ansible을 통해 배포 및 관리를 수행합니다.

---

## 목차

- [소개](#소개)
- [프로젝트 구조](#프로젝트-구조)
- [설치 방법](#설치-방법)
- [사용법](#사용법)
- [배포 방법](#배포-방법)
- [기여 방법](#기여-방법)
- [라이선스](#라이선스)

---

## 소개

이 프로젝트는 날씨를 매일 확인해야 하는 번거로움을 줄이기 위해 만들어졌습니다.

### 주요 기능:

- 다음날의 날씨 정보를 자동으로 확인 및 가공
- 카카오톡 API를 이용해 알림 메시지 전송
- Python과 OpenAI API를 활용한 간단한 데이터 처리
- Docker 및 Docker-compose를 통한 컨테이너 기반 관리
- Ansible을 이용한 서버 배포 자동화

---

## 프로젝트 구조

```
.
├── Main.py               # 실행 파일, OpenAI 호출 담당
├── kakao.py              # 카카오톡 API 관련 파일 (토큰 설정 및 메시지 발송)
├── weather.py            # 날짜 및 날씨 API 처리 및 데이터 가공
├── Dockerfile            # Docker 컨테이너 설정 파일
├── docker-compose.yml    # Docker Compose 관리 파일
├── requirement.txt       # 의존성 라이브러리 목록
├── crontab               # 주기적 실행을 위한 크론탭 설정
└── playbook.yml          # Ansible 배포 설정 파일
```

---

## 설치 방법

1. **프로젝트 클론**

   ```bash
   git clone https://github.com/username/weather-kakao.git
   cd weather-kakao
   ```

2. **의존성 설치**

   ```bash
   pip install -r requirement.txt
   ```

3. **API 키 설정**
   - OpenAI와 카카오톡 API 키를 환경 변수로 설정하거나 별도의 설정 파일에 저장하세요.
     ```bash
     export OPENAI_API_KEY="your_openai_api_key"
     export KAKAO_API_KEY="your_kakao_api_key"
     ```

---

## 사용법

1. **Main.py 실행**

   ```bash
   python Main.py
   ```

   - Main.py는 OpenAI API를 호출하고, 다음날의 날씨 데이터를 가공하여 카카오톡으로 전송합니다.

2. **주요 파일 역할**
   - `Main.py`: 프로젝트의 실행 파일로, OpenAI 호출을 담당합니다.
   - `kakao.py`: 카카오톡 API 관련 로직을 포함하며, 토큰값 설정 및 메시지 발송을 처리합니다.
   - `weather.py`: 날짜와 날씨 API를 가공하여 메시지에 필요한 데이터를 제공합니다.

---

## 배포 방법

1. **Docker 컨테이너 빌드 및 실행**

   ```bash
   docker-compose up -d
   ```

2. **Ansible을 통한 배포**

   - `playbook.yml` 파일을 사용하여 개인 NAS 서버에 배포할 수 있습니다.
     ```bash
     ansible-playbook -i inventory playbook.yml
     ```

3. **Crontab 설정**
   - 주기적으로 Main.py를 실행하도록 크론탭을 설정합니다.
     ```bash
     crontab -e
     ```
     예:
     ```bash
     0 21 * * * /usr/bin/python3 /path/to/Main.py
     ```

---

## 추가 정보

- Python 3.9 이상 권장
- OpenAI 및 카카오톡 API 사용 관련 문서를 확인하세요.
