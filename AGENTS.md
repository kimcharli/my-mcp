# AGENTS.md for my-mcp

This document provides guidance for AI agents working on the `my-mcp` project. It outlines the project structure, conventions, and instructions for common tasks like testing and dependency management.

## Project Structure

The `my-mcp` project is a collection of MCP (Model Context Protocol) servers. The project is organized as a monorepo with the following structure:

```
/
├── .agents/              # Agent definitions
├── .claude/              # Claude-specific configurations
├── .gemini/              # Gemini-specific configurations
├── add-demo/             # Demo application
├── docs/                 # Project documentation
├── prompts/              # Prompts for agents
├── server/               # MCP servers
│   ├── filesystem/       # Filesystem analysis server
│   ├── trading/          # Stock trading server
│   └── weather/          # Weather data server
├── tests/                # Integration tests
├── .gitignore            # Git ignore file
├── README.md             # Project README
├── run_all_tests.py      # Comprehensive test runner
└── TESTING_STRATEGY.md   # Testing strategy documentation
```

## Dependencies

This project uses `uv` for dependency management. Each Python-based server has its own `pyproject.toml` file with a list of dependencies.

To install the dependencies for a specific server, navigate to the server's directory and run:

```bash
uv pip install -r requirements.txt
```

Alternatively, you can use `uv` to create a virtual environment and install the dependencies from `pyproject.toml`:

```bash
uv venv
uv pip install -e .
```

## Testing

The project has a comprehensive test suite that includes unit tests for each server and integration tests for the entire collection.

### Running All Tests

To run all tests and generate a coverage report, use the `run_all_tests.py` script at the root of the project:

```bash
python run_all_tests.py
```

### Running Tests for a Specific Server

To run the tests for a specific server, navigate to the server's directory and run the tests using `uv run pytest`. For example, to run the tests for the `trading` server:

```bash
cd server/trading
uv run pytest tests/ --cov=. --cov-report=html -v
```

For more details on the testing strategy, please refer to the `TESTING_STRATEGY.md` file.

## Python Project Rules
When working in a Python project (indicated by presence of `pyproject.toml`, `uv.lock`, or `requirements.txt`):
- **ALWAYS use `uv run` to execute Python commands** - NEVER use `python` or `python3` directly
- Examples:
  - ✅ CORRECT: `uv run python script.py`, `uv run pytest`
  - ❌ WRONG: `python script.py`, `python3 script.py`, `pytest`
- This ensures consistent virtual environment usage and dependency management
- Exception: If `uv` is not installed or the project explicitly states not to use it

## Coding Style and Conventions

This project follows the PEP 8 style guide for Python code. We use pre-commit hooks to enforce code style and run static analysis. Please make sure to install the pre-commit hooks before committing any changes:

```bash
pip install pre-commit
pre-commit install
```

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

## Commit Guidelines

We follow the Conventional Commits specification for our commit messages. This helps us to have a clear and descriptive commit history. The format is as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

For example:

```
feat(trading): add support for market orders
```

## Adding a New Server

To add a new server to the project, you need to:

1.  Create a new directory for the server under the `server/` directory.
2.  Create a `pyproject.toml` file with the server's dependencies.
3.  Create a `tests/` directory with unit tests for the server.
4.  Add the new server to the `run_all_tests.py` script.
5.  Update the `README.md` and `AGENTS.md` files with information about the new server.