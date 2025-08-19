# Claude Code AI Assistant Guide - MCP Server Collection

This document provides context and guidance for AI assistants (particularly Claude) when working with the MCP server collection in this repository.

## Repository Overview

This is a comprehensive MCP (Model Context Protocol) server collection designed for Claude Code and other AI assistants, featuring:

- **4 Custom-built MCP servers** (trading, filesystem, weather, add-demo)
- **7 Third-party integrations** (context7, gemini, browser, memory, sequential-thinking, apify, apstra)
- **Production-ready configurations** with comprehensive documentation
- **Development templates and patterns** for MCP server creation
- **Claude Code SuperClaude framework integration** with custom commands and orchestration
- **Gemini AI integration** with specialized command tooling

## Core Capabilities

### 🏦 Trading Server (`server/trading/`)
**Primary Use Case:** Stock market analysis, paper trading, portfolio management

**Key Tools Available:**
- `get_quote(symbol)` - Real-time stock prices
- `get_historical_data(symbol, period, interval)` - Historical price data
- `submit_order(symbol, action, quantity, order_type)` - Place trades (paper mode)
- `get_account_summary()` - Account balance and positions
- `analyze_portfolio()` - Portfolio performance analysis
- `setup_paper_account(cash)` - Initialize trading account

**AI Usage Patterns:**
```
# Market Research
"Get the current price and 3-month historical data for Apple (AAPL)"
"Compare the performance of tech stocks: AAPL, MSFT, GOOGL over the last month"

# Portfolio Management  
"Show me my current portfolio and suggest rebalancing based on performance"
"Calculate my portfolio's return and risk metrics"

# Trading Operations
"Place a buy order for 50 shares of Tesla at market price"
"Set up a paper trading account with $100,000 initial balance"
```

**Safety Features:**
- Paper trading mode by default (no real money at risk)
- Comprehensive input validation and error handling
- Risk management limits and warnings

### 🗂️ Filesystem Server (`server/filesystem/`)
**Primary Use Case:** macOS disk analysis, cleanup automation, system maintenance

**Key Tools Available:**
- `disk_usage_summary()` - Overall disk space analysis
- `find_large_files(min_size_mb, directory)` - Locate space-consuming files
- `analyze_directory_sizes(top_n)` - Directory size breakdown
- `clean_temp_files(dry_run)` - Clean temporary files
- `clean_downloads_folder(days_old, dry_run)` - Downloads cleanup
- `clear_application_caches(app_name, dry_run)` - Clear app caches
- `find_duplicate_files(directory, max_files)` - Duplicate detection
- `list_installed_applications()` - App inventory with sizes

**AI Usage Patterns:**
```
# System Analysis
"Analyze my disk usage and show me the largest files taking up space"
"What directories are using the most space on my system?"

# Cleanup Operations
"Clean up my Downloads folder of files older than 30 days"
"Find and help me remove duplicate files in my Documents folder"
"Clear Chrome's cache to free up space"

# Maintenance
"Show me all installed applications and their disk usage"
"Find temporary files I can safely delete"
```

**Safety Features:**
- Dry-run mode by default for all destructive operations
- Files moved to trash (not permanently deleted)
- System file protection and validation

### 🌤️ Weather Server (`server/weather/`)
**Primary Use Case:** Weather data retrieval, forecasting, location-based queries

**Key Tools Available:**
- `get_current_weather(location)` - Current conditions
- `get_weather_forecast(location, days)` - Multi-day forecasts
- `get_weather_alerts(location)` - Weather warnings and alerts

**AI Usage Patterns:**
```
# Current Conditions
"What's the weather like in San Francisco right now?"
"Compare current weather conditions in New York and Los Angeles"

# Forecasting
"Give me a 7-day weather forecast for London"
"Will it rain in Seattle this weekend?"

# Planning
"Should I plan outdoor activities in Miami this week based on weather?"
"Are there any weather alerts for Chicago?"
```

### 🛠️ Add Demo Server (`add-demo/`)
**Primary Use Case:** MCP development learning, pattern examples, templates

**Key Features:**
- Complete MCP server implementation examples
- Authentication patterns and security practices
- Image processing and file handling examples
- Error handling and validation patterns
- Development templates for new servers

**AI Usage for Development:**
```
# Learning MCP Development
"Show me examples of MCP server tool implementations"
"How do I handle authentication in an MCP server?"
"What are the best practices for error handling in MCP servers?"

# Template Usage
"Help me create a new MCP server based on these examples"
"Explain the image processing patterns in the demo server"
```

## Third-Party Integration Context

### Context7 - Documentation & Code Patterns
**Use When:** Need official documentation, code examples, best practices for libraries/frameworks
**AI Context:** Automatically resolves library names to official documentation and provides accurate, up-to-date code patterns

### Gemini - Google AI Integration  
**Use When:** Need Google's AI capabilities, alternative AI perspective, or Gemini-specific features
**AI Context:** Provides access to Google's Gemini models with different capabilities and perspectives

### Browser MCP - Web Automation
**Use When:** Need to interact with websites, scrape data, or automate browser tasks
**AI Context:** Can navigate websites, extract data, and perform automated web interactions

### Memory Server - Persistent Context
**Use When:** Need to remember information across conversations or maintain long-term context
**AI Context:** Stores and retrieves conversation context and important information

### Sequential Thinking - Enhanced Reasoning
**Use When:** Complex problem-solving, step-by-step analysis, or structured thinking required
**AI Context:** Provides enhanced reasoning capabilities and systematic problem-solving approaches

### Apify - Web Scraping
**Use When:** Need specialized web scraping for job sites, search results, or product information
**AI Context:** Configured for Indeed jobs, Google search results, and Amazon products

### Apstra Network Automation - Infrastructure Management
**Use When:** Network automation, infrastructure management, or datacenter operations
**AI Context:** External integration for network infrastructure automation and management

## AI Assistant Best Practices

### Tool Selection Strategy

1. **Start with Local Servers** for specific domains:
   - Financial data/trading → Trading Server
   - System maintenance → Filesystem Server  
   - Weather information → Weather Server

2. **Use Third-party Services** for broader capabilities:
   - Documentation needs → Context7
   - Web interactions → Browser MCP
   - Complex reasoning → Sequential Thinking
   - Memory across sessions → Memory Server

3. **Combine Tools** for comprehensive solutions:
   - Trading Server + Context7 for investment research
   - Filesystem Server + Memory for system maintenance tracking
   - Weather Server + Browser MCP for location-specific planning

### Error Handling Patterns

All servers implement comprehensive error handling:
- Input validation with clear error messages
- Network timeout protection
- Graceful degradation when services unavailable
- Dry-run modes for destructive operations

**AI Response Pattern:**
```python
try:
    result = await tool_call(parameters)
    return successful_response(result)
except ValidationError as e:
    return "Please check your input: " + str(e)
except NetworkError as e:
    return "Service temporarily unavailable. Please try again later."
except Exception as e:
    return "Unexpected error occurred. Please try a different approach."
```

### Safety Considerations

1. **Financial Operations:**
   - Trading server is in paper mode by default
   - Always confirm before suggesting real trading
   - Emphasize educational/simulation context

2. **File Operations:**
   - Filesystem server uses dry-run by default
   - Always preview changes before execution
   - Files go to trash, not permanent deletion

3. **External Services:**
   - Respect API rate limits
   - Handle authentication securely
   - Validate all external data

### Common Usage Workflows

#### Stock Market Analysis Workflow
1. Get current quote for target stocks
2. Fetch historical data for trend analysis
3. Analyze portfolio if positions exist
4. Provide recommendations based on data
5. Offer to place paper trades for learning

#### System Maintenance Workflow
1. Analyze overall disk usage
2. Identify largest files/directories
3. Suggest cleanup operations (dry-run first)
4. Execute approved cleanup operations
5. Verify results and update recommendations

#### Weather Planning Workflow
1. Get current weather conditions
2. Check forecast for planning period
3. Look for weather alerts/warnings
4. Provide planning recommendations
5. Offer to monitor conditions

## Configuration Context

### Environment Setup
- **Trading:** Requires E*TRADE API keys or paper trading mode
- **Weather:** Needs weather API key for data access
- **Third-party:** Various API keys for external services

### File Paths
- All servers use absolute paths in configurations
- UV package manager handles Python dependencies
- NPX handles Node.js based servers

### Testing Approach
- Each server includes CLI testing capabilities
- Comprehensive test suites available
- Dry-run modes for safe testing

## Development Guidance

When helping users extend or modify these servers:

1. **Follow Existing Patterns:**
   - Type hints and input validation
   - Comprehensive error handling
   - Dry-run modes for destructive operations
   - Clear documentation and examples

2. **Security First:**
   - Never log sensitive information
   - Validate all inputs thoroughly
   - Use secure communication protocols
   - Implement proper authentication

3. **User Experience:**
   - Provide clear, actionable error messages
   - Include helpful usage examples
   - Implement progress indicators for long operations
   - Offer both CLI and MCP interfaces

## Troubleshooting Context

### Common Issues
1. **Network Connectivity:** Corporate firewalls may block financial APIs
2. **Authentication:** API keys need proper setup in .env files
3. **Dependencies:** UV and NPX need to be properly installed
4. **Permissions:** File operations need appropriate system permissions

### Resolution Strategies
1. **Check Environment:** Verify .env files and API keys
2. **Test Individually:** Use CLI interfaces for direct testing
3. **Validate Setup:** Ensure UV/NPX installations are correct
4. **Check Logs:** Enable debug mode for detailed error information

## AI Assistant Expectations

When working with this MCP collection:

1. **Be Comprehensive:** Leverage multiple servers for complete solutions
2. **Be Safe:** Always use dry-run modes first for destructive operations
3. **Be Educational:** Explain what each tool does and why you're using it
4. **Be Helpful:** Provide clear next steps and alternatives when tools fail
5. **Be Accurate:** Validate results and provide appropriate context

This collection is designed to be a powerful toolkit for AI assistants, enabling sophisticated interactions with real-world systems while maintaining safety and providing educational value.

## Testing Integration Context

### Test-Driven Development Support

The MCP server collection includes comprehensive testing frameworks designed to support AI assistants in development workflows:

**Testing Capabilities:**
- **Multi-language Testing**: Python (pytest), JavaScript (npm test), Java (maven/gradle), Rust (cargo), Go (go test), PHP (phpunit)
- **Coverage Reporting**: HTML coverage reports with >80% target coverage
- **Safety Validation**: Dry-run testing for destructive operations
- **Integration Testing**: Cross-server workflow validation
- **Command Validation**: Claude Code command compatibility testing

**AI Usage Patterns for Testing:**
```
# Test Development Workflow
"Create comprehensive test cases for the weather API integration"
"Run the test suite and analyze the coverage report"
"Generate integration tests for the trading server portfolio analysis"

# Quality Assurance
"Validate all filesystem operations use dry-run mode by default"
"Test error handling for network timeouts in market data requests"
"Verify security compliance across all MCP server implementations"

# Test Analysis
"Review test failures and suggest fixes for the trading server"
"Analyze test coverage gaps and recommend additional test cases"
"Generate performance test cases for large file operations"
```

**Testing Best Practices for AI Assistants:**
1. **Test First**: Generate comprehensive test cases before implementing features
2. **Safety Testing**: Always include dry-run and error condition testing
3. **Coverage Focus**: Aim for >80% code coverage with meaningful tests
4. **Integration Validation**: Test cross-server workflows and dependencies
5. **Command Compatibility**: Validate Claude Code command syntax and permissions

**Recent Testing Enhancements:**
- **Bash Command Validation Framework**: Prevents Claude Code permission failures
- **Enhanced Integration Testing**: Cross-server workflow validation
- **Multi-language Test Support**: Intelligent framework detection and execution
- **Coverage Analysis**: Detailed HTML reports with improvement recommendations

## Advanced Integration Features

### Claude Code SuperClaude Framework

This project now includes integration with the Claude Code SuperClaude framework, providing:

**Custom Command Structure:**
- **Command System**: Custom `.claude/commands/` directory with specialized commands
- **Command Categories**: Security review, fix-issue, git operations, test cases, documentation updates
- **Orchestration**: Multi-step command execution with intelligent routing

**Available Custom Commands:**
- `/ck:security-review` - Comprehensive security analysis and recommendations
- `/ck:fix-issue` - Automated issue resolution with best practices
- `/ck:git-commit-push` - Smart git operations with conventional commits
- `/ck:testcases` - Test case generation and validation
- `/ck:update-docs` - Documentation synchronization and enhancement
- `/ck:rule-engine` - Business rule analysis and implementation

**Framework Benefits:**
- **Intelligent Task Routing**: Automatic selection of optimal tools and approaches
- **Context Preservation**: Maintains project context across complex operations
- **Quality Gates**: Built-in validation and safety checks
- **Performance Optimization**: Efficient resource usage and parallel processing

### Gemini AI Integration

Enhanced integration with Google's Gemini models through specialized command tooling:

**Gemini Commands** (`.gemini/commands/ck/`):
- `area-of.toml` - Domain expertise analysis
- `changelog.toml` - Automated changelog generation
- `commit.toml` - Smart commit message generation
- `refactor.toml` - Code refactoring recommendations

**Multi-AI Coordination:**
- **Claude + Gemini**: Complementary AI perspectives for complex problems
- **Context Sharing**: Shared context between different AI models
- **Specialized Tools**: Model-specific optimizations and capabilities

**Usage Patterns:**
```
# Claude Code with SuperClaude framework
claude /ck:security-review --comprehensive --include-dependencies

# Gemini integration for specific tasks
gemini area-of "network automation patterns"
gemini commit --conventional --scope "mcp-integration"
```

### Integration Architecture

**Layered Integration:**
1. **Base Layer**: Core MCP servers (trading, filesystem, weather, add-demo)
2. **Service Layer**: Third-party integrations (context7, gemini, browser, etc.)
3. **Framework Layer**: SuperClaude orchestration and command system
4. **AI Coordination Layer**: Multi-model integration and context sharing

**Benefits for AI Assistants:**
- **Enhanced Capabilities**: Access to specialized tools and services
- **Intelligent Orchestration**: Automatic selection of optimal approaches
- **Context Awareness**: Deep understanding of project structure and patterns
- **Quality Assurance**: Built-in validation and best practices enforcement
- **Performance Optimization**: Efficient resource usage and parallel processing

## Claude Code Specialized Agents

This project includes dedicated AI agents for different development domains:

### 🏗️ Feature Developer Agent (`.claude/agents/feature-developer.md`)

**Specialization**: Full-stack feature development for TypeScript/React/Node.js MCP server projects

**Context Files**:
- `CLAUDE.md` - Project-specific patterns and integration context
- `TESTING_STRATEGY.md` - Testing approaches and quality standards
- `server/*/REQUIREMENTS.md` - Individual server requirements and specifications

**Technology-Specific Guidelines**:
- **TypeScript/Node.js**: Strict mode, async patterns, MCP protocol compliance
- **React Development**: Component patterns, accessibility, state management
- **Python Development**: Type hints, UV package manager, async patterns
- **MCP Server Development**: Protocol specifications, validation, security

**Common Tasks**:
- API endpoint development with REST conventions
- MCP tool creation with parameter validation
- Frontend component development with TypeScript
- Database integration and testing

### 🐛 Bug Fixer Agent (`.claude/agents/bug-fixer.md`)

**Specialization**: Debugging, issue investigation, and systematic problem resolution

**Context Files**:
- `TESTING_STRATEGY.md` - Testing approaches and debugging techniques
- `CLAUDE.md` - Project-specific patterns and integration context
- `server/*/REQUIREMENTS.md` - Individual server requirements and specifications

**Technology-Specific Debugging**:
- **Frontend Issues**: Browser DevTools, React DevTools, component state debugging
- **Backend Issues**: Node.js/Python debugger, server logs, API testing
- **MCP Server Issues**: Protocol debugging, tool execution validation
- **System-Level Issues**: Permissions, environment variables, network connectivity

**Bug Categories**:
- Frontend: Component state, API integration, UI rendering
- Backend: Route handlers, database queries, authentication
- MCP Integration: Server registration, tool parameter validation
- Infrastructure: Configuration, dependencies, deployment

### 🚀 Project Initializer Agent (`.claude/agents/project-initializer.md`)

**Specialization**: New project setup with comprehensive templates and tooling

**Template System** (`.claude/templates/`):
- **README.md**: Project documentation with variable substitution
- **package.json**: Modern React/TypeScript configuration
- **tsconfig.json**: TypeScript strict mode configuration
- **`.env.example`**: Environment variables template
- **`.gitignore`**: Comprehensive ignore patterns

**Generated Project Structure**:
```
{PROJECT_NAME}/
├── .github/workflows/    # CI/CD automation
├── docs/                 # Project documentation
├── src/                  # Source code organization
├── tests/               # Testing framework
├── package.json         # Dependencies and scripts
├── README.md           # Generated from template
└── ...configuration files
```

**Quality Standards**:
- TypeScript strict mode with comprehensive type definitions
- Testing framework setup (Jest, coverage >80%)
- ESLint, Prettier, and development tooling
- Docker support and CI/CD workflows
- Comprehensive documentation structure

## Enhanced Command System

### Development Commands

**`/ck:init-project`**: Initialize new project with comprehensive structure
- Uses `project-initializer` agent
- Template variable substitution system
- Complete development environment setup
- Quality assurance and validation

**`/ck:create-feature`**: Scaffold new feature with testing and documentation  
- Uses `feature-developer` agent
- Requirements analysis and technical design
- Implementation with established patterns
- Comprehensive testing and documentation

**`/ck:add-api-endpoint`**: Create API endpoint with validation and security
- Uses `feature-developer` agent
- REST conventions and error handling
- Authentication and rate limiting
- API documentation generation

### Usage Examples

```bash
# Initialize a new TypeScript/React project
claude /ck:init-project "My Dashboard" "Analytics dashboard with real-time data"

# Create a comprehensive feature
claude /ck:create-feature "User authentication with JWT tokens"

# Add a new API endpoint
claude /ck:add-api-endpoint "POST /api/reports - Generate analytics report"
```