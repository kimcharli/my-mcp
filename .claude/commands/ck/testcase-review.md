---
description: Build comprehensive unit and integration tests for added features and execute them
allowed-tools: Bash(ls:*), Bash(find:*), Bash(cat:*), Bash(git status:*), Bash(npm:*), Bash(yarn:*), Bash(python:*), Bash(pytest:*), Bash(cargo:*), Read(*), Write(*), Edit(*), MultiEdit(*), Grep(*), Glob(*)
---

## Context

- Project files: !`ls -la`
- Test files: !`find . -name "*test*" -o -name "*spec*"`
- Package info: !`cat package.json`
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

4. **Execute all tests** and:
   - Run unit tests with coverage reporting
   - Run integration tests
   - Verify all tests pass
   - Report coverage metrics and any failures

5. **Provide test documentation** including:
   - Test strategy explanation
   - Coverage report summary
   - Instructions for running tests locally
