#!/usr/bin/env python3
"""
VibeOps CLI - 명령줄 인터페이스
개념 증명 (Proof of Concept)

사용법:
  vibe init              - 새 프로젝트에 .vibe 초기화
  vibe inject            - AI 프롬프트용 컨텍스트 출력
  vibe check <file>      - 파일에서 제약조건 위반 검사
  vibe why <file>        - 파일의 의도/히스토리 조회
  vibe add-constraint    - 새 제약조건 추가
  vibe add-decision      - 새 기술 결정 추가
"""

import argparse
import sys
from pathlib import Path


def cmd_init(args):
    """새 프로젝트에 .vibe 디렉토리 초기화"""
    vibe_dir = Path(".vibe")
    
    if vibe_dir.exists():
        print("⚠️ .vibe 디렉토리가 이미 존재합니다.")
        return
    
    # 디렉토리 생성
    vibe_dir.mkdir()
    (vibe_dir / "history").mkdir()
    
    # 기본 context.yaml 생성
    context_template = '''# VibeOps 프로젝트 컨텍스트
version: "1.0"

project:
  name: "프로젝트명"
  description: |
    프로젝트 설명을 여기에 작성하세요.

tech_stack:
  languages:
    - Python 3.11
  frameworks:
    - FastAPI

requirements:
  must_have:
    - "필수 요구사항을 여기에 작성"
  nice_to_have:
    - "권장 사항"

conventions:
  patterns:
    - "사용할 패턴"
  anti_patterns:
    - "금지할 패턴"
'''
    
    (vibe_dir / "context.yaml").write_text(context_template, encoding='utf-8')
    
    # 기본 constraints.yaml 생성
    constraints_template = '''# VibeOps 제약조건
version: "1.0"

constraints:
  - id: "C001"
    rule: "예시: 외부 API 직접 호출 금지"
    reason: "모든 외부 통신은 서비스 레이어를 통해야 함"
    severity: warning
    scope: "전체"
    keywords:
      - "requests.get"
      - "fetch("
    exceptions: []
'''
    
    (vibe_dir / "constraints.yaml").write_text(constraints_template, encoding='utf-8')
    
    # 기본 decisions.yaml 생성
    decisions_template = '''# VibeOps 기술 결정 기록
version: "1.0"

decisions:
  - id: "D001"
    date: "날짜"
    title: "첫 번째 기술 결정"
    status: "accepted"
    context: "결정 배경"
    decision: "결정 내용"
    consequences:
      positive:
        - "장점"
      negative:
        - "단점"
    related_files: []
'''
    
    (vibe_dir / "decisions.yaml").write_text(decisions_template, encoding='utf-8')
    
    # .vibeignore 생성
    (vibe_dir / ".vibeignore").write_text('''# AI 주입에서 제외할 패턴
history/*.yaml
''', encoding='utf-8')
    
    print("✅ VibeOps 초기화 완료!")
    print()
    print("📁 생성된 파일:")
    print("   .vibe/context.yaml      - 프로젝트 컨텍스트")
    print("   .vibe/constraints.yaml  - 제약조건/금지사항")
    print("   .vibe/decisions.yaml    - 기술 결정 기록")
    print("   .vibe/history/          - 세션 히스토리")
    print()
    print("💡 다음 단계:")
    print("   1. .vibe/context.yaml 수정 (프로젝트 정보)")
    print("   2. .vibe/constraints.yaml 수정 (금지사항)")
    print("   3. 'vibe inject'로 AI 프롬프트 확인")


def cmd_inject(args):
    """AI 프롬프트용 컨텍스트 출력"""
    try:
        # VibeOps_core에서 ContextManager import (실제 구현 시)
        from VibeOps_core import ContextManager
        
        cm = ContextManager()
        cm.load()
        prompt = cm.generate_ai_prompt()
        
        if args.output:
            Path(args.output).write_text(prompt, encoding='utf-8')
            print(f"✅ 컨텍스트가 {args.output}에 저장되었습니다.")
        else:
            print(prompt)
            
    except ImportError:
        print("⚠️ VibeOps_core를 import할 수 없습니다.")
        print("   demo 디렉토리에서 실행하세요.")
    except FileNotFoundError:
        print("⚠️ .vibe 디렉토리를 찾을 수 없습니다.")
        print("   'vibe init'으로 초기화하세요.")


def cmd_check(args):
    """파일에서 제약조건 위반 검사"""
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return
    
    try:
        from VibeOps_core import ContextManager, ConstraintChecker
        
        cm = ContextManager()
        context = cm.load()
        checker = ConstraintChecker(context.constraints)
        
        content = file_path.read_text(encoding='utf-8')
        violations = checker.check_text(content)
        
        if violations:
            print(f"❌ {file_path}에서 제약조건 위반 발견!")
            print()
            print(checker.format_warning(violations))
        else:
            print(f"✅ {file_path}: 제약조건 위반 없음")
            
    except ImportError:
        print("⚠️ VibeOps_core를 import할 수 없습니다.")


def cmd_why(args):
    """파일의 의도/히스토리 조회"""
    file_path = args.file
    
    print(f"📜 {file_path} 히스토리")
    print("-" * 50)
    print()
    
    # 실제 구현에서는 history/*.yaml을 검색하여
    # 해당 파일이 생성/수정된 세션 정보를 찾아 표시
    
    print("ℹ️ 이 기능은 세션 히스토리가 축적된 후 사용 가능합니다.")
    print()
    print("💡 히스토리에서 찾을 수 있는 정보:")
    print("   • 파일이 생성된 세션")
    print("   • 생성 의도/목적")
    print("   • 관련 기술 결정")
    print("   • 원본 대화 요약")


def cmd_add_constraint(args):
    """새 제약조건 추가 (인터랙티브)"""
    print("🆕 새 제약조건 추가")
    print("-" * 30)
    
    rule = input("금지사항: ")
    reason = input("이유: ")
    severity = input("심각도 (critical/warning) [warning]: ") or "warning"
    scope = input("적용 범위 [전체]: ") or "전체"
    keywords = input("감지 키워드 (쉼표 구분): ").split(",")
    keywords = [k.strip() for k in keywords if k.strip()]
    
    print()
    print("📋 추가할 제약조건:")
    print(f"   규칙: {rule}")
    print(f"   이유: {reason}")
    print(f"   심각도: {severity}")
    print(f"   범위: {scope}")
    print(f"   키워드: {keywords}")
    print()
    
    confirm = input("추가하시겠습니까? (y/n): ")
    if confirm.lower() == 'y':
        print("✅ 제약조건이 추가되었습니다. (개념 증명 - 실제 저장 생략)")
    else:
        print("❌ 취소되었습니다.")


def main():
    parser = argparse.ArgumentParser(
        description="VibeOps CLI - AI 컨텍스트 영속화 시스템",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  vibe init                  # 새 프로젝트 초기화
  vibe inject                # AI 프롬프트 컨텍스트 출력
  vibe inject -o prompt.txt  # 파일로 저장
  vibe check src/auth.py     # 제약조건 위반 검사
  vibe why src/login.py      # 파일 히스토리 조회
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="명령")
    
    # init
    parser_init = subparsers.add_parser("init", help="새 프로젝트에 .vibe 초기화")
    
    # inject
    parser_inject = subparsers.add_parser("inject", help="AI 프롬프트용 컨텍스트 출력")
    parser_inject.add_argument("-o", "--output", help="출력 파일 경로")
    
    # check
    parser_check = subparsers.add_parser("check", help="파일에서 제약조건 위반 검사")
    parser_check.add_argument("file", help="검사할 파일 경로")
    
    # why
    parser_why = subparsers.add_parser("why", help="파일의 의도/히스토리 조회")
    parser_why.add_argument("file", help="조회할 파일 경로")
    
    # add-constraint
    parser_ac = subparsers.add_parser("add-constraint", help="새 제약조건 추가")
    
    args = parser.parse_args()
    
    if args.command == "init":
        cmd_init(args)
    elif args.command == "inject":
        cmd_inject(args)
    elif args.command == "check":
        cmd_check(args)
    elif args.command == "why":
        cmd_why(args)
    elif args.command == "add-constraint":
        cmd_add_constraint(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
