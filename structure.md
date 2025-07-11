# Directory Structure

## 패키지 구조
```
parallelstone-manager/
├── setup.py                     # 패키지 설정 파일
├── requirements.txt             # 의존성 목록
├── .env                        # 환경변수 (프로젝트 루트)
├── structure.md                # 프로젝트 구조 문서
│
├── parallelstone_manager/      # 메인 패키지
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 진입점 + Consumer 프로세스 관리
│   │
│   ├── routers/                # API 엔드포인트 그룹화
│   │   ├── __init__.py
│   │   ├── server.py           # 서버 제어 관련
│   │   └── players.py          # 플레이어 관리
│   │
│   ├── services/               # 실제 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── rcon.py             # RCON 통신
│   │   └── rabbitmq.py         # RabbitMQ 메시지 발송/수신 로직
│   │
│   ├── consumers/              # 독립 프로세스 Consumer들
│   │   ├── __init__.py
│   │   ├── consumer.py         # BaseConsumer 클래스
│   │   ├── telegram_sender.py  # 텔레그램 알림 처리 (독립 프로세스)
│   │   ├── discord_sender.py   # 디스코드 알림 처리 (구현 예정)
│   │   └── slack_sender.py     # 슬랙 알림 처리 (구현 예정)
│   │
│   ├── models/                 # 데이터 타입 정의 + 검증
│   │   ├── __init__.py
│   │   ├── players.py          # 플레이어 모델
│   │   └── responses.py        # 공통 응답 모델 (CommandResponse 등)
│   │
│   └── core/                   # 앱 기본 설정 + 공통 기능
│       ├── __init__.py
│       ├── config.py           # 환경설정 관리
│       └── dependencies.py     # 의존성 주입
│
└── parallelstone_manager.egg-info/  # 패키지 설치 정보 (자동 생성)
```

## 실행 방법
```bash
# 패키지 설치 (개발 모드)
uv pip install -e .

# FastAPI 서버 실행 (Consumer 프로세스들 자동 시작)
uvicorn parallelstone_manager.main:app --reload

# 개별 Consumer 실행 (디버깅용)
python -m parallelstone_manager.consumers.telegram_sender
```


# RabbitMQ
```
Exchange: "notification_router" (type: topic)
├── telegram_queue → binding: "#.telegram.#"
├── discord_queue  → binding: "#.discord.#"
└── slack_queue    → binding: "#.slack.#"
```