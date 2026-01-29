# VibeMemory

AI 컨텍스트 영속화 시스템

## 문제

바이브 코딩에서 AI는 이전 대화를 기억하지 못합니다.

- 30분 전에 "OAuth 금지"라고 했는데 AI가 OAuth 코드를 생성
- 어제 합의한 아키텍처를 오늘 AI가 전혀 모름
- 왜 이렇게 만들었는지 아무도 기억 못함

## 해결책

프로젝트에 `.vibe` 디렉토리를 추가하여 컨텍스트를 영구 저장합니다.

```
.vibe/
├── context.yaml      # 프로젝트 정보, 기술 스택
├── constraints.yaml  # 금지 규칙 (OAuth 금지 등)
├── decisions.yaml    # 기술 결정 사항과 이유
└── history/          # 세션별 변경 이력
```

## 핵심 기능

- **Context Injection**: AI 세션마다 프로젝트 맥락 자동 주입
- **Constraint Guard**: 금지 규칙 위반 실시간 감지
- **Decision Capture**: 기술 결정 자동 기록
- **Intent Tracking**: "왜 이렇게 만들었는지" 추적

## 데모 실행

```bash
cd demo
python vibememory_core.py
```

## 사용법

```bash
# 프로젝트 초기화
python vibe_cli.py init

# 현재 컨텍스트 확인 (AI에 주입할 프롬프트)
python vibe_cli.py inject

# 코드 파일 정책 검사
python vibe_cli.py check your_code.py

# 금지 규칙 추가
python vibe_cli.py add-constraint "외부 CDN 사용 금지"
```

## 예시: 금지 규칙 위반 감지

```yaml
# .vibe/constraints.yaml
constraints:
  - id: C001
    rule: OAuth 사용 금지
    severity: critical
    keywords: [oauth, google.oauth2]
```

코드에 `from google.oauth2 import credentials`가 있으면 즉시 경고합니다.

## 라이선스

MIT License
