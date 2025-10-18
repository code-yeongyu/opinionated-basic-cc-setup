# Opinionated Basic Claude Code Setup

A production-tested Claude Code plugin that helps AI automatically understand your codebase and coding conventions to write consistent code.

## Problems This Plugin Solves

Ever experienced this while working with Claude Code?

- Having to repeatedly explain coding conventions and style preferences
- Re-explaining project-specific patterns and architecture decisions
- Constantly reminding about language-specific best practices
- Code breaking due to file encoding errors

This plugin **automatically injects the right context at the right time**, so Claude always knows:
- How to write code in each language
- What your project conventions are
- When files have encoding issues

## Core Philosophy: Opinionated by Design

This isn't a generic plugin. It contains **specific, production-tested coding conventions** refined through real-world usage, providing best practices for:

- **Type-safe Python development** - with async-first patterns
- **Modern Svelte 5** - with proper rune usage
- **Project knowledge management** - for team consistency

If these opinions align with your workflow, you'll get immediate value. If not, you can easily customize the language guides to match your preferences.

---

## Plugin Components

### 1. Language-Specific Guide Auto-Injection

#### What does it do?

Automatically injects coding guides for supported languages when you read or write files.

#### Why do you need it?

**The Problem:**
```
You: "Fix this Python function"
Claude: *writes code with wrong style*
You: "No, we use type hints everywhere"
Claude: "Oh, let me fix that..."
You: "Also we use async-first patterns with Django ORM"
Claude: "Got it, updating..."
You: "And we have these pytest conventions..."
```

**The Solution:**
```
You: "Fix this Python function"
Claude: *automatically knows all your Python conventions*
Claude: *writes perfect code matching your style on first try*
```

#### Currently Supported Languages

**Python (`py.md`)**
- **Type Safety**: Enforce type hints on all functions, prohibit `-> Any`
- **Async-First Django**: Proper async ORM patterns, eager loading strategies
- **Testing Standards**: pytest conventions, AAA pattern, fixture placement rules
- **Package Management**: uv for modern projects, poetry for legacy
- **Code Style**: No abbreviations, explicit naming, no nested imports

**Why these specific rules?**
- Type hints catch bugs at development time, not production
- Async-first prevents performance bottlenecks in Django
- Pytest conventions ensure maintainable test suites
- uv is faster and more reliable than legacy tools
- Explicit naming improves code readability for teams

**Svelte (`svelte.md`)**
- **Svelte 5 Runes**: Proper `$state`, `$derived`, `$effect` usage
- **Reactivity Patterns**: Avoiding common proxy-related pitfalls
- **Component Best Practices**: Props, state management, lifecycle
- **SvelteKit Integration**: Routing, load functions, form actions

**Why Svelte 5 specifically?**
- Runes are the future of Svelte (Svelte 4 syntax is legacy)
- Common mistakes (destructuring reactive proxies) cause subtle bugs
- SvelteKit patterns differ significantly from other frameworks

#### Customization: Adding New Languages

1. **Create guide file:**
```bash
touch modular-prompts/languages/go.md
```

2. **Write conventions:**
```markdown
<style>
    <naming>
        Use camelCase for variables
        Use PascalCase for classes
    </naming>

    <patterns>
        Always use composition over inheritance
        Prefer immutability
    </patterns>

    <errors>
        Check errors immediately:
        ```go
        if err != nil {
            return fmt.Errorf("failed to X: %w", err)
        }
        ```

        Why: Unchecked errors cause silent failures
    </errors>
</style>
```

3. **Test:**
```bash
# Just read any file with that extension
claude> Review this TypeScript file
# Guide auto-injects
```

**Key Points:**
- Filename must be `{extension}.md` format (e.g., `ts.md` applies to `.ts` files)
- Global guides (`~/.claude/modular-prompts/languages/`) take priority over plugin guides
- Injected once per session (prevents duplication)

---

### 2. Project Knowledge Auto-Injection

#### What does it do?

Automatically finds and injects `claude.md` and `agents.md` files from your project.

#### Why do you need it?

**The Problem:**
- Team documents architecture decisions in `claude.md`
- New contributors don't know this file exists
- Claude doesn't automatically read it
- You repeatedly re-explain the same context
- Team consistency suffers

**The Solution:**
Plugin walks up from working file to project root, automatically discovering:
- `claude.md`: Project-wide conventions, architecture, patterns
- `agents.md`: Agent-specific workflows, automation rules

**Smart Discovery:**
```
your-project/
├── claude.md                    <- Root-level project knowledge
├── backend/
│   ├── claude.md                <- Backend-specific rules
│   └── api/
│       └── users.py             <- Working here
```

When working on `users.py`, both `claude.md` files are injected, with closer files prioritized.

#### Real-World Use Cases

**Use Case 1: Onboarding**
```markdown
# claude.md

## Architecture
We use hexagonal architecture with these layers:
- Domain: Pure business logic
- Application: Use cases
- Infrastructure: External dependencies

Never import Infrastructure from Domain!
```

Now Claude automatically respects your architecture boundaries.

**Use Case 2: Agent Automation**
```markdown
# agents.md

## Code Review Agent
Always check:
1. Type coverage > 95%
2. No console.log statements
3. Tests for all public functions
```

Agents automatically follow your review standards.

#### Deduplication Strategy

**Problem:** Without deduplication, same content would be injected multiple times per session.

**Solution:**
- Each file identified by `[knowledge:{path}:{hash}:{modified}]`
- Hash changes trigger re-injection (when you update the file)
- Transcript checked to avoid duplicate injection
- Only inject once per unique file version per session

#### Customization

**Add more knowledge files:**

Modify `KNOWLEDGE_FILES` in `hooks/post-tool-use/inject_knowledge.py`:
```python
class KnowledgeFinder:
    KNOWLEDGE_FILES = ["claude.md", "agents.md", "ARCHITECTURE.md", "CONVENTIONS.md"]
```

**Add project root markers:**

Modify `_find_project_root()` method in `inject_knowledge.py`:
```python
def _find_project_root(self) -> Path:
    markers = [".git", "pyproject.toml", "package.json", ".venv", "go.mod"]  # Add desired markers
    # ...
```

---

### 3. Encoding Validation

#### What does it do?

Validates files after write operations to catch encoding corruption immediately.

#### Why do you need it?

**The Problem:**
LLM-generated text that looks fine in output but corrupts when written to files:
- Unicode replacement characters (U+FFFD)
- Binary data written as text
- Wrong encoding assumptions
- Null bytes in text files

**Real Horror Story:**
```python
# What Claude thinks it wrote:
name = "user"

# What actually got written:
name = "us\ufffd\ufffdr"
```

This compiles but breaks at runtime with cryptic errors.

**The Solution:**
After every write, the plugin:
1. Checks MIME type (detects binary files)
2. Scans for null bytes (strong corruption indicator)
3. Validates UTF-8 decoding
4. Detects replacement characters
5. Tries alternative encodings with chardet

**When issues are found:**
```
WARNING: ENCODING ISSUES DETECTED: output.json
The file contains encoding issues (1 problems found).
Please use Read() to review the file and rewrite it from scratch.
```

Claude immediately knows to fix it, preventing broken code from entering your codebase.

#### What Gets Checked

**Binary File Detection:**
```bash
file --mime-type output.bin
# application/octet-stream -> WARNING
```

**Null Byte Detection:**
```python
if b'\x00' in file_bytes:
    # Binary file written as text!
```

**UTF-8 Validation:**
```python
try:
    content = raw_bytes.decode('utf-8')
    if '\ufffd' in content:
        # Replacement chars indicate corruption
except UnicodeDecodeError:
    # Try chardet to identify encoding
```

#### Customization

**Disable checking (specific file types):**

Modify MIME type check in `check_corrupted_encoding.py`:
```python
# Consider specific MIME types as safe
if not mime_type.startswith("text/") and mime_type not in [
    "inode/x-empty",
    "application/json",
    "application/javascript",  # Add
    "application/xml"  # Add
]:
```

**Completely disable:**

Remove from `hooks/hooks.json`:
```json
{
  "PostToolUse": [
    // Remove or comment out:
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

### 4. Static Analysis Checker

#### What does it do?

Automatically runs language-specific static analysis tools when writing code.

#### Why do you need it?

**The Problem:**
- Claude writes code but doesn't run linters or type checkers
- Manual checking required after writing
- Small mistakes accumulate

**The Solution:**
Automatically upon code writing:
- **Python**: Ruff (linting) + basedpyright (type checking) + custom rules
- **TypeScript**: TypeScript compiler + ESLint
- **Terraform**: terraform validate

#### Supported Languages & Checkers

**Python Pipeline:**
1. `python_1_opinionated.py` - Custom rules (6 checkers)
   - Prohibit `-> Any` return type
   - Detect unnecessary comments
   - Recommend match-case
   - Prohibit nested imports
   - Prohibit TypedDict total=False
   - Enforce explicit re-export in `__init__.py`

2. `python_2_ruff.py` - Ruff linter
   - Auto-apply fixable issues
   - Report remaining issues

3. `python_3_basedpyright.py` - Type checking
   - Detect type errors
   - Report type coverage

**TypeScript:**
- TSC compiler check
- Type error reporting

**Terraform:**
- terraform validate
- Configuration validation

#### Customization

**Add new language checker:**

1. Create `hooks/post-tool-use/static_check/{language}.py`
2. Receive PostToolUse data via stdin
3. Communicate results via exit codes:
   - `0`: No issues
   - `2`: Issues found that Claude needs to know

**Example - Go Checker:**
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

    # Run go fmt
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

**Disable checker:**

Remove or comment out static_check hook in `hooks/hooks.json`

---

### 5. Terminalcp Helpers

#### What does it do?

Two hooks to help use terminalcp MCP server:

1. **suggest_terminalcp_for_bash**: Suggest terminalcp when using Bash
2. **terminalcp_list_on_start**: Show active sessions when terminalcp session starts

#### Why do you need it?

**The Problem:**
- Bash unsuitable for interactive processes (REPL, debuggers, etc.)
- Difficult to manage long-running processes
- Limited stdin/stdout interaction

**The Solution:**
terminalcp provides proper terminal emulation for:
- Interactive process support
- Background process management
- Session monitoring

#### How It Works

**suggest_terminalcp_for_bash:**
- Show suggestion once when Bash tool used
- Prevent duplication via Transcript check
- Provide useful usage examples

**terminalcp_list_on_start:**
- Auto-run when terminalcp session starts
- Show current active sessions
- Guide how to attach via CLI

#### Customization

**Disable suggestions:**

Remove from `hooks/hooks.json`:
```json
{
  "PostToolUse": [
    // Remove:
    // { "name": "suggest_terminalcp_for_bash", ... },
    // { "name": "terminalcp_list_on_start", ... }
  ]
}
```

---

### 6. TODO Completion Check (Stop Hook)

#### What does it do?

Blocks stopping conversation when incomplete TODOs remain.

#### Why do you need it?

**The Problem:**
- Claude stops mid-task
- User misses incomplete work
- Inconsistent task completion

**The Solution:**
Stop hook:
1. Reads session's TODO file (`~/.claude/todos/{session_id}-agent-{session_id}.json`)
2. Finds `pending` or `in_progress` status items
3. Blocks stopping if found and shows list

#### Example Behavior

```
[Stop Hook] You still have unresolved TODO items:

  [in_progress] Run tests and fix failures
  [pending] Update documentation

Please complete all tasks before stopping.
If you believe all tasks are done, mark them as 'completed' using TodoWrite.
```

#### Customization

**Disable:**

Remove Stop hook from `hooks/hooks.json`:
```json
{
  "Stop": [
    // Remove:
    // { "name": "check_todos_completed", ... }
  ]
}
```

**Modify TODO file path:**

Modify `get_todos_from_file()` in `hooks/stop/check_todos_completed.py`

---

## MCP Server Configuration

### Included MCP Servers

**1. context7**
- **Purpose**: Library documentation search
- **Usage**: Query latest API docs, version info, breaking changes
- **Command**: `bunx --bun -y @upstash/context7-mcp`

**2. terminalcp**
- **Purpose**: Terminal emulation
- **Usage**: Interactive processes, background job management
- **Command**: `npx @mariozechner/terminalcp@latest --mcp`

### Customization

**Add new MCP server:**

Modify `.mcp.json`:
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

**Remove MCP server:**

Delete server entry from `.mcp.json`

---

## Installation

Install via Claude Code marketplace:

```bash
# Add marketplace
/plugin marketplace add code-yeongyu/opinionated-basic-cc-setup

# Install plugin
/plugin install opinionated-basic-cc-setup
```

The plugin will automatically activate after installation. You may need to restart Claude Code.

---

## Usage Examples

### Example 1: Python Development

```bash
# Start working on Django view
claude> Add a new API endpoint for user profiles

# Plugin auto-injects py.md:
# - Type hints required
# - Use async for with Django ORM
# - pytest naming conventions
# - No alist() method

# Claude writes:
async def get_user_profile(request: HttpRequest, user_id: int) -> JsonResponse:
    user = await User.objects.select_related('profile').aget(id=user_id)
    # ... properly typed, async-first code
```

**Without plugin:** Claude might use `alist()` (doesn't exist), forget type hints, or use sync patterns

### Example 2: Svelte Component

```bash
claude> Create a reactive counter component

# Plugin injects svelte.md:
# - Use Svelte 5 runes
# - Don't destructure reactive proxies
# - Use $state for reactivity

# Claude writes:
<script>
  let count = $state(0);
  const double = $derived(count * 2);
</script>

<button onclick={() => count++}>
  Count: {count}, Double: {double}
</button>
```

**Without plugin:** Might use outdated Svelte 4 syntax or make reactivity mistakes

### Example 3: Project-Aware Refactoring

```markdown
<!-- Project's claude.md -->
# Architecture

Use repository pattern:
- All database access through repositories
- Never use ORM directly in views
- Repositories in `repositories/` directory
```

```bash
claude> Refactor this view to be cleaner

# Plugin automatically injects your claude.md
# Claude refactors using your repository pattern:

async def get_users(request: HttpRequest) -> JsonResponse:
    repository = UserRepository()
    users = await repository.find_all()
    return JsonResponse({'users': [u.dict() for u in users]})
```

**Without plugin:** Refactors without knowing architecture, potentially violating patterns

---

## How It Works Internally

### Hook Execution Pipeline

```
Read/Write/Edit tool execution
    ↓
PostToolUse Hook triggered
    ↓
├─→ inject_language_guide
│   ├─→ Extract extension (.py)
│   ├─→ Find guide (py.md)
│   ├─→ Check Transcript
│   └─→ Inject if not present
│
├─→ inject_knowledge
│   ├─→ Find project root
│   ├─→ Search claude.md/agents.md
│   ├─→ Check duplicates with hash
│   └─→ Inject by distance order
│
├─→ check_corrupted_encoding
│   ├─→ Check MIME type
│   ├─→ Scan null bytes
│   ├─→ Validate UTF-8
│   └─→ Warn if issues found
│
└─→ static_check
    ├─→ Detect language
    ├─→ Run checker
    └─→ Report results
```

### Priority System

**Language guides:**
```
1. ~/.claude/modular-prompts/languages/py.md  (global, highest priority)
2. plugin/modular-prompts/languages/py.md     (plugin default)
```

**Static checkers:**
```
1. ~/.claude/hooks/post-tool-use/static_check/python.py  (global)
2. plugin/hooks/post-tool-use/static_check/python.py     (plugin)
```

This allows global customization to override plugin defaults.

---

## Troubleshooting

### Guide Not Injecting

**Check 1: File exists**
```bash
ls modular-prompts/languages/py.md
```

**Check 2: Already injected**
- Guides inject once per session
- Start new Claude Code session to re-inject

**Check 3: File extension matches**
- `py.md` matches `.py` files
- `svelte.md` matches `.svelte` files
- Extension must match guide filename

### Knowledge Files Not Found

**Check 1: Correct names**
```bash
# Must be exact:
claude.md  # not CLAUDE.md or Claude.md
agents.md  # not AGENTS.md or Agents.md
```

**Check 2: In project hierarchy**
```
project-root/
├── .git/          <- Project root marker
└── claude.md      <- Must be here or below
```

**Check 3: Project root detected**
Plugin looks for:
- `.git/`
- `pyproject.toml`
- `package.json`
- `.venv/`

### Encoding Check False Positives

**If warnings on valid files:**

1. Check actual file:
```bash
file --mime-type yourfile.txt
hexdump -C yourfile.txt | head
```

2. If file is actually valid, hook might be too strict:
```json
// Disable encoding check in hooks/hooks.json
{
  "PostToolUse": [
    // Remove or comment out:
    // { "name": "check_corrupted_encoding", ... }
  ]
}
```

---

## FAQ

**Q: Will this slow down Claude?**
A: No. Guides inject once per session. After initial injection, there's no overhead.

**Q: Can I use this with other editors?**
A: Claude Code specific. Concepts could be adapted to other AI coding tools.

**Q: What if I disagree with Python conventions?**
A: Fork and customize `modular-prompts/languages/py.md` to match your preferences.

**Q: Does this work with Claude Code projects?**
A: Yes! That's the primary use case.

**Q: Can I disable specific hooks?**
A: Yes, edit `hooks/hooks.json` and remove/comment out unwanted hooks.

**Q: How do I update the plugin?**
```bash
cd ~/.claude/plugins/opinionated-basic-cc-setup
git pull origin master
```

**Q: Can I use this commercially?**
A: Yes, MIT License. Free to use in any project.

---

## License

MIT License - See [LICENSE](LICENSE) file for details

## Credits

**Created by:** [@code-yeongyu](https://github.com/code-yeongyu)

**Built with:** [Claude Code](https://claude.com/claude-code)

**Inspired by:** Real-world frustrations with context management in AI-assisted development

---

## Contributing

### Adding Language Guides

New language guide contributions are welcome!

**What makes a good guide:**
- Specific, actionable rules
- Based on real-world experience
- Explains WHY, not just WHAT
- Covers common pitfalls

**Example contribution:**
```markdown
<!-- modular-prompts/languages/rust.md -->
<style>
    <ownership>
        Always follow ownership rules:
        ```rust
        let s1 = String::from("hello");
        let s2 = s1;  // s1 is now invalid
        // println!("{}", s1);  // Error!
        ```

        Why: Core of Rust's memory safety
    </ownership>

    <error-handling>
        Handle errors with Result type:
        ```rust
        fn read_file() -> Result<String, io::Error> {
            let contents = fs::read_to_string("file.txt")?;
            Ok(contents)
        }
        ```

        Why: Explicit error handling improves robustness
    </error-handling>
</style>
```

### Improving Existing Guides

Found a better pattern or discovered a common mistake?

1. Fork the repo
2. Update relevant `.md` file
3. Submit PR with explanation

### Bug Reports

Open an issue with:
- What happened
- What you expected
- Minimal reproduction steps
