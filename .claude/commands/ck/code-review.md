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

**🚨 MANDATORY SECURITY-FIRST APPROACH WITH AUTOMATED REMEDIATION:**

1. **Security-First Root Scan** (BEFORE ANY OTHER ANALYSIS):
   - **Read ALL executable files in project root** (.js, .py, .ts, .sh, .bat)
   - **Search for credentials across ENTIRE project** (not just src/)
   - **Flag hardcoded secrets, production IPs, API keys** as CRITICAL blockers
   - **Verify no debug/temp files contain sensitive data**
   
2. **Project Structure Security Validation**:
   - Check for misplaced debug/utility files in root
   - Verify only essential files exist in project root
   - Scan for any suspicious file patterns (debug-*.js, temp-*, scratch-*)
   
3. **AUTOMATED REMEDIATION PHASE** (NEW):
   - **Immediately fix identified security issues** after flagging them
   - **Move misplaced debug/utility files** to appropriate directories
   - **Create scripts/ directory** if it doesn't exist
   - **Update .gitignore** to prevent future issues
   - **Verify all fixes** are applied correctly
   
4. **Code Quality Review**: Check implementation patterns and best practices
5. **Performance Review**: Identify optimization opportunities  
6. **Code Documentation Review**: Verify inline comments and code-level documentation
7. **Test Coverage**: Ensure adequate testing for new/changed code

**⚠️ UPDATED RULE: When security issues are found, IDENTIFY them as CRITICAL, then IMMEDIATELY PROCEED to fix them automatically**

## 🚨 SECURITY SCAN AND AUTO-FIX EXECUTION STEPS

**CRITICAL WORKFLOW: IDENTIFY → FIX → VERIFY → CONTINUE**

### Step 1: Discovery and Analysis Phase

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

### Step 5: **IMMEDIATE AUTO-REMEDIATION** (Execute After Each Issue Found)

**🚨 DO NOT PROCEED TO NEXT REVIEW SECTION UNTIL ALL CRITICAL FIXES ARE APPLIED**

#### A. Move Misplaced Files:
```bash
# Execute immediately when debug/test files found in root
mkdir -p scripts/
for file in debug-*.js temp-*.* test-*.js scratch-*.*; do
    if [ -f "$file" ]; then
        echo "🔧 FIXING: Moving $file to scripts/"
        mv "$file" scripts/
    fi
done
```

#### B. Secure Credentials:
- **IMMEDIATE ACTION**: Edit files with hardcoded secrets
- **REPLACE** hardcoded values with environment variables  
- **CREATE** .env.example with placeholder values

#### C. Update .gitignore:
```bash
# Prevent future issues
if ! grep -q "debug-\*" .gitignore; then
    echo "🔧 FIXING: Updating .gitignore"
    echo -e "\n# Debug and temp files\ndebug-*\ntemp-*\nscratch-*" >> .gitignore
fi
```

### Step 6: Post-Fix Verification

```bash
# Verify no critical files remain in root
echo "🔍 VERIFYING: Checking for remaining debug files in root"
find . -maxdepth 1 \( -name "debug-*" -o -name "temp-*" -o -name "scratch-*" \) -type f

# Verify scripts directory created
echo "🔍 VERIFYING: Scripts directory contents"
ls -la scripts/ 2>/dev/null || echo "No scripts directory found"

# Final security scan
echo "🔍 VERIFYING: Final credential scan"  
grep -r -i "password\|secret\|api.*key" --include="*.js" --include="*.py" . | grep -v ".env.example" || echo "No hardcoded credentials found"
```

### Step 7: **ONLY THEN CONTINUE** to Code Quality Review

- ✅ All critical security issues resolved
- ✅ File structure organized properly  
- ✅ Post-fix verification completed
- ➡️ **NOW SAFE** to proceed with quality/performance/documentation review

**Note:** For comprehensive documentation review (README, guides, changelogs, etc.), use `/ck:doc-review`

## 🔧 AUTOMATED REMEDIATION PROCEDURES

### Security Issue Remediation (Execute Immediately After Identification)

#### 1. **Misplaced Debug/Test Files in Root**
```bash
# Create scripts directory if it doesn't exist
mkdir -p scripts/

# Move debug/test files to scripts/
for file in debug-*.js temp-*.* test-*.js scratch-*.*; do
    if [ -f "$file" ]; then
        echo "Moving $file to scripts/"
        mv "$file" scripts/
    fi
done
```

#### 2. **Hardcoded Credentials Found**
- **IMMEDIATE ACTION**: Comment out or remove lines with hardcoded credentials
- **SECURE REPLACEMENT**: Replace with environment variable references
- **EXAMPLE FIX**:
```javascript
// BEFORE (CRITICAL):
const apiKey = "sk-1234567890abcdef";

// AFTER (SECURE):
const apiKey = process.env.API_KEY || '';
if (!apiKey) {
    throw new Error('API_KEY environment variable is required');
}
```

#### 3. **Production URLs/IPs in Code**
- **IMMEDIATE ACTION**: Replace hardcoded production URLs with environment variables
- **CONFIGURATION FILE**: Create/update .env.example with placeholder values
- **EXAMPLE FIX**:
```javascript
// BEFORE (INSECURE):
const baseUrl = "https://production.example.com";

// AFTER (SECURE):
const baseUrl = process.env.BASE_URL || 'https://localhost:3000';
```

#### 4. **Missing .gitignore Entries**
```bash
# Add to .gitignore if not present
echo "# Temporary and debug files" >> .gitignore
echo "debug-*" >> .gitignore
echo "temp-*" >> .gitignore
echo "scratch-*" >> .gitignore
echo "test-*.js" >> .gitignore
echo "*.log" >> .gitignore
echo ".env" >> .gitignore
```

#### 5. **File Organization Fixes**
```bash
# Ensure proper directory structure
mkdir -p scripts/ tests/ docs/ src/

# Move utility scripts
find . -maxdepth 1 -name "*-util.js" -exec mv {} scripts/ \;
find . -maxdepth 1 -name "*-helper.py" -exec mv {} scripts/ \;

# Update any imports/references after moving files
grep -r "require('./debug-" . && echo "⚠️  Update import paths after moving files"
```

### Automated Quality Fixes

#### 1. **Missing Error Handling**
- Add try-catch blocks around risky operations
- Implement proper error logging
- Add input validation

#### 2. **Documentation Gaps**
- Add JSDoc/docstring headers to undocumented functions
- Add inline comments for complex logic
- Update README with new features

#### 3. **Security Headers**
```bash
# Add security headers to .env.example
echo "# Security Configuration" >> .env.example
echo "NODE_ENV=production" >> .env.example
echo "SESSION_SECRET=generate-secure-key-here" >> .env.example
```

### Post-Remediation Validation

#### 1. **Verify Fixes Applied**
```bash
# Confirm no debug files in root
find . -maxdepth 1 \( -name "debug-*" -o -name "temp-*" -o -name "scratch-*" \) -type f | wc -l

# Confirm no hardcoded credentials
grep -r -i "password\|secret\|api.*key" --include="*.js" --include="*.py" . | grep -v ".env.example"

# Confirm scripts directory created and populated
ls -la scripts/ 2>/dev/null || echo "Scripts directory needed"
```

#### 2. **Test Application Still Works**
```bash
# Run basic tests
npm test 2>/dev/null || python -m pytest 2>/dev/null || echo "Run manual testing"

# Check for broken imports
grep -r "require('./debug-" . && echo "⚠️  Fix import paths"
grep -r "from.*debug-" . && echo "⚠️  Fix import paths"
```

#### 3. **Update Documentation**
- Update README.md with new security practices
- Document environment variable requirements
- Add setup instructions for scripts/

### Remediation Priority Order

1. **🔴 CRITICAL - Execute Immediately**:
   - Remove/secure hardcoded credentials
   - Move debug files from root
   - Fix production URL exposure

2. **🟡 HIGH - Execute During Review**:
   - Update .gitignore
   - Create proper directory structure
   - Add environment variable templates

3. **🟢 NICE TO HAVE - Schedule for Later**:
   - Add missing error handling
   - Improve documentation
   - Optimize performance issues

## Output Format

Provide review results in this structure:

```markdown
# Code Review Summary

## 🎯 Overall Assessment
[Brief assessment: APPROVED/NEEDS CHANGES/MAJOR ISSUES]

## 📊 Review Metrics
- Files Reviewed: X
- Issues Found: X (Critical: X, High: X, Low: X)  
- Issues Fixed: X (Critical: X, High: X)
- Test Coverage: X%
- Code Documentation Coverage: X%

## 🔧 AUTOMATED FIXES APPLIED
[List of security and structural issues automatically resolved]

### 🔴 Critical Security Fixes:
- ✅ Moved debug-*.js files from root to scripts/
- ✅ Removed hardcoded API keys from config.js
- ✅ Updated .gitignore to prevent future issues
- ⚠️ Manual review required for: [list any issues needing manual attention]

### 📁 Structure Improvements:
- ✅ Created scripts/ directory
- ✅ Organized utility files properly  
- ✅ Updated file permissions

## 🔴 Remaining Critical Issues (SECURITY BLOCKERS)
[Issues that require manual attention before merge]

## 🟡 High Priority Issues  
[Should fix soon - some may have been auto-fixed]

## 🟢 Suggestions & Improvements
[Nice to have improvements for future consideration]

## ✅ What's Working Well
[Positive feedback on good practices]

## 📝 Verification Steps Completed
- [x] Security scan completed
- [x] Automated fixes applied  
- [x] Post-fix validation run
- [x] File structure reorganized
- [ ] Manual testing recommended

## 📝 Action Items Remaining
- [ ] Test application after file moves
- [ ] Update import paths if needed
- [ ] Review environment variable setup
- [ ] Add missing documentation for functions X, Y
```

This comprehensive review catches organizational issues before they become problems during documentation updates! 🎯
