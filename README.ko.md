# Opinionated Basic Claude Code Setup

Claude Code와 함께 사용하는 실전 검증된 플러그인으로, AI가 여러분의 코드베이스와 코딩 컨벤션을 자동으로 이해하고 일관된 코드를 작성하도록 돕습니다.

## 이 플러그인이 해결하는 문제

Claude Code로 작업할 때 이런 경험 있으신가요?

- 코딩 컨벤션과 스타일을 매번 설명해야 함
- 프로젝트별 패턴과 아키텍처 결정사항을 반복 설명
- 언어별 베스트 프랙티스를 계속 알려줘야 함
- 파일 인코딩 오류로 코드가 깨짐

이 플러그인은 **적절한 시점에 자동으로 올바른 컨텍스트를 주입**하여 Claude가 항상 다음을 알 수 있게 합니다:
- 각 언어로 코드를 어떻게 작성하는지
- 프로젝트 컨벤션이 무엇인지
- 파일에 인코딩 문제가 있는지

## 핵심 철학: Opinionated by Design

이 플러그인은 범용 도구가 아닙니다. **실전에서 검증된 구체적인 코딩 컨벤션**을 담고 있으며, 다음 영역에 대한 베스트 프랙티스를 제공합니다:

- **타입 안전한 Python 개발** - async-first 패턴 적용
- **Modern Svelte 5** - 올바른 rune 사용법
- **프로젝트 지식 관리** - 팀 일관성 유지

이 의견들이 여러분의 워크플로우와 맞는다면 즉시 가치를 얻을 수 있습니다. 그렇지 않다면 언어 가이드를 쉽게 커스터마이징할 수 있습니다.

---

## 플러그인 구성 요소

### 1. 언어별 가이드 자동 주입 (Language-Specific Guide Injection)

#### 무엇을 하나요?

지원하는 언어로 작성된 파일을 읽거나 쓸 때, 해당 언어의 코딩 가이드를 자동으로 주입합니다.

#### 왜 필요한가요?

**문제점:**
```
사용자: "이 Python 함수를 수정해줘"
Claude: *잘못된 스타일로 코드 작성*
사용자: "아니야, 우린 모든 곳에 타입 힌트를 쓴다고"
Claude: "아, 알겠습니다. 수정할게요..."
사용자: "그리고 Django ORM은 async-first 패턴으로 써야 해"
Claude: "네, 업데이트하겠습니다..."
사용자: "그리고 pytest 컨벤션도 있는데..."
```

**해결책:**
```
사용자: "이 Python 함수를 수정해줘"
Claude: *자동으로 모든 Python 컨벤션을 숙지함*
Claude: *첫 시도부터 스타일에 맞는 완벽한 코드 작성*
```

#### 현재 지원 언어

**Python (`py.md`)**
- **타입 안전성**: 모든 함수에 타입 힌트 강제, `-> Any` 금지
- **Async-First Django**: 올바른 async ORM 패턴, eager loading 전략
- **테스트 표준**: pytest 컨벤션, AAA 패턴, fixture 배치 규칙
- **패키지 관리**: 최신 프로젝트는 uv, 레거시는 poetry
- **코드 스타일**: 축약 금지, 명시적 네이밍, nested import 금지

**왜 이런 규칙들인가요?**
- 타입 힌트는 프로덕션이 아닌 개발 시점에 버그를 잡아냅니다
- Async-first는 Django에서 성능 병목을 방지합니다
- Pytest 컨벤션은 유지보수 가능한 테스트 스위트를 보장합니다
- uv는 레거시 도구보다 빠르고 안정적입니다
- 명시적 네이밍은 팀 코드 가독성을 향상시킵니다

**Svelte (`svelte.md`)**
- **Svelte 5 Runes**: `$state`, `$derived`, `$effect` 올바른 사용법
- **반응성 패턴**: 프록시 관련 흔한 실수 회피
- **컴포넌트 베스트 프랙티스**: Props, 상태 관리, 라이프사이클
- **SvelteKit 통합**: 라우팅, load 함수, form action

**왜 Svelte 5인가요?**
- Runes는 Svelte의 미래입니다 (Svelte 4 문법은 레거시)
- 흔한 실수들 (반응형 프록시 destructuring 등)이 미묘한 버그를 만듭니다
- SvelteKit 패턴은 다른 프레임워크와 크게 다릅니다

#### 커스터마이징: 새 언어 추가하기

1. **가이드 파일 생성:**
```bash
touch modular-prompts/languages/go.md
```

2. **컨벤션 작성:**
```markdown
<style>
    <naming>
        변수는 camelCase 사용
        클래스는 PascalCase 사용
    </naming>

    <patterns>
        항상 composition over inheritance
        불변성(immutability) 선호
    </patterns>

    <errors>
        에러 즉시 체크:
        ```go
        if err != nil {
            return fmt.Errorf("failed to X: %w", err)
        }
        ```

        이유: 체크하지 않은 에러는 조용한 실패를 야기합니다
    </errors>
</style>
```

3. **테스트:**
```bash
# 해당 확장자 파일 읽기만 하면 됩니다
claude> 이 TypeScript 파일 리뷰해줘
# 가이드가 자동으로 주입됩니다
```

**핵심 포인트:**
- 파일명이 `{확장자}.md` 형식이어야 합니다 (예: `ts.md`는 `.ts` 파일에 적용)
- 전역 가이드 (`~/.claude/modular-prompts/languages/`)가 플러그인 가이드보다 우선
- 세션당 한 번만 주입 (중복 방지)

---

### 2. 프로젝트 지식 자동 주입 (Project Knowledge Injection)

#### 무엇을 하나요?

프로젝트의 `claude.md`와 `agents.md` 파일을 자동으로 찾아서 주입합니다.

#### 왜 필요한가요?

**문제점:**
- 팀이 아키텍처 결정사항을 `claude.md`에 문서화함
- 신규 기여자는 이 파일의 존재를 모름
- Claude는 자동으로 읽지 않음
- 같은 컨텍스트를 반복 설명
- 팀 일관성 저하

**해결책:**
플러그인이 작업 중인 파일에서 프로젝트 루트까지 올라가며 자동으로 발견:
- `claude.md`: 프로젝트 전체 컨벤션, 아키텍처, 패턴
- `agents.md`: Agent별 워크플로우, 자동화 규칙

**스마트 디스커버리:**
```
your-project/
├── claude.md                    <- 루트 레벨 프로젝트 지식
├── backend/
│   ├── claude.md                <- 백엔드 전용 규칙
│   └── api/
│       └── users.py             <- 여기서 작업 중
```

`users.py`에서 작업하면 두 개의 `claude.md`가 모두 주입되며, 더 가까운 파일이 우선순위를 가집니다.

#### 실전 사용 예시

**유스케이스 1: 온보딩**
```markdown
# claude.md

## 아키텍처
우리는 헥사고날 아키텍처를 사용하며 다음 레이어를 따릅니다:
- Domain: 순수 비즈니스 로직
- Application: 유스케이스
- Infrastructure: 외부 의존성

절대 Domain에서 Infrastructure를 import하지 마세요!
```

이제 Claude가 자동으로 여러분의 아키텍처 경계를 존중합니다.

**유스케이스 2: Agent 자동화**
```markdown
# agents.md

## 코드 리뷰 Agent
항상 체크:
1. 타입 커버리지 > 95%
2. console.log 문 없음
3. 모든 public 함수에 테스트
```

Agent들이 자동으로 여러분의 리뷰 기준을 따릅니다.

#### 중복 제거 전략

**문제:** 중복 제거 없이는 세션당 여러 번 같은 내용이 주입됩니다.

**해결책:**
- 각 파일은 `[knowledge:{path}:{hash}:{modified}]`로 식별
- 해시 변경 시 재주입 (파일을 수정했을 때)
- Transcript를 체크하여 중복 주입 방지
- 세션당 고유한 파일 버전당 한 번만 주입

#### 커스터마이징

**더 많은 지식 파일 추가:**

`hooks/post-tool-use/inject_knowledge.py`에서 `KNOWLEDGE_FILES` 수정:
```python
class KnowledgeFinder:
    KNOWLEDGE_FILES = ["claude.md", "agents.md", "ARCHITECTURE.md", "CONVENTIONS.md"]
```

**프로젝트 루트 마커 추가:**

프로젝트 루트 감지 기준을 수정하려면 `inject_knowledge.py`의 `_find_project_root()` 메서드 수정:
```python
def _find_project_root(self) -> Path:
    markers = [".git", "pyproject.toml", "package.json", ".venv", "go.mod"]  # 원하는 마커 추가
    # ...
```

---

### 3. 인코딩 검증 (Encoding Validation)

#### 무엇을 하나요?

Write 작업 후 파일을 검증하여 인코딩 손상을 즉시 잡아냅니다.

#### 왜 필요한가요?

**문제점:**
LLM이 생성한 텍스트가 출력에서는 괜찮아 보이지만 파일로 쓸 때 손상되는 경우:
- 유니코드 교체 문자 (U+FFFD)
- 바이너리 데이터를 텍스트로 기록
- 잘못된 인코딩 가정
- 텍스트 파일에 null byte

**실제 사례:**
```python
# Claude가 작성했다고 생각한 것:
name = "user"

# 실제로 기록된 것:
name = "us\ufffd\ufffdr"
```

이는 컴파일되지만 런타임에 알 수 없는 에러로 깨집니다.

**해결책:**
모든 write 후 플러그인이:
1. MIME 타입 체크 (바이너리 파일 감지)
2. Null byte 스캔 (강력한 손상 지표)
3. UTF-8 디코딩 검증
4. 교체 문자 감지
5. chardet으로 대체 인코딩 시도

**문제 발견 시:**
```
WARNING: ENCODING ISSUES DETECTED: output.json
The file contains encoding issues (1 problems found).
Please use Read() to review the file and rewrite it from scratch.
```

Claude가 즉시 수정해야 함을 알고, 손상된 코드가 코드베이스에 들어가는 것을 방지합니다.

#### 검사 항목

**바이너리 파일 감지:**
```bash
file --mime-type output.bin
# application/octet-stream -> WARNING
```

**Null Byte 감지:**
```python
if b'\x00' in file_bytes:
    # 바이너리 파일이 텍스트로 기록됨!
```

**UTF-8 검증:**
```python
try:
    content = raw_bytes.decode('utf-8')
    if '\ufffd' in content:
        # 교체 문자는 손상을 나타냄
except UnicodeDecodeError:
    # chardet으로 인코딩 식별 시도
```

#### 커스터마이징

**검사 비활성화 (특정 파일 타입):**

`check_corrupted_encoding.py`의 MIME 타입 체크 부분 수정:
```python
# 특정 MIME 타입을 안전한 것으로 간주
if not mime_type.startswith("text/") and mime_type not in [
    "inode/x-empty",
    "application/json",
    "application/javascript",  # 추가
    "application/xml"  # 추가
]:
```

**완전히 비활성화:**

`hooks/hooks.json`에서 해당 hook 제거:
```json
{
  "PostToolUse": [
    // 이 부분 제거 또는 주석 처리:
    // {
    //   "blocking": true,
    //   "description": "Validates file encoding...",
    //   "name": "check_corrupted_encoding",
    //   "script": "...",
    //   "triggers": ["Write", "Edit", "MultiEdit", "NotebookEdit"]
    // }
  ]
}
```

---

### 4. 정적 분석 체커 (Static Check)

#### 무엇을 하나요?

코드 작성 시 언어별 정적 분석 도구를 자동 실행합니다.

#### 왜 필요한가요?

**문제점:**
- Claude가 코드를 작성하지만 linter나 type checker를 거치지 않음
- 작성 후에 수동으로 검사해야 함
- 작은 실수들이 누적됨

**해결책:**
코드 작성 즉시 자동으로:
- **Python**: Ruff (linting) + basedpyright (타입 체킹) + 커스텀 규칙
- **TypeScript**: TypeScript 컴파일러 + ESLint
- **Terraform**: terraform validate

#### 지원 언어 및 체커

**Python 파이프라인:**
1. `python_1_opinionated.py` - 커스텀 규칙 (6개 체커)
   - `-> Any` 리턴 타입 금지
   - 불필요한 주석 감지
   - match-case 권장
   - nested import 금지
   - TypedDict total=False 금지
   - `__init__.py` 명시적 re-export 강제

2. `python_2_ruff.py` - Ruff linter
   - 자동 수정 가능한 이슈 자동 적용
   - 남은 이슈 리포트

3. `python_3_basedpyright.py` - 타입 체킹
   - 타입 에러 감지
   - 타입 커버리지 리포트

**TypeScript:**
- TSC 컴파일러 체크
- 타입 에러 리포트

**Terraform:**
- terraform validate
- 구성 검증

#### 커스터마이징

**새 언어 체커 추가:**

1. `hooks/post-tool-use/static_check/{language}.py` 생성
2. 표준 입력으로 PostToolUse 데이터 받기
3. 종료 코드로 결과 전달:
   - `0`: 문제 없음
   - `2`: Claude에게 알려야 할 문제 발견

**예시 - Go 체커:**
```python
#!/usr/bin/env python3
# hooks/post-tool-use/static_check/go.py

import json
import subprocess
import sys
from pathlib import Path

def main():
    data = json.loads(sys.stdin.read())
    file_path = data["tool_input"]["file_path"]

    # go fmt 실행
    result = subprocess.run(
        ["gofmt", "-l", file_path],
        capture_output=True,
        text=True
    )

    if result.stdout.strip():
        print(f"Go formatting issues in {file_path}", file=sys.stderr)
        print("Please run: gofmt -w {file_path}", file=sys.stderr)
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
```

**체커 비활성화:**

`hooks/hooks.json`에서 static_check hook 제거 또는 주석 처리

---

### 5. Terminalcp 도우미 (Terminalcp Helpers)

#### 무엇을 하나요?

두 개의 hook으로 terminalcp MCP 서버 사용을 돕습니다:

1. **suggest_terminalcp_for_bash**: Bash 사용 시 terminalcp 제안
2. **terminalcp_list_on_start**: terminalcp 세션 시작 시 활성 세션 목록 표시

#### 왜 필요한가요?

**문제점:**
- Bash는 인터랙티브 프로세스 (REPL, 디버거 등)에 적합하지 않음
- 긴 실행 프로세스 관리 어려움
- stdin/stdout 상호작용 제한적

**해결책:**
terminalcp는 적절한 터미널 에뮬레이션을 제공하여:
- 인터랙티브 프로세스 지원
- 백그라운드 프로세스 관리
- 세션 모니터링

#### 동작 방식

**suggest_terminalcp_for_bash:**
- Bash 도구 사용 시 한 번만 제안 표시
- Transcript 체크로 중복 방지
- 유용한 사용 예제 제공

**terminalcp_list_on_start:**
- terminalcp 세션 시작 시 자동 실행
- 현재 활성 세션 목록 표시
- CLI로 attach하는 방법 안내

#### 커스터마이징

**제안 비활성화:**

`hooks/hooks.json`에서 해당 hook들 제거:
```json
{
  "PostToolUse": [
    // 제거:
    // { "name": "suggest_terminalcp_for_bash", ... },
    // { "name": "terminalcp_list_on_start", ... }
  ]
}
```

---

### 6. TODO 완료 체크 (Stop Hook)

#### 무엇을 하나요?

대화 종료 시 미완료 TODO가 있으면 중단을 차단합니다.

#### 왜 필요한가요?

**문제점:**
- Claude가 작업 중간에 멈춤
- 사용자가 미완료 작업을 놓침
- 일관성 없는 작업 완료

**해결책:**
Stop hook이:
1. 세션의 TODO 파일 읽기 (`~/.claude/todos/{session_id}-agent-{session_id}.json`)
2. `pending` 또는 `in_progress` 상태 항목 찾기
3. 있으면 중단 차단하고 목록 표시

#### 동작 예시

```
[Stop Hook] You still have unresolved TODO items:

  [in_progress] Run tests and fix failures
  [pending] Update documentation

Please complete all tasks before stopping.
If you believe all tasks are done, mark them as 'completed' using TodoWrite.
```

#### 커스터마이징

**비활성화:**

`hooks/hooks.json`에서 Stop hook 제거:
```json
{
  "Stop": [
    // 제거:
    // { "name": "check_todos_completed", ... }
  ]
}
```

**TODO 파일 경로 수정:**

`hooks/stop/check_todos_completed.py`의 `get_todos_from_file()` 수정

---

## MCP 서버 구성

### 포함된 MCP 서버

**1. context7**
- **목적**: 라이브러리 문서 검색
- **사용법**: 최신 API 문서, 버전 정보, breaking change 조회
- **명령어**: `bunx --bun -y @upstash/context7-mcp`

**2. terminalcp**
- **목적**: 터미널 에뮬레이션
- **사용법**: 인터랙티브 프로세스, 백그라운드 작업 관리
- **명령어**: `npx @mariozechner/terminalcp@latest --mcp`

### 커스터마이징

**새 MCP 서버 추가:**

`.mcp.json` 수정:
```json
{
  "mcpServers": {
    "context7": { ... },
    "terminalcp": { ... },
    "your-server": {
      "type": "stdio",
      "command": "npx",
      "args": ["your-package"],
      "env": {}
    }
  }
}
```

**MCP 서버 제거:**

`.mcp.json`에서 해당 서버 항목 삭제

---

## 설치

### 빠른 시작

```bash
# Claude Code 플러그인 디렉토리에 클론
git clone https://github.com/code-yeongyu/opinionated-basic-cc-setup \
    ~/.claude/plugins/opinionated-basic-cc-setup
```

### 설치 확인

```bash
ls ~/.claude/plugins/opinionated-basic-cc-setup/
# 보여야 할 것: .claude-plugin/, hooks/, modular-prompts/, .mcp.json
```

Claude Code를 재시작하면 플러그인이 자동으로 활성화됩니다.

---

## 사용 예시

### 예시 1: Python 개발

```bash
# Django 뷰 작업 시작
claude> 유저 프로필용 API 엔드포인트 추가해줘

# 플러그인이 py.md 자동 주입:
# - 타입 힌트 필수
# - Django ORM은 async for 사용
# - pytest 네이밍 컨벤션
# - alist() 메서드 없음

# Claude가 작성:
async def get_user_profile(request: HttpRequest, user_id: int) -> JsonResponse:
    user = await User.objects.select_related('profile').aget(id=user_id)
    # ... 올바르게 타입 지정되고 async-first인 코드
```

**플러그인 없이:** Claude가 `alist()` (존재하지 않음) 사용, 타입 힌트 누락, sync 패턴 사용 가능

### 예시 2: Svelte 컴포넌트

```bash
claude> 반응형 카운터 컴포넌트 만들어줘

# 플러그인이 svelte.md 주입:
# - Svelte 5 runes 사용
# - 반응형 프록시 destructure 금지
# - $state로 반응성 구현

# Claude가 작성:
<script>
  let count = $state(0);
  const double = $derived(count * 2);
</script>

<button onclick={() => count++}>
  Count: {count}, Double: {double}
</button>
```

**플러그인 없이:** 구식 Svelte 4 문법 사용하거나 반응성 실수 가능

### 예시 3: 프로젝트 인지 리팩토링

```markdown
<!-- 프로젝트의 claude.md -->
# 아키텍처

Repository 패턴 사용:
- 모든 데이터베이스 접근은 repository를 통해
- 뷰에서 절대 ORM 직접 사용 금지
- Repository는 `repositories/` 디렉토리에
```

```bash
claude> 이 뷰를 깔끔하게 리팩토링해줘

# 플러그인이 자동으로 claude.md 주입
# Claude가 repository 패턴으로 리팩토링:

async def get_users(request: HttpRequest) -> JsonResponse:
    repository = UserRepository()
    users = await repository.find_all()
    return JsonResponse({'users': [u.dict() for u in users]})
```

**플러그인 없이:** 아키텍처를 모르고 리팩토링하여 패턴 위반 가능

---

## 내부 동작 원리

### Hook 실행 파이프라인

```
Read/Write/Edit 도구 실행
    ↓
PostToolUse Hook 트리거
    ↓
├─→ inject_language_guide
│   ├─→ 확장자 추출 (.py)
│   ├─→ 가이드 찾기 (py.md)
│   ├─→ Transcript 체크
│   └─→ 미주입시 주입
│
├─→ inject_knowledge
│   ├─→ 프로젝트 루트 찾기
│   ├─→ claude.md/agents.md 탐색
│   ├─→ 해시로 중복 체크
│   └─→ 거리순 주입
│
├─→ check_corrupted_encoding
│   ├─→ MIME 타입 체크
│   ├─→ Null byte 스캔
│   ├─→ UTF-8 검증
│   └─→ 문제 발견시 경고
│
└─→ static_check
    ├─→ 언어 감지
    ├─→ 체커 실행
    └─→ 결과 리포트
```

### 우선순위 시스템

**언어 가이드:**
```
1. ~/.claude/modular-prompts/languages/py.md  (전역, 최우선)
2. plugin/modular-prompts/languages/py.md     (플러그인 기본값)
```

**정적 체커:**
```
1. ~/.claude/hooks/post-tool-use/static_check/python.py  (전역)
2. plugin/hooks/post-tool-use/static_check/python.py     (플러그인)
```

이를 통해 전역 커스터마이징이 플러그인 기본값을 오버라이드합니다.

---

## 문제 해결

### 가이드가 주입되지 않음

**체크 1: 파일 존재 확인**
```bash
ls modular-prompts/languages/py.md
```

**체크 2: 이미 주입됨**
- 가이드는 세션당 한 번만 주입
- 새 Claude Code 세션을 시작하여 재주입

**체크 3: 파일 확장자 매칭**
- `py.md`는 `.py` 파일과 매칭
- `svelte.md`는 `.svelte` 파일과 매칭
- 확장자가 가이드 파일명과 일치해야 함

### 지식 파일을 찾지 못함

**체크 1: 정확한 이름**
```bash
# 정확히 일치해야 함:
claude.md  # CLAUDE.md나 Claude.md 아님
agents.md  # AGENTS.md나 Agents.md 아님
```

**체크 2: 프로젝트 계층 구조 내**
```
project-root/
├── .git/          <- 프로젝트 루트 마커
└── claude.md      <- 여기 또는 하위에 있어야 함
```

**체크 3: 프로젝트 루트 감지**
플러그인이 찾는 것:
- `.git/`
- `pyproject.toml`
- `package.json`
- `.venv/`

### 인코딩 체크 오탐지

**유효한 파일에 경고가 나오면:**

1. 실제 파일 확인:
```bash
file --mime-type yourfile.txt
hexdump -C yourfile.txt | head
```

2. 파일이 실제로 유효하다면 hook이 너무 엄격할 수 있습니다:
```json
// hooks/hooks.json에서 인코딩 체크 비활성화
{
  "PostToolUse": [
    // 제거하거나 주석 처리:
    // { "name": "check_corrupted_encoding", ... }
  ]
}
```

---

## FAQ

**Q: Claude 속도가 느려지나요?**
A: 아니요. 가이드는 세션당 한 번만 주입됩니다. 초기 주입 후에는 오버헤드가 없습니다.

**Q: 다른 에디터에서 사용할 수 있나요?**
A: Claude Code 전용입니다. 개념은 다른 AI 코딩 도구에 적용할 수 있습니다.

**Q: Python 컨벤션에 동의하지 않으면?**
A: 포크하여 `modular-prompts/languages/py.md`를 선호도에 맞게 커스터마이징하세요.

**Q: Claude Code 프로젝트에서 작동하나요?**
A: 네! 주요 사용 사례입니다.

**Q: 특정 hook을 비활성화할 수 있나요?**
A: 네, `hooks/hooks.json`을 편집하여 원하지 않는 hook을 제거/주석 처리하세요.

**Q: 플러그인 업데이트 방법은?**
```bash
cd ~/.claude/plugins/opinionated-basic-cc-setup
git pull origin master
```

**Q: 상업적으로 사용할 수 있나요?**
A: 네, MIT 라이선스입니다. 어떤 프로젝트에서든 자유롭게 사용하세요.

---

## 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

## 크레딧

**제작:** [@code-yeongyu](https://github.com/code-yeongyu)

**빌드 도구:** [Claude Code](https://claude.com/claude-code)

**영감:** AI 지원 개발에서 컨텍스트 관리의 실전 불편함

---

## 기여

### 언어 가이드 추가

새로운 언어 가이드 기여를 환영합니다!

**좋은 가이드의 조건:**
- 구체적이고 실행 가능한 규칙
- 실전 경험 기반
- 무엇뿐만 아니라 왜 설명
- 흔한 함정 다룸

**예시 기여:**
```markdown
<!-- modular-prompts/languages/rust.md -->
<style>
    <ownership>
        항상 소유권 규칙 준수:
        ```rust
        let s1 = String::from("hello");
        let s2 = s1;  // s1은 이제 무효
        // println!("{}", s1);  // 에러!
        ```

        이유: Rust의 메모리 안전성 핵심
    </ownership>

    <error-handling>
        Result 타입으로 에러 처리:
        ```rust
        fn read_file() -> Result<String, io::Error> {
            let contents = fs::read_to_string("file.txt")?;
            Ok(contents)
        }
        ```

        이유: 명시적 에러 처리가 견고성 향상
    </error-handling>
</style>
```

### 기존 가이드 개선

더 나은 패턴을 발견했거나 흔한 실수를 찾았다면:

1. 레포 포크
2. 관련 `.md` 파일 업데이트
3. 설명과 함께 PR 제출

### 버그 리포트

다음을 포함하여 이슈 열기:
- 무엇이 발생했는지
- 무엇을 기대했는지
- 최소 재현 단계
