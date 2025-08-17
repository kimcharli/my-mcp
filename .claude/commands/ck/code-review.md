---
command: "/ck:code-review"
category: "Quality & Code Review"
purpose: "Comprehensive code review with project structure validation"
wave-enabled: true
performance-profile: "optimization"
allowed-tools: Bash(find:*), Bash(git status:*), Bash(git log:*), Bash(ls:*), Bash(grep:*), Bash(wc:*), Read(*), Glob(*), Grep(*)
---

## Context

- Python files: !`find . -name "*.py"`
- JSON files: !`find . -name "*.json"`
- Documentation: !`find . -name "*.md"`
- Current git status: !`git status --porcelain`
- Recent commits: !`git log --oneline -10`
- Root structure: !`ls -la`
- Main directories: !`find . -maxdepth 2 -type d`

## Task

Perform comprehensive code review covering structure, quality, security, and maintainability.

## Code Review Checklist

### 📁 File Organization & Project Structure
- ✅ **Root Directory Clean**: Only essential files (README.md, CLAUDE.md, package.json, pyproject.toml, etc.)
- ✅ **Appropriate Directories**: Files organized in logical directory structure
- ✅ **No Development Clutter**: Debug scripts, temp files, logs properly organized
- ✅ **Repository Hygiene**: No artifacts affecting project navigation

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

### 🔒 Security Review
- ✅ **Sensitive Data**: No hardcoded secrets, API keys, or credentials
- ✅ **Input Validation**: Proper input sanitization and validation
- ✅ **Environment Variables**: Secure configuration management
- ✅ **Dependencies**: No known vulnerabilities in dependencies
- ✅ **File Operations**: Safe file handling, no path traversal risks
- ✅ **Authentication**: Secure authentication patterns

### 🧪 Testing & Validation
- ✅ **Test Coverage**: Adequate test coverage for critical functionality
- ✅ **Test Organization**: Tests properly organized and maintainable
- ✅ **CI/CD Integration**: Automated testing where applicable
- ✅ **Edge Cases**: Tests cover edge cases and error conditions

### 📚 Documentation Review
- ✅ **Content Accuracy**: Documentation reflects current implementation
- ✅ **Completeness**: All features and APIs documented
- ✅ **Link Validity**: All internal and external links working
- ✅ **User Experience**: Clear setup and usage instructions
- ✅ **Consistency**: Consistent terminology and formatting
- ✅ **Examples**: Working code examples and use cases

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

1. **Structure Analysis**: Validate project organization and file placement
2. **Code Quality Review**: Check implementation patterns and best practices
3. **Security Audit**: Scan for vulnerabilities and security issues
4. **Performance Review**: Identify optimization opportunities
5. **Documentation Validation**: Verify accuracy and completeness
6. **Test Coverage**: Ensure adequate testing for new/changed code

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
- Documentation Coverage: X%

## 🔴 Critical Issues
[Must fix before merge]

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
- [ ] Update documentation for feature Y
- [ ] Add tests for module Z
```

This comprehensive review catches organizational issues before they become problems during documentation updates! 🎯