# Code Review TODO

This file summarizes the findings and recommendations from the code review.

## Security Vulnerabilities


- [x] **Hardcoded Secrets:** Remove all hardcoded secrets (passwords, API keys, tokens) from the code and load them from a secure source, such as environment variables or a secret management system.

- [x] **Insecure File Operations:** Validate all file paths to prevent path traversal vulnerabilities. Use `send2trash` instead of `os.unlink` and `shutil.rmtree` to delete files and directories.

- [x] **Use of `eval`:** Remove the use of `eval` from the `test_framework.py` script.

- [x] **Unsafe `grep` commands:** Use the `re` module instead of `grep` with `shell=True` in the `test_code_review_security.py` script.

- [x] **Insecure `os.system` call:** Use a library like `blessings` or `curses` to control the terminal instead of `os.system`.

- [x] **Insecure `subprocess.run` calls:** Avoid using `subprocess.run` to execute shell commands.

## Maintainability


- [x] **Add Comments:** Add comments to the code to improve readability and maintainability.

- [x] **Refactor Complex Functions:** Break down complex functions into smaller, more manageable functions.

- [x] **Remove Redundant Code:** Refactor redundant code into reusable functions.

- [x] **Add More Unit Tests:** Add more unit tests to improve code quality and reduce the risk of regressions.

## File-Specific Issues

### `add-demo/`


- [x] **`app_auth.py`**: Externalize the hardcoded `issuer_url`.

- [x] **`app_tool.py`**: Use `https` instead of `http` in the `fetch_weather` function.

### `server/filesystem/`


- [x] **`filesystem.py`**:

  - [x] Validate all file paths to prevent path traversal vulnerabilities.

  - [x] Use `send2trash` instead of `os.unlink` and `shutil.rmtree`.

  - [x] Avoid using `subprocess.run` to execute the `mdls` command.

### `server/trading/`


- [x] **`cli.py`**: Use a library like `blessings` or `curses` to control the terminal instead of `os.system`.

- [x] **`paper_trading.py`**: Make the `RISK_MAX_POSITION_SIZE` and `RISK_MAX_DAILY_LOSS` constants configurable.

- [x] **`trading.py`**: Make the `TRADING_MODE` and `DATA_REQUEST_TIMEOUT` constants configurable.

### `tests/`


- [x] **`test_code_review_security.py`**: Use the `re` module instead of `subprocess.run` with `grep`.

- [x] **`test_command_bash_validation.py`**: Avoid executing shell commands with `subprocess.run`.

- [x] **`test_original_issue_scenario.py`**: Avoid executing shell commands with `subprocess.run`.
