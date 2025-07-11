# Directory
```
minecraft_api/
├── main.py              # FastAPI 앱 진입점 + 백그라운드 태스크 시작
│
├── routers/             # API 엔드포인트 그룹화
│   ├── __init__.py
│   ├── server.py        # 서버 제어 관련
│   └── players.py       # 플레이어 관리
│
├── services/            # 실제 비즈니스 로직
│   ├── __init__.py
│   ├── rcon.py          # RCON 통신
│   └── rabbitmq.py      # RabbitMQ 메시지 발송/수신 로직
│
├── consumers/           # 백그라운드 태스크들
│   ├── __init__.py
│   ├── telegram_sender.py      # 텔레그램 알림 처리
│   ├── discord_sender.py       # 디스코드 알림 처리
│   └── slack_sender.py         # 슬랙 알림 처리
│
├── models/              # 데이터 타입 정의 + 검증
│   ├── __init__.py
│   ├── player.py        # 플레이어 모델
│   └── responses.py     # 공통 응답 모델 (CommandResponse 등)
│
├── core/                # 앱 기본 설정 + 공통 기능
│   ├── __init__.py
│   ├── config.py        # 환경설정 관리
│   └── dependencies.py  # 의존성 주입
│
└── requirements.txt
```


# RabbitMQ
```
Exchange: "notification_router" (type: topic)
├── telegram_queue → binding: "#.telegram.#"
├── discord_queue  → binding: "#.discord.#"
└── slack_queue    → binding: "#.slack.#"
```