# How to Create and Use CLAUDE.md

This document provides a comprehensive guide on how to create and use `CLAUDE.md` files in your projects. `CLAUDE.md` is a project-specific context file designed to guide AI coding assistants (particularly Claude Code) by providing detailed project information, tool capabilities, usage patterns, and best practices.

## Why use CLAUDE.md?

`CLAUDE.md` serves as a "comprehensive project guide for AI assistants," offering detailed context that helps AI tools work more effectively with your codebase. While `AGENTS.md` provides machine-readable build steps and conventions, `CLAUDE.md` focuses on:

- **Project-specific tool capabilities and APIs**
- **AI usage patterns and workflow examples**
- **Integration context for third-party services**
- **Best practices for AI-assisted development**
- **Safety considerations and error handling patterns**
- **Troubleshooting guidance specific to your project**

By using `CLAUDE.md`, AI assistants gain deep understanding of your project's architecture, capabilities, and expectations, leading to more accurate, helpful, and context-aware assistance.

## What to include in CLAUDE.md?

`CLAUDE.md` should include comprehensive context that helps AI assistants understand your project holistically:

### 1. Repository Overview
*   **Project Description**: Brief overview of what the project does
*   **Key Features**: Highlight major capabilities and components
*   **Technology Stack**: Languages, frameworks, and key dependencies
*   **Architecture**: High-level system design and component relationships

### 2. Core Capabilities
*   **Feature Documentation**: Detailed description of each major feature
*   **API Specifications**: Available tools, methods, and their parameters
*   **Usage Patterns**: Example prompts and expected AI interactions
*   **Safety Features**: Built-in protections and validation mechanisms

### 3. Third-Party Integrations
*   **External Services**: APIs, SDKs, and service integrations
*   **Use Cases**: When and why to use each integration
*   **Configuration Requirements**: API keys, environment variables, setup needs

### 4. AI Assistant Best Practices
*   **Tool Selection Strategy**: Guidelines for choosing appropriate tools
*   **Error Handling Patterns**: How to handle failures gracefully
*   **Safety Considerations**: Security, privacy, and operational safety
*   **Common Workflows**: Step-by-step patterns for frequent tasks

### 5. Configuration Context
*   **Environment Setup**: Required installations and configurations
*   **File Paths**: Important directory structures and conventions
*   **Testing Approach**: How to run tests and validate changes

### 6. Development Guidance
*   **Coding Standards**: Project-specific conventions and patterns
*   **Security Requirements**: Authentication, validation, data handling
*   **User Experience**: Guidelines for helpful and clear interactions

### 7. Troubleshooting Context
*   **Common Issues**: Frequent problems and their solutions
*   **Resolution Strategies**: Step-by-step debugging approaches
*   **Diagnostic Commands**: How to investigate issues

### 8. AI Assistant Expectations
*   **Response Quality**: Standards for completeness and accuracy
*   **Explanation Level**: When to explain vs. when to execute
*   **Safety First**: Always prioritize safe operations

## CLAUDE.md Hierarchy

### Global vs. Project-Specific

**Global CLAUDE.md** (`~/.claude/CLAUDE.md`):
- User-wide preferences and coding standards
- Cross-project conventions (e.g., "always use uv for Python")
- Personal workflow preferences
- General configuration management rules

**Project CLAUDE.md** (at repository root):
- Project-specific context and capabilities
- Tool APIs and usage patterns
- Integration documentation
- Project-specific best practices

**Nested CLAUDE.md** (in subdirectories):
- Component-specific context
- Module-level documentation
- Specialized tool guidance for subsystems

AI assistants will automatically read the most relevant `CLAUDE.md` files in this order:
1. Global user CLAUDE.md
2. Project root CLAUDE.md
3. Nearest subdirectory CLAUDE.md (if applicable)

## Structure and Organization Best Practices

### Use Clear Hierarchy
```markdown
# Main Title

## Major Section
Brief overview of what this section covers

### Subsection
Detailed information

#### Sub-subsection (use sparingly)
Very specific details
```

### Provide Concrete Examples
```markdown
**AI Usage Patterns:**
```
# Good Example
"Get the current price and 3-month historical data for Apple (AAPL)"
"Compare the performance of tech stocks: AAPL, MSFT, GOOGL"

# What Users Can Expect
Clear, actionable responses with data visualization
```
```

### Document Tool APIs Clearly
```markdown
### Tool Name

**Primary Use Case:** Clear, one-line description

**Key Tools Available:**
- `function_name(param1, param2)` - What it does
- `another_function(param)` - What it does

**AI Usage Patterns:**
[Concrete examples of how to invoke these tools]

**Safety Features:**
[Built-in protections and limitations]
```

### Include Safety and Error Handling
```markdown
**Error Handling Pattern:**
```python
try:
    result = await tool_call(parameters)
    return successful_response(result)
except ValidationError as e:
    return "Please check your input: " + str(e)
except NetworkError as e:
    return "Service temporarily unavailable. Please try again later."
```
```

### Specify Configuration Requirements
```markdown
### Environment Setup
- **Service Name:** API key required (`ENV_VAR_NAME`)
- **Dependencies:** List required installations
- **File Paths:** Important locations and conventions
```

## Example CLAUDE.md Structure

Here's a recommended structure for a comprehensive `CLAUDE.md`:

```markdown
# [Project Name] - AI Assistant Guide

Brief description of what this project does and who it's for.

## Repository Overview

- **Purpose**: What problem does this solve?
- **Key Features**: Bullet list of major capabilities
- **Technology Stack**: Languages, frameworks, key dependencies
- **Architecture**: High-level system design

## Core Capabilities

### Feature 1 Name
**Primary Use Case:** One-line description

**Key Tools Available:**
- `tool_name(params)` - Description
- `other_tool(params)` - Description

**AI Usage Patterns:**
```
"Example prompt that users might use"
"Another example with expected behavior"
```

**Safety Features:**
- Protection 1
- Protection 2

### Feature 2 Name
[Same structure as Feature 1]

## Third-Party Integrations

### Integration Name
**Use When:** Specific scenarios
**AI Context:** How to use effectively
**Configuration:** Required setup

## AI Assistant Best Practices

### Tool Selection Strategy
1. When to use Tool A
2. When to use Tool B
3. How to combine tools

### Error Handling Patterns
[Code examples and strategies]

### Safety Considerations
1. **Category 1**: Guidelines
2. **Category 2**: Guidelines

### Common Workflows

#### Workflow Name
1. Step 1
2. Step 2
3. Step 3

## Configuration Context

### Environment Setup
- **Requirement 1**: Details
- **Requirement 2**: Details

### File Paths
- Project structure overview
- Important directories

### Testing Approach
- How to run tests
- Coverage expectations

## Development Guidance

### Coding Standards
- Convention 1
- Convention 2

### Security Requirements
- Authentication
- Validation
- Data handling

## Troubleshooting Context

### Common Issues
1. **Issue**: Description
   - **Cause**: Why it happens
   - **Solution**: How to fix

### Resolution Strategies
1. Check X
2. Validate Y
3. Test Z

## AI Assistant Expectations

1. **Be Comprehensive**: Use multiple tools for complete solutions
2. **Be Safe**: Always use dry-run modes first
3. **Be Educational**: Explain what tools do and why
4. **Be Helpful**: Provide clear next steps
5. **Be Accurate**: Validate results and provide context
```

## Writing Tips for Effective CLAUDE.md

### 1. Be Specific and Actionable
❌ **Vague**: "This tool helps with data analysis"
✅ **Specific**: "Use `analyze_portfolio()` to calculate return metrics, risk ratios, and performance benchmarks for your current trading positions"

### 2. Include Real Examples
❌ **Abstract**: "You can query weather information"
✅ **Concrete**:
```
"What's the weather like in San Francisco right now?"
"Give me a 7-day forecast for London"
```

### 3. Document Safety Features Explicitly
```markdown
**Safety Features:**
- Paper trading mode by default (no real money at risk)
- Dry-run mode for all destructive operations
- Files moved to trash (not permanently deleted)
- Input validation with clear error messages
```

### 4. Provide Context for Tool Selection
```markdown
### Tool Selection Strategy

1. **Start with Local Tools** for domain-specific tasks:
   - Financial data → Trading Server
   - System maintenance → Filesystem Server

2. **Use External Services** for broader capabilities:
   - Documentation → Context7
   - Web scraping → Browser MCP

3. **Combine Tools** for comprehensive solutions:
   - Trading + Context7 for investment research
```

### 5. Include Troubleshooting Guidance
```markdown
### Common Issues

1. **Network Connectivity**: Corporate firewalls may block APIs
   - **Check**: Test API endpoint directly
   - **Solution**: Configure proxy settings or use VPN

2. **Authentication**: Missing or invalid API keys
   - **Check**: Verify .env file exists and contains valid keys
   - **Solution**: Regenerate API keys from service dashboard
```

### 6. Define AI Expectations Clearly
```markdown
## AI Assistant Expectations

When working with this project:

1. **Be Comprehensive**: Always check multiple data sources
2. **Be Safe**: Never execute destructive operations without dry-run
3. **Be Educational**: Explain API responses and data insights
4. **Be Helpful**: Suggest next steps and alternatives
5. **Be Accurate**: Validate results before presenting them
```

## Integration with AGENTS.md

`CLAUDE.md` and `AGENTS.md` serve complementary purposes:

| Aspect | AGENTS.md | CLAUDE.md |
|--------|-----------|-----------|
| **Purpose** | Build/test instructions | AI assistant context |
| **Audience** | AI agents (task execution) | AI assistants (guidance) |
| **Content** | Commands, conventions, rules | Capabilities, patterns, workflows |
| **Format** | Machine-readable steps | Rich documentation with examples |
| **Focus** | How to build/test/commit | What the project does and how to use it |

**Best Practice**: Use both files together
- `AGENTS.md`: "Run `pnpm test` to execute tests"
- `CLAUDE.md`: "The trading server provides `get_quote()` for real-time stock prices. Use it when users ask about current market data."

## Validation and Maintenance

### How to Validate Your CLAUDE.md

1. **Completeness Check**
   - [ ] Repository overview present?
   - [ ] All major features documented?
   - [ ] Usage patterns with examples?
   - [ ] Safety features explained?
   - [ ] Troubleshooting guidance included?

2. **Quality Check**
   - [ ] Examples are concrete and actionable?
   - [ ] Technical details are accurate?
   - [ ] Error handling patterns documented?
   - [ ] Configuration requirements clear?

3. **Usability Check**
   - [ ] Can AI understand tool selection strategy?
   - [ ] Are workflows step-by-step and clear?
   - [ ] Is safety guidance prominent?
   - [ ] Are integration contexts helpful?

### Maintenance Best Practices

1. **Update on Major Changes**
   - New features or tools added
   - API changes or deprecations
   - New integrations or dependencies
   - Architecture modifications

2. **Version Control**
   - Commit CLAUDE.md to your repository
   - Document significant changes in commit messages
   - Review during code reviews

3. **Keep Examples Current**
   - Verify example prompts still work
   - Update API signatures when they change
   - Refresh configuration examples

4. **Gather Feedback**
   - Note when AI assistants misunderstand context
   - Add clarifications for frequently confused topics
   - Improve based on actual usage patterns

## Common Patterns by Project Type

### API/Web Service Projects
```markdown
## API Endpoints

### GET /api/resource
**Purpose**: Retrieve resource data
**Parameters**:
- `id` (required): Resource identifier
- `format` (optional): Response format (json|xml)

**AI Usage**: "Get details for resource ID 123 in JSON format"
```

### CLI Tool Projects
```markdown
## Command Reference

### command-name [options]
**Purpose**: What this command does
**Options**:
- `--flag`: What this flag does
- `--param=value`: Parameter description

**AI Usage**: "Run the analyzer with verbose output"
```

### Library/SDK Projects
```markdown
## API Reference

### ClassName.method(param1, param2)
**Purpose**: Method description
**Parameters**:
- `param1` (type): Description
- `param2` (type): Description
**Returns**: Return type and description

**AI Usage**: "Create an instance and call the transform method"
```

### Full-Stack Application Projects
```markdown
## Application Architecture

### Frontend (React/TypeScript)
- Component patterns
- State management approach
- API integration patterns

### Backend (Node.js/Python)
- API design conventions
- Database schema
- Authentication flow

**AI Usage**:
"Add a new feature that displays user statistics"
"Debug the authentication flow when users login"
```

## Advanced Topics

### Multi-Repository Projects

For monorepos or multi-service architectures:

```markdown
# Main CLAUDE.md (repository root)
Project-wide context and overall architecture

# services/service-a/CLAUDE.md
Service A specific capabilities and patterns

# services/service-b/CLAUDE.md
Service B specific capabilities and patterns
```

### Dynamic Configuration

For projects with environment-specific behavior:

```markdown
## Environment-Specific Context

### Development Environment
- Uses mock APIs
- Relaxed validation
- Debug logging enabled

### Production Environment
- Real API endpoints
- Strict validation
- Error logging only

**AI Guidance**: Always confirm environment before suggesting operations
```

### Integration with MCP Servers

For projects that provide MCP servers:

```markdown
## MCP Server Integration

### Server Name
**Protocol**: MCP (Model Context Protocol)
**Transport**: stdio | HTTP

**Available Tools**:
- `tool_name(params)`: Description
  - Input validation: Requirements
  - Output format: Structure
  - Error codes: Meanings

**AI Usage Patterns**:
[Specific examples of tool invocation]
```

## Official Resources and Community

*   **Claude Code Documentation**: [https://docs.claude.com/claude-code](https://docs.claude.com/claude-code)
*   **AGENTS.md Format**: [https://agents.md](https://agents.md)
*   **MCP Protocol**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
*   **Best Practices**: Review example CLAUDE.md files in open source projects

## Summary

`CLAUDE.md` is a powerful tool for enhancing AI assistant effectiveness in your projects:

✅ **Do**:
- Provide comprehensive project context
- Include concrete usage examples
- Document safety features explicitly
- Explain tool selection strategies
- Keep content up-to-date

❌ **Don't**:
- Use vague or abstract descriptions
- Omit safety considerations
- Forget to include error handling patterns
- Leave configuration requirements unclear
- Let documentation become stale

By creating a well-structured `CLAUDE.md`, you enable AI assistants to provide more accurate, helpful, and context-aware assistance throughout your development workflow.
