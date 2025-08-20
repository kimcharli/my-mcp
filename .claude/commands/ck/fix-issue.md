---
command: "/ck:fix-issue"
category: "Development & Bug Fixing"
purpose: "Automated issue resolution with comprehensive debugging and quality assurance"
description: "Systematically analyze, debug, and fix issues while maintaining code quality and preventing regressions"
allowed-tools: Bash(find:*), Bash(git status:*), Bash(grep:*), Bash(npm:*), Bash(pytest:*), Read(*), Write(*), Edit(*), MultiEdit(*), Grep(*), Glob(*)
wave-enabled: true
performance-profile: "standard"
agent: "bug-fixer"
---

## Context

- Issue details: **$ARGUMENTS**
- Current git status: !`git status --porcelain`
- Recent commits: !`git log --oneline -10`
- Relevant files: !`find . -name "*.py" -o -name "*.js" -o -name "*.ts" | head -20`
- Error logs: !`find . -name "*.log" -o -name "error*" | head -10`
- Test files: !`find . -name "*test*" -o -name "*spec*" | head -15`
- Project config: @package.json @pyproject.toml
- Architecture docs: @docs/ARCHITECTURE.md

## Task

**Systematically resolve issue using comprehensive debugging and quality assurance methodology.**

## Issue Resolution Workflow

### Phase 1: Issue Analysis & Root Cause Investigation
- [ ] **Parse Issue Description**: Extract symptoms, error messages, reproduction steps
- [ ] **Gather Context**: Review related code, recent changes, system state
- [ ] **Reproduce Issue**: Create minimal reproduction case if not provided
- [ ] **Root Cause Analysis**: Use debugging tools to identify underlying cause
- [ ] **Impact Assessment**: Determine scope and severity of the issue

#### Debugging Strategies by Issue Type:
```bash
# Runtime Errors
grep -r "error\|exception\|traceback" --include="*.log" .
find . -name "*error*" -exec tail -50 {} \;

# Performance Issues  
find . -name "*.py" -exec grep -l "time\|performance\|slow" {} \;
ps aux | grep -E "(node|python|uvicorn)"

# Integration Failures
grep -r "connection\|timeout\|404\|500" --include="*.log" .
netstat -tuln | grep -E "(3000|8000|5000)"

# Logic Errors
git log --oneline -10 -- path/to/affected/files
git diff HEAD~5..HEAD -- path/to/affected/files
```

### Phase 2: Solution Design & Planning
- [ ] **Design Fix Strategy**: Plan approach that addresses root cause, not just symptoms
- [ ] **Consider Side Effects**: Identify potential impact on other components
- [ ] **Plan Testing Strategy**: Design tests to validate fix and prevent regressions
- [ ] **Review Dependencies**: Check if fix requires dependency updates or changes
- [ ] **Plan Rollback Strategy**: Ensure fix can be safely reverted if needed

### Phase 3: Implementation & Code Quality
- [ ] **Apply Fix Following Standards**: Implement solution using project conventions
- [ ] **Maintain Code Patterns**: Respect existing architecture and design patterns
- [ ] **Add Comprehensive Error Handling**: Include proper exception handling and logging
- [ ] **Update Documentation**: Add inline comments and update relevant docs
- [ ] **Validate Against Requirements**: Ensure fix meets all functional requirements

#### Implementation Best Practices:
```python
# Error Handling Pattern
try:
    result = risky_operation()
    logger.info(f"Operation completed successfully: {result}")
    return result
except SpecificException as e:
    logger.error(f"Known issue occurred: {e}")
    handle_gracefully(e)
    raise UserFriendlyError(f"Operation failed: {user_message}")
except Exception as e:
    logger.exception("Unexpected error in operation")
    monitor.record_error("operation_name", str(e))
    raise SystemError("Internal system error occurred")
```

### Phase 4: Testing & Validation
- [ ] **Create Regression Tests**: Add tests that would catch this issue in future
- [ ] **Test Fix Thoroughly**: Validate fix works under various conditions
- [ ] **Test Edge Cases**: Ensure fix handles boundary conditions properly
- [ ] **Integration Testing**: Verify fix doesn't break other functionality
- [ ] **Performance Testing**: Confirm fix doesn't introduce performance regressions

#### Test Implementation:
```python
# Regression Test Example
def test_issue_regression():
    """Test for issue #123 - ensure fix prevents regression."""
    # Arrange: Set up conditions that caused the original issue
    problematic_input = create_issue_scenario()
    
    # Act: Execute the fixed functionality
    result = fixed_function(problematic_input)
    
    # Assert: Verify issue is resolved
    assert result.is_valid()
    assert not result.has_errors()
    assert result.meets_requirements()

# Integration Test
def test_fix_integration():
    """Verify fix integrates properly with rest of system."""
    # Test full workflow including the fix
    pass
```

### Phase 5: Documentation & Prevention
- [ ] **Update Issue Documentation**: Document root cause and solution approach
- [ ] **Add Code Comments**: Explain fix reasoning and important considerations
- [ ] **Update Architecture Docs**: If fix changes system behavior significantly
- [ ] **Create Prevention Guidelines**: Document how to avoid similar issues
- [ ] **Update Monitoring**: Add alerts or checks to detect similar issues early

## Quality Assurance Checklist

### Code Quality Standards
- ✅ **Follows Project Conventions**: Naming, formatting, structure patterns
- ✅ **Proper Type Hints**: Python type annotations, TypeScript types
- ✅ **Comprehensive Error Handling**: All exceptions properly caught and handled
- ✅ **Logging Integration**: Appropriate logging levels and messages
- ✅ **Performance Considerations**: No unnecessary performance degradation

### Testing Requirements
- ✅ **Unit Tests Added**: Test the specific functionality that was broken
- ✅ **Integration Tests**: Verify fix works with other system components
- ✅ **Regression Tests**: Prevent the issue from reoccurring
- ✅ **Edge Case Coverage**: Test boundary conditions and error scenarios
- ✅ **All Tests Pass**: Both new and existing test suites

### Security & Safety
- ✅ **Input Validation**: Ensure fix doesn't introduce security vulnerabilities
- ✅ **Authorization Checks**: Verify proper access controls maintained
- ✅ **Data Protection**: Sensitive data handling remains secure
- ✅ **Rollback Safety**: Fix can be safely reverted if needed

## Debugging Tools & Techniques

### Language-Specific Debugging:
```bash
# Python Debugging
python -m pdb script.py  # Interactive debugger
python -c "import pdb; pdb.set_trace()"  # Breakpoint in code
pytest -xvs --pdb  # Drop into debugger on test failure

# JavaScript/Node.js Debugging  
node --inspect-brk script.js  # Chrome DevTools debugging
console.log() and console.trace()  # Quick debugging
npm test -- --verbose  # Detailed test output

# System-Level Debugging
strace -e trace=file program  # System call tracing
lsof -p PID  # Open files for process
netstat -tuln  # Network connections
```

### Log Analysis:
```bash
# Find recent errors
grep -r "ERROR\|CRITICAL" --include="*.log" . | tail -20

# Pattern analysis
awk '/ERROR/ {print $1, $2, $NF}' app.log | sort | uniq -c

# Real-time monitoring
tail -f logs/app.log | grep -E "(ERROR|WARN|CRITICAL)"
```

## Post-Fix Validation

### Automated Checks:
```bash
# Run test suites
npm test || python -m pytest || cargo test

# Code quality checks
eslint . || flake8 . || clippy

# Security scanning
npm audit || safety check || cargo audit

# Performance verification
time npm start  # Startup time check
ab -n 100 -c 10 http://localhost:3000/  # Load testing
```

### Manual Verification:
- [ ] **Reproduce Original Issue**: Confirm it no longer occurs
- [ ] **Test Happy Path**: Verify normal functionality works
- [ ] **Test Error Conditions**: Ensure error handling works properly
- [ ] **Check Logs**: Verify appropriate logging is in place
- [ ] **Monitor Resources**: Check memory/CPU usage is reasonable

## Documentation Updates

### Required Documentation:
- [ ] **Inline Code Comments**: Explain fix reasoning and important details
- [ ] **Changelog Entry**: Document what was fixed and why
- [ ] **Architecture Updates**: If fix changes system design significantly
- [ ] **Troubleshooting Guide**: Help others diagnose similar issues
- [ ] **Prevention Guidelines**: Best practices to avoid similar issues

### Issue Tracking:
- [ ] **Close Original Issue**: Link to fix commit and provide summary
- [ ] **Update Related Issues**: Cross-reference related problems
- [ ] **Tag for Testing**: Mark for QA validation if applicable
- [ ] **Add Labels**: Categorize fix type (bugfix, hotfix, enhancement)

## Success Criteria

### Fix Validation:
- ✅ **Issue Resolved**: Original problem no longer occurs
- ✅ **Root Cause Addressed**: Fix addresses underlying cause, not just symptoms  
- ✅ **No Regressions**: Existing functionality still works correctly
- ✅ **Tests Pass**: All automated tests continue to pass
- ✅ **Performance Maintained**: No significant performance degradation
- ✅ **Code Quality**: Fix maintains or improves code quality standards
- ✅ **Documentation Updated**: All relevant documentation reflects changes
