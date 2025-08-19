---
command: "/ck:create-feature"
category: "Development & Feature Creation"
purpose: "Scaffold new feature with comprehensive structure and integration"
wave-enabled: true
performance-profile: "standard"
agent: "feature-developer"
allowed-tools: Read(*), Write(*), Edit(*), MultiEdit(*), Bash(*), Glob(*), Grep(*), Task(*)
---

## Context

- Project structure: !`find . -maxdepth 2 -type d`
- Existing features: !`find . -name "*.py" -o -name "*.js" -o -name "*.ts" | head -20`
- Current git status: !`git status --porcelain`
- Package configuration: @package.json @pyproject.toml @Cargo.toml
- Architecture documentation: @docs/ARCHITECTURE.md
- Requirements documentation: @docs/REQUIREMENTS.md
- API design patterns: @docs/API_DESIGN.md

## Task

Create a new feature following project conventions and best practices. This command will:

1. **Requirements Analysis**: Review feature specifications and requirements
2. **Architecture Planning**: Design feature structure following existing patterns
3. **Implementation**: Create all necessary files and components
4. **Integration**: Ensure proper integration with existing system
5. **Testing**: Add appropriate test coverage
6. **Documentation**: Update relevant documentation

## Feature Creation Workflow

### Phase 1: Planning & Analysis
- [ ] Analyze feature requirements and acceptance criteria
- [ ] Review existing codebase patterns and conventions
- [ ] Plan feature architecture and component structure
- [ ] Identify integration points and dependencies
- [ ] Create feature implementation plan

### Phase 2: Core Implementation
- [ ] Create main feature files following project structure
- [ ] Implement core functionality with proper error handling
- [ ] Add input validation and security measures
- [ ] Ensure proper logging and monitoring integration
- [ ] Follow established coding standards and patterns

### Phase 3: Integration & Testing
- [ ] Integrate with existing APIs and services
- [ ] Add comprehensive unit tests
- [ ] Create integration tests for critical paths
- [ ] Test error scenarios and edge cases
- [ ] Validate performance requirements

### Phase 4: Documentation & Finalization
- [ ] Update API documentation if applicable
- [ ] Add feature documentation to relevant guides
- [ ] Update README or user documentation
- [ ] Create or update configuration examples
- [ ] Verify feature meets all requirements

## Best Practices

- **Follow Existing Patterns**: Maintain consistency with established codebase patterns
- **Security First**: Implement proper input validation and security measures
- **Error Handling**: Include comprehensive error handling and logging
- **Testing**: Ensure adequate test coverage for all feature components
- **Documentation**: Keep documentation current and comprehensive
- **Performance**: Consider performance implications and optimization opportunities

## Usage Examples

```bash
# Create a new user authentication feature
/ck:create-feature "User authentication with JWT tokens"

# Create a new API endpoint feature
/ck:create-feature "Product inventory management API"

# Create a new UI component feature
/ck:create-feature "Interactive dashboard with real-time updates"
```

## Integration with Project

This command integrates with:
- **Architecture documentation** for design patterns
- **API design standards** for consistency
- **Testing framework** for quality assurance
- **CI/CD pipeline** for deployment
- **Documentation system** for knowledge management