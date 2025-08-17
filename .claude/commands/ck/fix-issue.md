---
command: "/ck:fix-issue"
category: "Development & Bug Fixing"
purpose: "Automated issue resolution with coding standards compliance"
description: "Analyze and fix bugs, issues, and problems while maintaining code quality and standards"
allowed-tools: Bash(find:*), Bash(git status:*), Bash(grep:*), Read(*), Write(*), Edit(*), MultiEdit(*), Grep(*), Glob(*)
wave-enabled: false
performance-profile: "standard"
---

## Context

- Issue details: **$ARGUMENTS**
- Current git status: !`git status --porcelain`
- Recent commits: !`git log --oneline -5`
- Relevant files: !`find . -name "*.py" -o -name "*.js" -o -name "*.ts"`

## Task

Fix issue following coding standards and best practices.

### Issue Resolution Process

1. **Issue Analysis**
   - Understand the problem description
   - Identify affected code components
   - Determine root cause and scope
   - Review related error logs or symptoms

2. **Solution Design**
   - Plan the fix approach
   - Consider impact on existing functionality
   - Design for maintainability and extensibility
   - Identify testing requirements

3. **Implementation**
   - Apply the fix following coding standards
   - Maintain existing code patterns and conventions
   - Add appropriate error handling
   - Include inline documentation as needed

4. **Validation**
   - Test the fix thoroughly
   - Verify no regressions introduced
   - Check edge cases and error conditions
   - Ensure compliance with quality standards

### Coding Standards Compliance

- Follow established naming conventions
- Maintain consistent code formatting
- Add appropriate type hints (Python)
- Include comprehensive error handling
- Write clear, self-documenting code
- Update related documentation if needed

### Quality Assurance

Ensure the fix meets:
- ✅ Functional requirements
- ✅ Performance standards
- ✅ Security best practices
- ✅ Code quality metrics
- ✅ Testing coverage requirements
