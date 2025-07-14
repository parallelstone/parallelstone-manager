# Directory Structure

## 패키지 구조
```
parallelstone-manager/
├── pyproject.toml              # 패키지 설정 및 의존성 관리 (통합)
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
│   │   ├── telegram_sender.py  # 텔레그램 알림 처리
│   │   ├── discord_sender.py   # 디스코드 알림 처리
│   │   └── slack_sender.py     # 슬랙 알림 처리
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
├── tests/                      # 테스트 패키지
│   ├── __init__.py
│   ├── conftest.py            # pytest 설정 및 공통 fixture
│   ├── unit/                  # 유닛 테스트
│   │   ├── __init__.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── test_players.py  # players API 테스트
│   │   │   └── test_server.py   # server API 테스트 (RCON mock)
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── test_rcon.py     # RCON 서비스 테스트
│   │   │   └── test_rabbitmq.py # RabbitMQ 서비스 테스트
│   │   └── consumers/
│   │       ├── __init__.py
│   │       ├── test_telegram_sender.py
│   │       ├── test_discord_sender.py
│   │       └── test_slack_sender.py
│   └── integration/           # 통합 테스트 (선택적)
│       ├── __init__.py
│       └── test_api_integration.py
│
└── parallelstone_manager.egg-info/  # 패키지 설치 정보 (자동 생성)
```

## 실행 방법
```bash
# 패키지 설치 (개발 모드)
uv pip install -e .

# 개발 의존성 설치
uv pip install -e ".[dev]"

# FastAPI 서버 실행 (Consumer 프로세스들 자동 시작)
uvicorn parallelstone_manager.main:app --reload

# 개별 Consumer 실행 (디버깅용)
python -m parallelstone_manager.consumers.telegram_sender

# 테스트 실행
pytest                    # 모든 테스트 실행
pytest tests/unit/        # 유닛 테스트만 실행
pytest -v                 # 상세한 출력
```


# RabbitMQ
```
Exchange: "notification_router" (type: topic)
├── telegram_queue → binding: "#.telegram.#"
├── discord_queue  → binding: "#.discord.#"
└── slack_queue    → binding: "#.slack.#"
```