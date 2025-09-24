# Claude

## General Rules
- keep the style decisions and files to be able to load when required instead of searching files.

## Coding Standards

### Configuration Management
**AVOID hardcoded values** - Use flexible variables, configuration files, or environment variables instead:
- ✅ CORRECT: Store in config files (`.yaml`, `.json`, `.env`), constants at module level, or class attributes
- ❌ WRONG: Hardcode paths, URLs, credentials, or magic numbers directly in functions
- Examples:
  ```python
  # ✅ GOOD - Configurable
  CONFIG_PATH = Path("config/settings.yaml")
  DEFAULT_TIMEOUT = 30

  # ❌ BAD - Hardcoded
  def connect():
      return requests.get("http://10.0.0.1:8080", timeout=30)

  # ✅ GOOD - Flexible
  def connect(host=None, port=None, timeout=None):
      host = host or os.getenv("API_HOST", "localhost")
      port = port or int(os.getenv("API_PORT", 8080))
      timeout = timeout or DEFAULT_TIMEOUT
      return requests.get(f"http://{host}:{port}", timeout=timeout)
  ```
- Order of preference: 1) Function parameters, 2) Config files, 3) Environment variables, 4) Module constants

## Python Project Rules
When working in a Python project (indicated by presence of `pyproject.toml`, `uv.lock`, or `requirements.txt`):
- **ALWAYS use `uv run` to execute Python commands** - NEVER use `python` or `python3` directly
- Examples:
  - ✅ CORRECT: `uv run python script.py`, `uv run pytest`
  - ❌ WRONG: `python script.py`, `python3 script.py`, `pytest`
- This ensures consistent virtual environment usage and dependency management
- Exception: If `uv` is not installed or the project explicitly states not to use it