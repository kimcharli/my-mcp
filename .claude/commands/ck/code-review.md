---
command: "/ck:code-review"
category: "Quality & Code Review"
purpose: "Comprehensive code review with project structure validation (excludes documentation review)"
wave-enabled: true
performance-profile: "optimization"
allowed-tools: Bash(find:*), Bash(git status:*), Bash(git log:*), Bash(ls:*), Bash(grep:*), Bash(wc:*), Read(*), Glob(*), Grep(*)
---

## Context

- Python files: !`find . -name "*.py"`
- JSON files: !`find . -name "*.json"`
- JavaScript files: !`find . -name "*.js"`
- TypeScript files: !`find . -name "*.ts"`
- Current git status: !`git status --porcelain`
- Recent commits: !`git log --oneline -10`
- Root structure: !`ls -la`
- Main directories: !`find . -maxdepth 2 -type d`
- **ALL executable files in root**: !`find . -maxdepth 1 \( -name "*.js" -o -name "*.py" -o -name "*.ts" -o -name "*.sh" -o -name "*.bat" \) -type f`

## Task

Perform comprehensive code review covering structure, quality, security, and maintainability.

**Note:** For documentation review, use `/ck:doc-review` command.

## Code Review Checklist

### 📁 File Organization & Project Structure (SECURITY CRITICAL)
- ✅ **Root Directory Security**: ZERO debug/temp/scratch files in root (debug-*.js, temp-*, test-*.js)
- ✅ **Essential Files Only**: Only essential files (README.md, CLAUDE.md, package.json, pyproject.toml, etc.)
- ✅ **Executable File Placement**: ALL .js/.py/.ts/.sh files in root READ and security-validated
- ✅ **No Development Artifacts**: Debug scripts, temp files, logs properly organized in scripts/ or tools/
- ✅ **Repository Hygiene**: No artifacts affecting project navigation or containing sensitive data

**Typical Structure Should Be:**
```
/
├── README.md, CLAUDE.md, package.json (essential files)
├── src/ (source code)
├── server/ (server implementations)
├── tests/ (test files)
├── scripts/ (debug/utility scripts)  
├── docs/ (documentation)
├── .claude/ (Claude Code framework)
├── .gemini/ (Gemini integration)
└── dist/ (build artifacts)
```

### 🏗️ Code Quality & Architecture
- ✅ **Code Structure**: Logical organization and separation of concerns
- ✅ **Naming Conventions**: Consistent and meaningful naming
- ✅ **Documentation**: Adequate code comments and docstrings
- ✅ **Error Handling**: Comprehensive error handling patterns
- ✅ **Type Hints**: Python type annotations where applicable
- ✅ **Import Organization**: Clean imports, no unused dependencies

### 🔒 Security Review (PRIORITY #1)
- ✅ **ROOT FILE SECURITY SCAN**: ALL executable files in root (.js, .py, .ts, .sh) read and analyzed
- ✅ **PROJECT-WIDE CREDENTIAL SCAN**: Search entire project (not just src/) for:
  - Hardcoded passwords/secrets/API keys
  - Production IPs (10.*, 192.168.*, specific IPs)
  - Authentication credentials (admin:admin, etc.)
  - Database connection strings with credentials
- ✅ **SUSPICIOUS FILE PATTERNS**: No debug-*.js, temp-*, scratch-*, test-*.js files in root
- ✅ **Sensitive Data**: No hardcoded secrets, API keys, or credentials anywhere
- ✅ **Input Validation**: Proper input sanitization and validation
- ✅ **Environment Variables**: Secure configuration management
- ✅ **Dependencies**: No known vulnerabilities in dependencies
- ✅ **File Operations**: Safe file handling, no path traversal risks
- ✅ **Authentication**: Secure authentication patterns

**MANDATORY SECURITY COMMANDS:**
```bash
# 1. Find ALL executable files in root
find . -maxdepth 1 \( -name "*.js" -o -name "*.py" -o -name "*.ts" -o -name "*.sh" \) -type f

# 2. Read each found file completely
# 3. Project-wide credential scan
grep -r -i "password\|secret\|token\|api.*key\|admin:admin\|10\.\|192\.168\." \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.json" \
  --exclude-dir=node_modules --exclude-dir=dist .

# 4. Check for production URLs/IPs  
grep -r -E "https://.*\.(46|85)\." --include="*.js" --include="*.ts" .
```

### 🧪 Testing & Validation
- ✅ **Test Coverage**: Adequate test coverage for critical functionality
- ✅ **Test Organization**: Tests properly organized and maintainable
- ✅ **CI/CD Integration**: Automated testing where applicable
- ✅ **Edge Cases**: Tests cover edge cases and error conditions

### 📝 Code Documentation
- ✅ **Inline Comments**: Clear code comments and docstrings
- ✅ **API Documentation**: Code-level documentation (docstrings, JSDoc)
- ✅ **Code Examples**: Inline examples in docstrings where helpful
- ✅ **TODO/FIXME**: Appropriate use of code annotations

**Note:** For comprehensive documentation review (README, guides, etc.), use `/ck:doc-review`

### ⚡ Performance & Optimization
- ✅ **Resource Usage**: Efficient resource utilization
- ✅ **Async Patterns**: Proper async/await usage where applicable
- ✅ **Caching Strategy**: Appropriate caching implementation
- ✅ **Database Queries**: Optimized database operations
- ✅ **Memory Management**: No memory leaks or excessive usage

### 🔧 Configuration & Environment
- ✅ **Environment Setup**: Clear environment setup instructions
- ✅ **Configuration Files**: Well-structured configuration
- ✅ **Dependency Management**: Proper dependency declarations
- ✅ **Build Process**: Reliable build and deployment process

## Prevention Strategies

### Pre-Merge Checklist
Create `docs/CODE-REVIEW-CHECKLIST.md`:

```markdown
### Project Structure
- [ ] Root directory only contains essential files
- [ ] Debug/utility scripts organized in scripts/ directory  
- [ ] No development artifacts cluttering root
- [ ] Clear separation between source, tests, docs, and utilities

### Code Quality
- [ ] All functions have appropriate documentation
- [ ] Error handling implemented consistently
- [ ] No TODO/FIXME comments in production code
- [ ] Code follows established patterns and conventions

### Security
- [ ] No hardcoded credentials or sensitive data
- [ ] Input validation implemented where needed
- [ ] Environment variables used for configuration
- [ ] Dependencies scanned for vulnerabilities

### Documentation
- [ ] README.md updated with new features
- [ ] API documentation current and accurate
- [ ] All links validated and working
- [ ] Examples tested and functional
```

### Automated Quality Gates
Set up automated checks:

```bash
# Pre-commit hooks
pre-commit install

# Linting and formatting
ruff check .
black --check .
mypy .

# Security scanning
bandit -r .
safety check

# Documentation validation
markdown-link-check README.md
```

### Review Categories by Risk Level

**🔴 Critical (Must Fix Before Merge):**
- Security vulnerabilities
- Breaking changes without documentation
- Production credential exposure
- Major architectural violations

**🟡 High Priority (Should Fix):**
- Performance issues
- Missing error handling
- Incomplete documentation
- Test coverage gaps

**🟢 Nice to Have (Consider Fixing):**
- Code style improvements
- Optimization opportunities
- Documentation enhancements
- Additional test cases

## Review Process

**🚨 MANDATORY SECURITY-FIRST APPROACH:**

1. **Security-First Root Scan** (BEFORE ANY OTHER ANALYSIS):
   - **Read ALL executable files in project root** (.js, .py, .ts, .sh, .bat)
   - **Search for credentials across ENTIRE project** (not just src/)
   - **Flag hardcoded secrets, production IPs, API keys** as CRITICAL blockers
   - **Verify no debug/temp files contain sensitive data**
   
2. **Project Structure Security Validation**:
   - Check for misplaced debug/utility files in root
   - Verify only essential files exist in project root
   - Scan for any suspicious file patterns (debug-*.js, temp-*, scratch-*)
   
3. **Code Quality Review**: Check implementation patterns and best practices
4. **Performance Review**: Identify optimization opportunities  
5. **Code Documentation Review**: Verify inline comments and code-level documentation
6. **Test Coverage**: Ensure adequate testing for new/changed code

**⚠️ CRITICAL RULE: If ANY hardcoded credentials, production IPs, or sensitive data found in root files, STOP review and flag as SECURITY CRITICAL**

## 🚨 SECURITY SCAN EXECUTION STEPS

### Step 1: Discovery Phase

```bash
# Find ALL executable files in project root
find . -maxdepth 1 \( -name "*.js" -o -name "*.py" -o -name "*.ts" -o -name "*.sh" -o -name "*.bat" \) -type f
```

### Step 2: Mandatory Root File Review

- **READ EVERY FILE** found in Step 1 completely (not just listing)
- **ANALYZE CONTENTS** for credentials, production URLs, hardcoded secrets
- **FLAG IMMEDIATELY** any sensitive data found

### Step 3: Project-Wide Security Scan

```bash
# Comprehensive credential scan across entire project
grep -r -i "password\|secret\|token\|api.*key\|admin:admin" \
  --include="*.js" --include="*.ts" --include="*.py" --include="*.json" \
  --exclude-dir=node_modules --exclude-dir=dist .

# Production IP scan
grep -r "10\.\|192\.168\.\|172\." --include="*.js" --include="*.ts" --include="*.py" .

# Specific production URL patterns
grep -r -E "https://.*\.(46|85)\." --include="*.js" --include="*.ts" .
```

### Step 4: File Placement Validation

- **ZERO TOLERANCE** for debug-*.js, temp-*, scratch-*, test-*.js files in project root
- All utility/debug scripts must be in scripts/ or tools/ directories
- Flag any misplaced development artifacts

**Note:** For comprehensive documentation review (README, guides, changelogs, etc.), use `/ck:doc-review`

## Output Format

Provide review results in this structure:

```markdown
# Code Review Summary

## 🎯 Overall Assessment
[Brief assessment: APPROVED/NEEDS CHANGES/MAJOR ISSUES]

## 📊 Review Metrics
- Files Reviewed: X
- Issues Found: X (Critical: X, High: X, Low: X)  
- Test Coverage: X%
- Code Documentation Coverage: X%

## 🔴 Critical Issues (SECURITY BLOCKERS)
[Must fix before merge - security issues BLOCK all other review]

## 📁 Project Structure Issues  
[File organization and placement violations]

## 🟡 High Priority Issues  
[Should fix soon]

## 🟢 Suggestions & Improvements
[Nice to have improvements]

## 📁 Project Structure Issues
[Organization and file placement issues]

## ✅ What's Working Well
[Positive feedback on good practices]

## 📝 Action Items
- [ ] Fix critical security issue in file X
- [ ] Add inline documentation for function Y
- [ ] Add tests for module Z
```

This comprehensive review catches organizational issues before they become problems during documentation updates! 🎯
