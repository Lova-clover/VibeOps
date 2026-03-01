# 🚀 VibeOps

> 바이브 코딩을 위한 품질 파이프라인 PoC (DevOps 관점)  
> "AI에게 코드를 요청하기 전에, 먼저 스펙을 확정하라."

## 🔥 핵심 메시지
**"바이브 코딩에도 품질 관리 프로세스가 필요하다."**

바이브 코딩은 빠르지만, 프로세스가 없으면 기술 부채가 누적됩니다.  
VibeOps는 `Spec -> Verify -> Generate -> Validate -> Document` 흐름으로 이를 통제 가능한 프로세스로 전환합니다.

## 📌 개요
VibeOps는 바이브 코딩 과정에 `Spec -> Verify -> Generate -> Validate -> Document` 흐름을 적용해,
의도 불일치/정책 위반/맥락 소실을 줄이기 위한 개념 증명(Proof of Concept) 저장소입니다.

핵심은 "더 빠르게 생성"이 아니라, "생성 전후 통제 가능한 개발 프로세스"입니다.

## 🔗 문서 및 링크
- 🌐 데모 사이트: [vibeops-rho.vercel.app](https://vibeops-rho.vercel.app/)
- 📄 1차 기획서(PDF): [VibeOps 기획서.pdf](./VibeOps 기획서.pdf)
- 🏁 최종 기획서(PDF): [VibeOps 최종 기획서.pdf](./VibeOps 최종 기획서.pdf)
- 🎬 데모 영상: [VibeOps데모영상.mp4](./VibeOps데모영상.mp4)
- 🗂️ 제출본(해커톤 PDF): [월간 해커톤_ 바이_VibeOps - 바이브 코딩을 위한 품질 파이프라인__성주__20260301.pdf](./월간 해커톤_ 바이_VibeOps - 바이브 코딩을 위한 품질 파이프라인__성주__20260301.pdf)

## 📁 저장소 구성
```text
.
├─ web/
│  └─ index.html                 # 정적 데모 페이지 (브라우저 인터랙션)
├─ demo/
│  ├─ vibe_cli.py                # CLI 인터페이스 PoC
│  ├─ vibememory_core.py         # 컨텍스트/제약 검사 코어 PoC
│  └─ .vibe/                     # 샘플 컨텍스트 데이터
│     ├─ context.yaml
│     ├─ constraints.yaml
│     ├─ decisions.yaml
│     ├─ glossary.yaml
│     └─ history/2026-01-20-login.yaml
├─ VibeOps 기획서.pdf
├─ VibeOps 최종 기획서.pdf
└─ README.md
```

## ✅ 실제 구현된 기능 (코드 기준)
아래는 현재 저장소에서 확인 가능한 기능만 정리한 목록입니다.

### 1) 🧠 컨텍스트 로드 및 프롬프트 생성 (`demo/vibememory_core.py`)
- `.vibe/context.yaml`, `.vibe/constraints.yaml`, `.vibe/decisions.yaml` 로드
- `ProjectContext` 객체 구성
- AI 시스템 프롬프트 문자열 생성 (`generate_ai_prompt`)

### 2) 🛡️ 제약 조건 위반 감지 (`ConstraintChecker`)
- 텍스트에서 키워드 기반 위반 탐지
- 위반 ID/심각도/매칭 키워드/주변 컨텍스트 반환
- 사람이 읽기 쉬운 경고 메시지 포맷팅 (`format_warning`)

### 3) 🧰 CLI 초기화 기능 (`demo/vibe_cli.py`)
- `init` 명령으로 `.vibe` 템플릿 구조 생성
- `context.yaml`, `constraints.yaml`, `decisions.yaml`, `.vibeignore` 자동 생성

### 4) 🖥️ 웹 데모 (`web/index.html`)
- 문제/해결/효과 구조의 단일 페이지 데모
- 입력값 기반 5단계 파이프라인 시뮬레이션 UI
- 정책 충돌 예시와 통과 예시를 브라우저에서 시각화

## ⚠️ 현재 상태 (PoC 범위)
일부 CLI 명령은 "개념 증명 단계"로 남아 있습니다.

| 항목 | 상태 | 비고 |
|---|---|---|
| `vibe init` | 동작 | `.vibe` 초기 템플릿 생성 |
| `vibe inject` | 제한 | `VibeOps_core` 모듈 참조(현재 파일명과 불일치) |
| `vibe check <file>` | 제한 | 위와 동일한 import 경로 이슈 |
| `vibe why <file>` | 안내 출력 | 히스토리 조회 UX만 제공(실조회 미구현) |
| `vibe add-constraint` | 입력 가능 | 인터랙티브 입력 후 실제 저장은 생략 |

## 🛠️ 실행 방법

### 1) 웹 데모 실행
```bash
cd web
python -m http.server 8000
```
브라우저에서 `http://localhost:8000` 접속

### 2) 코어 데모 실행
```bash
cd demo
pip install pyyaml
set PYTHONUTF8=1
python vibememory_core.py
```

### 3) CLI 확인
```bash
cd demo
python vibe_cli.py --help
python vibe_cli.py init
```

## 🔄 5단계 파이프라인 개념
```text
SPEC -> VERIFY -> GENERATE -> VALIDATE -> DOCUMENT
```
- Spec: 요청을 구조화된 스펙으로 정리
- Verify: 기존 제약/결정과 충돌 검사
- Generate: 합의된 맥락 기반 코드 생성
- Validate: 정책/일관성/보안 검증
- Document: 스펙/결정/히스토리 기록

## 🎯 프로젝트 목표
- 바이브 코딩의 속도는 유지
- 품질 리스크(정책 위반, 재작업, 맥락 소실)는 사전 차단
- 사람 중심 리뷰를 "반복 탐색"이 아닌 "핵심 판단"에 집중

---

> 빠른 생성만으로는 부족합니다.  
> VibeOps는 실무에 적용 가능한 품질 운영체계를 탐색하는 PoC입니다.
