---
description: Multi-language test case builder and executor - works with JavaScript, Python, Java, Rust, Go, PHP, and other languages
allowed-tools: Bash(ls:*), Bash(find:*), Bash(cat:*), Bash(git status:*), Bash(npm:*), Bash(yarn:*), Bash(python:*), Bash(pytest:*), Bash(cargo:*), Bash(mvn:*), Bash(gradle:*), Bash(go:*), Bash(phpunit:*), Read(*), Write(*), Edit(*), MultiEdit(*), Grep(*), Glob(*)
---

## Multi-Language Test Case Review

**Universal testing command that intelligently detects project type and applies appropriate testing strategies.**

**Supported Languages & Frameworks:**
- **JavaScript/TypeScript**: Jest, Mocha, Jasmine, Vitest
- **Python**: pytest, unittest, nose2  
- **Java**: JUnit, TestNG with Maven/Gradle
- **Rust**: Built-in cargo test framework
- **Go**: Built-in go test framework
- **PHP**: PHPUnit, Pest
- **Other**: Auto-detects testing patterns and frameworks

## Context

- Project files: !`ls -la`
- Test files: !`find . -name "*test*" -o -name "*spec*"`
- Python config: !`find . -maxdepth 2 -name "pyproject.toml" -type f`
- JavaScript config: !`find . -maxdepth 2 -name "package.json" -type f`
- Java config: !`find . -maxdepth 2 -name "pom.xml" -o -name "build.gradle" -type f`
- Rust config: !`find . -maxdepth 2 -name "Cargo.toml" -type f`
- Go config: !`find . -maxdepth 2 -name "go.mod" -type f`
- PHP config: !`find . -maxdepth 2 -name "composer.json" -type f`
- Recent changes: !`git status`

## Your task

For the feature: **$ARGUMENTS**

1. **Analyze the added/modified code** to understand:
   - Core functionality and business logic
   - Dependencies and integrations
   - Edge cases and error conditions
   - Public APIs and interfaces

2. **Create comprehensive unit tests** that:
   - Test individual functions/methods in isolation
   - Cover happy path, edge cases, and error scenarios
   - Mock external dependencies
   - Achieve >80% code coverage for new code

3. **Create integration tests** that:
   - Test feature interactions with other components
   - Verify end-to-end workflows
   - Test database/API integrations if applicable
   - Validate user-facing functionality

4. **Execute all tests** based on project type:
   - **JavaScript/TypeScript**: `npm test` or `yarn test` or `jest` with coverage
   - **Python**: `pytest --cov=. --cov-report=html` or `python -m unittest`
   - **Java**: `mvn test` or `./gradlew test` 
   - **Rust**: `cargo test`
   - **Go**: `go test ./...`
   - **PHP**: `phpunit` or `composer test`
   - **Generic**: Look for test runners in project structure

5. **Intelligent test detection**:
   - Auto-detect testing framework from dependencies/files
   - Use appropriate coverage tools for each language
   - Handle both unit and integration tests
   - Report results in standardized format

6. **Provide test documentation** including:
   - Test strategy explanation
   - Coverage report summary  
   - Language-specific test running instructions
   - Framework-specific setup requirements
