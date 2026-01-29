#!/usr/bin/env python3
"""
VibeMemory Core - AI 컨텍스트 영속화 시스템
개념 증명 (Proof of Concept) 코드
"""

import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


# =============================================================================
# 데이터 모델
# =============================================================================

@dataclass
class Constraint:
    """금지사항/제약조건"""
    id: str
    rule: str
    reason: str
    severity: str  # critical | warning
    scope: str
    keywords: List[str] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)


@dataclass
class Decision:
    """기술/아키텍처 결정 기록"""
    id: str
    date: str
    title: str
    decision: str
    context: str
    consequences: Dict[str, List[str]] = field(default_factory=dict)
    related_files: List[str] = field(default_factory=list)


@dataclass
class ProjectContext:
    """프로젝트 전체 컨텍스트"""
    name: str
    description: str
    tech_stack: Dict[str, Any]
    requirements: Dict[str, List[str]]
    conventions: Dict[str, Any]
    constraints: List[Constraint]
    decisions: List[Decision]


# =============================================================================
# Context Manager - 컨텍스트 로드/관리
# =============================================================================

class ContextManager:
    """프로젝트 컨텍스트 관리"""
    
    def __init__(self, vibe_dir: Path = Path(".vibe")):
        self.vibe_dir = vibe_dir
        self.context: Optional[ProjectContext] = None
        
    def load(self) -> ProjectContext:
        """
        .vibe 디렉토리에서 컨텍스트 로드
        """
        # context.yaml 로드
        context_file = self.vibe_dir / "context.yaml"
        with open(context_file, 'r', encoding='utf-8') as f:
            context_data = yaml.safe_load(f)
        
        # constraints.yaml 로드
        constraints_file = self.vibe_dir / "constraints.yaml"
        constraints = []
        if constraints_file.exists():
            with open(constraints_file, 'r', encoding='utf-8') as f:
                constraints_data = yaml.safe_load(f)
                for c in constraints_data.get('constraints', []):
                    constraints.append(Constraint(
                        id=c['id'],
                        rule=c['rule'],
                        reason=c['reason'],
                        severity=c['severity'],
                        scope=c['scope'],
                        keywords=c.get('keywords', []),
                        exceptions=c.get('exceptions', [])
                    ))
        
        # decisions.yaml 로드
        decisions_file = self.vibe_dir / "decisions.yaml"
        decisions = []
        if decisions_file.exists():
            with open(decisions_file, 'r', encoding='utf-8') as f:
                decisions_data = yaml.safe_load(f)
                for d in decisions_data.get('decisions', []):
                    decisions.append(Decision(
                        id=d['id'],
                        date=d['date'],
                        title=d['title'],
                        decision=d['decision'],
                        context=d.get('context', ''),
                        consequences=d.get('consequences', {}),
                        related_files=d.get('related_files', [])
                    ))
        
        # ProjectContext 생성
        self.context = ProjectContext(
            name=context_data['project']['name'],
            description=context_data['project']['description'],
            tech_stack=context_data.get('tech_stack', {}),
            requirements=context_data.get('requirements', {}),
            conventions=context_data.get('conventions', {}),
            constraints=constraints,
            decisions=decisions
        )
        
        return self.context
    
    def generate_ai_prompt(self) -> str:
        """
        AI 시스템 프롬프트에 주입할 컨텍스트 생성
        """
        if not self.context:
            self.load()
        
        ctx = self.context
        
        prompt_parts = [
            "# 프로젝트 컨텍스트 (VibeMemory)",
            "",
            f"## 프로젝트: {ctx.name}",
            ctx.description,
            "",
            "## 기술 스택",
        ]
        
        # 기술 스택
        for category, items in ctx.tech_stack.items():
            if isinstance(items, list):
                prompt_parts.append(f"- {category}: {', '.join(items)}")
            elif isinstance(items, dict):
                for key, value in items.items():
                    prompt_parts.append(f"- {key}: {value}")
        
        # 금지사항 (중요!)
        prompt_parts.extend([
            "",
            "## ⛔ 금지사항 (절대 위반 금지)",
            ""
        ])
        for c in ctx.constraints:
            if c.severity == 'critical':
                prompt_parts.append(f"- [{c.id}] {c.rule}")
                prompt_parts.append(f"  이유: {c.reason.strip()}")
        
        # 최근 결정 사항
        recent_decisions = ctx.decisions[:5]  # 최근 5개만
        if recent_decisions:
            prompt_parts.extend([
                "",
                "## 📋 최근 기술 결정",
                ""
            ])
            for d in recent_decisions:
                prompt_parts.append(f"- [{d.id}] {d.title}: {d.decision}")
        
        # 코딩 컨벤션
        if 'patterns' in ctx.conventions:
            prompt_parts.extend([
                "",
                "## 코딩 패턴",
                ""
            ])
            for pattern in ctx.conventions['patterns']:
                prompt_parts.append(f"- {pattern}")
        
        if 'anti_patterns' in ctx.conventions:
            prompt_parts.extend([
                "",
                "## ❌ 금지 패턴",
                ""
            ])
            for anti in ctx.conventions['anti_patterns']:
                prompt_parts.append(f"- {anti}")
        
        return "\n".join(prompt_parts)


# =============================================================================
# Constraint Checker - 제약조건 위반 감지
# =============================================================================

@dataclass
class Violation:
    """제약조건 위반 정보"""
    constraint_id: str
    rule: str
    severity: str
    matched_keyword: str
    context: str  # 위반이 발생한 텍스트 일부


class ConstraintChecker:
    """제약조건 위반 실시간 감지"""
    
    def __init__(self, constraints: List[Constraint]):
        self.constraints = constraints
    
    def check_text(self, text: str) -> List[Violation]:
        """
        텍스트(AI 응답 또는 코드)에서 제약조건 위반 감지
        """
        violations = []
        text_lower = text.lower()
        
        for constraint in self.constraints:
            for keyword in constraint.keywords:
                if keyword.lower() in text_lower:
                    # 키워드 주변 컨텍스트 추출
                    idx = text_lower.find(keyword.lower())
                    start = max(0, idx - 50)
                    end = min(len(text), idx + len(keyword) + 50)
                    context = text[start:end]
                    
                    violations.append(Violation(
                        constraint_id=constraint.id,
                        rule=constraint.rule,
                        severity=constraint.severity,
                        matched_keyword=keyword,
                        context=f"...{context}..."
                    ))
        
        return violations
    
    def format_warning(self, violations: List[Violation]) -> str:
        """위반 사항을 사람이 읽기 좋은 형식으로 변환"""
        if not violations:
            return ""
        
        lines = ["⚠️ VibeMemory 제약조건 위반 감지!", ""]
        
        for v in violations:
            icon = "🚨" if v.severity == "critical" else "⚠️"
            lines.append(f"{icon} [{v.constraint_id}] {v.rule}")
            lines.append(f"   매칭 키워드: {v.matched_keyword}")
            lines.append(f"   컨텍스트: {v.context}")
            lines.append("")
        
        lines.append("💡 조치: 프로젝트 정책에 맞게 수정하거나, 정책 예외가 필요하면 팀에 문의하세요.")
        
        return "\n".join(lines)


# =============================================================================
# Session Analyzer - 세션에서 정보 자동 추출 (개념)
# =============================================================================

class SessionAnalyzer:
    """
    AI 대화 세션에서 중요 정보 자동 추출
    
    실제 구현에서는 LLM을 사용하여 추출하지만,
    여기서는 개념만 보여줍니다.
    """
    
    @staticmethod
    def extract_decisions(conversation: str) -> List[Dict]:
        """
        대화에서 기술/설계 결정 추출
        
        실제 구현:
        - LLM에게 대화 분석 요청
        - 결정 패턴 감지 ("~하겠습니다", "~로 결정", "~를 사용")
        - 구조화된 Decision 객체 반환
        """
        # 개념 증명용 더미 구현
        return [
            {
                "type": "decision_candidate",
                "text": "대화에서 추출된 결정 사항",
                "confidence": 0.85,
                "needs_review": True
            }
        ]
    
    @staticmethod
    def extract_constraints(conversation: str) -> List[Dict]:
        """
        대화에서 새로운 금지사항 추출
        
        실제 구현:
        - "절대 ~하면 안됩니다", "~금지", "~사용하지 마세요" 패턴 감지
        - 구조화된 Constraint 객체 반환
        """
        return []
    
    @staticmethod
    def generate_session_summary(conversation: str) -> Dict:
        """
        세션 전체 요약 생성
        
        실제 구현:
        - 대화 전체를 LLM으로 요약
        - 주요 결정, 생성된 코드, 미해결 사항 추출
        """
        return {
            "objective": "세션 목표",
            "key_decisions": [],
            "code_generated": [],
            "unresolved": []
        }


# =============================================================================
# CLI 데모
# =============================================================================

def demo():
    """VibeMemory 개념 증명 데모"""
    
    print("=" * 60)
    print("🧠 VibeMemory Demo - AI 컨텍스트 영속화 시스템")
    print("=" * 60)
    print()
    
    # 1. 컨텍스트 로드
    print("[1] 프로젝트 컨텍스트 로드")
    print("-" * 40)
    
    try:
        cm = ContextManager(Path(".vibe"))
        context = cm.load()
        print(f"✅ 프로젝트: {context.name}")
        print(f"✅ 제약조건 {len(context.constraints)}개 로드")
        print(f"✅ 기술 결정 {len(context.decisions)}개 로드")
    except FileNotFoundError:
        print("⚠️ .vibe 디렉토리를 찾을 수 없습니다.")
        print("   이 데모는 .vibe 파일이 있는 프로젝트 루트에서 실행하세요.")
        return
    
    print()
    
    # 2. AI 프롬프트 생성
    print("[2] AI 시스템 프롬프트 생성")
    print("-" * 40)
    prompt = cm.generate_ai_prompt()
    print(prompt[:500] + "...\n")
    
    print()
    
    # 3. 제약조건 위반 체크 데모
    print("[3] 제약조건 위반 감지 데모")
    print("-" * 40)
    
    checker = ConstraintChecker(context.constraints)
    
    # 위반 사례 테스트
    test_cases = [
        "google-auth-library를 설치하겠습니다",
        "OAuth 로그인을 구현하겠습니다",
        "console.log('debug')로 출력하겠습니다",
        "일반적인 코드입니다"
    ]
    
    for test in test_cases:
        violations = checker.check_text(test)
        if violations:
            print(f"❌ '{test[:40]}...'")
            print(f"   → {violations[0].constraint_id}: {violations[0].rule}")
        else:
            print(f"✅ '{test[:40]}...'")
            print("   → 위반 없음")
        print()
    
    print("=" * 60)
    print("데모 완료!")
    print()
    print("💡 VibeMemory의 핵심 가치:")
    print("   1. AI 세션 시작 시 컨텍스트 자동 주입")
    print("   2. 금지사항 위반 실시간 감지")
    print("   3. 기술 결정 자동 추출 및 기록")
    print("   4. 의도와 코드의 연결 (추적성)")
    print("=" * 60)


if __name__ == "__main__":
    demo()
