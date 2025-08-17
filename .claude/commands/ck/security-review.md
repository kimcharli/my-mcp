---
command: "/ck:security-review"
category: "Security & Code Review"
purpose: "Comprehensive security vulnerability assessment and recommendations"
description: "Analyze code for security vulnerabilities, compliance issues, and security best practices"
allowed-tools: Bash(find:*), Bash(git status:*), Bash(grep:*), Read(*), Grep(*), Glob(*)
wave-enabled: true
performance-profile: "standard"
---

## Context

- Python files: !`find . -name "*.py"`
- JavaScript files: !`find . -name "*.js"`
- Configuration files: !`find . -name "*.json"`
- Environment files: !`find . -name ".env*"`
- Current git status: !`git status --porcelain`

## Task

Perform comprehensive security review of the codebase: **$ARGUMENTS**

### Security Analysis Areas

1. **Authentication & Authorization**
   - Verify secure authentication mechanisms
   - Check for proper access controls
   - Validate session management

2. **Data Protection** 
   - Identify sensitive data exposure
   - Validate encryption implementations
   - Check data sanitization

3. **Input Validation**
   - Analyze input validation patterns
   - Identify injection vulnerabilities
   - Check for XSS and CSRF protections

4. **Configuration Security**
   - Review environment variable usage
   - Check for hardcoded secrets
   - Validate security headers

5. **Dependency Security**
   - Scan for vulnerable dependencies
   - Check for outdated packages
   - Validate third-party integrations

### Output Requirements

Provide detailed security assessment with:
- Risk level classification (Critical/High/Medium/Low)
- Specific code locations and line numbers
- Actionable remediation recommendations
- Compliance considerations (OWASP, industry standards)
