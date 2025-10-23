# Git Hooks for Automated Documentation Review

This directory contains generalized git hooks for automatically triggering documentation updates when source code changes.

## Features

- **Multi-language support**: Python, JavaScript/TypeScript, Rust, Go, Java, C#

- **Configurable patterns**: Customize file patterns and documentation targets per project

- **Automatic detection**: Detects changed files and triggers appropriate documentation updates

- **Claude Code integration**: Creates context files for the document-reviewer agent

- **Logging**: Tracks all documentation update triggers

## Setup

### 1. Copy the hook to your project

```bash


# Copy the pre-commit hook to your project's .git/hooks directory

cp _git/hooks/pre-commit /path/to/your/project/.git/hooks/
chmod +x /path/to/your/project/.git/hooks/pre-commit

```


### 2. Create project configuration (optional)

```bash


# Copy the example configuration to your project root

cp _git/.doc-review-config.example /path/to/your/project/.doc-review-config

# Edit the configuration for your specific project

editor /path/to/your/project/.doc-review-config

```


### 3. Create documentation structure

The hook expects documentation files to exist. Create them if they don't:

```bash

mkdir -p docs
touch docs/python_modules_reference.md  # For Python projects
touch docs/javascript_modules_reference.md  # For JS/TS projects

# ... etc for other languages

```


## How It Works

1. **Pre-commit trigger**: When you commit changes, the hook runs automatically

2. **File detection**: Scans staged files for supported language patterns

3. **Context creation**: Creates `/tmp/doc_update_context_[lang].txt` files with change details

4. **Agent preparation**: Provides Claude Code commands to run after commit

5. **Logging**: Records all triggers in `docs/auto_update.log`

## Supported Languages

| Language | Default Pattern | Default Doc Target |
|----------|----------------|-------------------|
| Python | `(src/\|scripts/\|server/).*\.py$` | `docs/python_modules_reference.md` |
| JavaScript/TypeScript | `(src/\|lib/\|client/).*\.(js\|ts\|jsx\|tsx)$` | `docs/javascript_modules_reference.md` |
| Rust | `(src/\|crates/).*\.rs$` | `docs/rust_modules_reference.md` |
| Go | `(cmd/\|pkg/\|internal/).*\.go$` | `docs/go_modules_reference.md` |
| Java | `(src/\|main/).*\.java$` | `docs/java_modules_reference.md` |
| C# | `(src/\|lib/).*\.cs$` | `docs/csharp_modules_reference.md` |

## Configuration

### Basic Configuration

Create a `.doc-review-config` file in your project root:

```bash

#!/bin/bash

# Project-specific patterns

declare -A FILE_PATTERNS=(

```
["python"]="(my_package/|utils/).*\.py$"
["frontend"]="(components/|pages/).*\.(jsx|tsx)$"
```

)

declare -A DOC_TARGETS=(

```
["python"]="README.md"
["frontend"]="docs/components.md"
```

)

```


### Advanced Configuration Examples

#### Monorepo with Multiple Services

```bash

declare -A FILE_PATTERNS=(

```
["backend"]="(backend/|api/).*\.(py|js|ts)$"
["frontend"]="(frontend/|ui/).*\.(js|ts|jsx|tsx)$"
["mobile"]="(mobile/|app/).*\.(swift|kt)$"
```

)

declare -A DOC_TARGETS=(

```
["backend"]="docs/backend_api.md"
["frontend"]="docs/frontend_components.md"
["mobile"]="docs/mobile_features.md"
```

)

```


#### Infrastructure and Configuration Files

```bash

declare -A FILE_PATTERNS=(

```
["infrastructure"]="(terraform/|k8s/).*\.(tf|yaml|yml)$"
["config"]="(config/|settings/).*\.(json|yaml|toml)$"
```

)

declare -A DOC_TARGETS=(

```
["infrastructure"]="docs/infrastructure.md"
["config"]="docs/configuration.md"
```

)

```


## Usage Workflow

1. **Make changes** to your source code

2. **Stage files** with `git add`

3. **Commit** with `git commit -m "your message"`

4. **Hook runs** automatically and shows output like:
   ```


   🔍 Python files changed, updating documentation...
   Modified files:

```
 - src/trading_server.py
```

```
 - src/portfolio_manager.py
```

   🤖 Invoking document-reviewer agent for auto-update...
   📝 Python documentation update context created
   ℹ️  Run this after commit: claude-code /spawn document-reviewer "Update Python modules reference based on /tmp/doc_update_context_python.txt"
   ```


5. **Run the suggested command** after commit to update documentation

## Integration with Claude Code

After the hook triggers, run the suggested command:

```bash


# Example output from hook

claude-code /spawn document-reviewer "Update Python modules reference based on /tmp/doc_update_context_python.txt"

```


The document-reviewer agent will:

- Read the context file with change details

- Analyze the modified source files

- Update the appropriate documentation file

- Preserve existing documentation for unchanged modules

- Follow language-specific documentation conventions

## Troubleshooting

### Hook doesn't run

- Check hook permissions: `ls -la .git/hooks/pre-commit`

- Ensure it's executable: `chmod +x .git/hooks/pre-commit`

### No files detected

- Verify file patterns match your project structure

- Check the `.doc-review-config` file syntax

- Test pattern matching: `git diff --cached --name-only | grep -E "pattern"`

### Documentation files not found

- Create the expected documentation files

- Update `DOC_TARGETS` in configuration to match your structure

### Context files not created

- Check `/tmp/` directory permissions

- Verify the hook runs completely without errors

## Customization

### Adding New Languages

1. Edit `.doc-review-config`:

```bash

declare -A FILE_PATTERNS=(

```
# ... existing patterns ...
["kotlin"]="(src/|main/).*\.kt$"
```

)

declare -A DOC_TARGETS=(

```
# ... existing targets ...
["kotlin"]="docs/kotlin_modules_reference.md"
```

)

declare -A LANGUAGE_NAMES=(

```
# ... existing names ...
["kotlin"]="Kotlin"
```

)

```


### Disabling Languages

```bash


# Remove unwanted languages

unset FILE_PATTERNS["java"]
unset DOC_TARGETS["java"]
unset LANGUAGE_NAMES["java"]

```


### Custom Documentation Targets

You can point to any file:

- `README.md` - Update main README

- `docs/api.md` - Specific API documentation

- `wiki/modules.md` - Wiki-style documentation

## Log Files

The hook creates `docs/auto_update.log` to track all triggers:

```


2024-01-15 10:30:45: Python auto-update triggered for: src/trading.py, src/portfolio.py
2024-01-15 11:15:20: JavaScript auto-update triggered for: client/components/Dashboard.tsx

```


This log file is automatically added to commits when documentation updates are triggered.
