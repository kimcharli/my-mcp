# SuperClaude Entry Point

## General Rules
- keep the style decisions and files to be able to load when required instead of searching files.

## Python Project Rules
When working in a Python project (indicated by presence of `pyproject.toml`, `uv.lock`, or `requirements.txt`):
- **ALWAYS use `uv run` to execute Python commands** - NEVER use `python` or `python3` directly
- Examples:
  - ✅ CORRECT: `uv run python script.py`, `uv run pytest`
  - ❌ WRONG: `python script.py`, `python3 script.py`, `pytest`
- This ensures consistent virtual environment usage and dependency management
- Exception: If `uv` is not installed or the project explicitly states not to use it