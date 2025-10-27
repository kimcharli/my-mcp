# Changelog

All notable changes to the MCP Server Collection project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added


- **New MCP Server Integrations**

  - Glyph MCP server: Tree-sitter based code structure analysis and symbol extraction

  - IDE Integration: VS Code diagnostics and Jupyter notebook execution capabilities

  - Enhanced third-party server support with improved configuration

- **Comprehensive Testing Framework**

  - Multi-language test support (Python, JavaScript, Java, Rust, Go, PHP)

  - Bash command validation for Claude Code compatibility

  - Integration testing across MCP servers

  - Command permission validation system

- **Claude Code Specialized Agents**

  - Feature Developer Agent: Full-stack development specialist

  - Bug Fixer Agent: Debugging and issue resolution specialist

  - Project Initializer Agent: Project setup and scaffolding specialist

- **Enhanced Command System**

  - `/ck:init-project` - Project initialization with comprehensive templates

  - `/ck:create-feature` - Feature scaffolding with testing and documentation

  - `/ck:add-api-endpoint` - API endpoint creation with security and validation

  - `/ck:add-mcp-server` - MCP server integration configuration helper

  - `/ck:add-slash-command` - Claude Code slash command creation tool

- **Template System**

  - README.md template with variable substitution

  - package.json template for TypeScript/React projects

  - Configuration templates (.env.example, tsconfig.json, .gitignore)

- **Enhanced Documentation**

  - Testing integration context for AI assistants

  - Updated README.md with new MCP server integrations (Glyph, IDE)

  - Enhanced CLAUDE.md with new integration workflows and usage patterns

  - Added comprehensive usage examples for code analysis and development workflows

### Enhanced


- **MCP Server Integration**: Expanded from 7 to 9 third-party integrations with Glyph and IDE servers

- **Development Workflows**: Enhanced code analysis capabilities with Tree-sitter parsing and real-time diagnostics

- **Test Coverage**: Added 42% coverage for trading server, complete test suites for filesystem and weather servers

- **Command Validation**: Fixed bash command permission issues in testcase-review and doc-review commands

- **Quality Assurance**: Implemented comprehensive test execution framework with coverage reporting

- **AI Assistant Context**: Updated integration guides with new server capabilities and usage patterns

### Removed

- **Filesystem MCP**: Removed the old filesystem MCP from the configuration. This is because Claude now natively supports filesystem operations, making the old MCP redundant.

## [2.1.0] - 2025-08-17

### Added


- **Claude Code SuperClaude Framework Integration**

  - Custom command structure in `.claude/commands/` directory

  - Specialized commands for security, git operations, testing, documentation

  - Intelligent task routing and orchestration capabilities

  - Multi-step command execution with quality gates


- **Enhanced Gemini Integration**

  - Specialized command tooling in `.gemini/commands/ck/`

  - Multi-AI coordination between Claude and Gemini

  - Context sharing between different AI models

  - Model-specific optimizations and capabilities


- **New Third-Party Integrations**

  - Apstra network automation server for infrastructure management

  - Enhanced browser automation capabilities

  - Improved context7 integration for documentation lookup


- **Advanced AI Features**

  - Layered integration architecture (Base → Service → Framework → AI Coordination)

  - Intelligent tool selection and optimization

  - Enhanced context awareness and preservation

  - Performance optimization with parallel processing

### Changed


- **Documentation Overhaul**

  - Comprehensive CLAUDE.md update with new integration patterns

  - Enhanced AI assistant best practices and usage patterns

  - Updated README.md with current feature set

  - Added advanced integration architecture documentation


- **Configuration Updates**

  - Enhanced mcp.json with detailed server descriptions

  - Updated apify.json with comprehensive usage guidance

  - Improved environment variable documentation

### Fixed


- **Apify Integration**

  - Resolved previously failing Apify server configuration

  - Added comprehensive setup and troubleshooting guidance

  - Enhanced error handling and recovery strategies


- **Documentation Consistency**

  - Fixed cross-references and internal links

  - Updated code examples to match current implementations

  - Synchronized terminology across all documentation

## [2.0.0] - 2025-08-15

### Added


- **New MCP Servers**

  - Context7 integration for documentation and code pattern lookup

  - BrowserMCP integration for web automation

  - Sequential thinking server for enhanced reasoning

  - Memory server for persistent context


- **Enhanced Third-Party Support**

  - Improved Gemini AI integration

  - Enhanced Apify web scraping capabilities

  - Better error handling across all integrations

### Changed


- **Project Structure**

  - Organized server configurations into separate JSON files

  - Enhanced development templates and examples

  - Improved testing and validation procedures


- **Documentation**

  - Complete rewrite of README.md with comprehensive feature coverage

  - New CLAUDE.md for AI assistant integration guidance

  - Enhanced individual server documentation

### Enhanced


- **Trading Server**

  - Improved paper trading simulation

  - Enhanced risk management features

  - Better CLI interface and testing


- **Filesystem Server**

  - Enhanced cleanup automation

  - Improved safety features with dry-run modes

  - Better macOS integration


- **Weather Server**

  - Complete documentation overhaul

  - Enhanced API integration

  - Improved error handling

## [1.0.0] - 2025-08-10

### Added


- **Core MCP Servers**

  - Trading server with E*TRADE integration and paper trading

  - Filesystem server for macOS disk analysis and cleanup

  - Weather server for weather data and forecasting

  - Add-demo server with development templates


- **Basic Third-Party Integrations**

  - Initial Gemini integration

  - Basic Apify web scraping support


- **Development Infrastructure**

  - UV package manager integration

  - Comprehensive testing framework

  - CLI interfaces for all servers


- **Documentation**

  - Initial README.md with setup instructions

  - Individual server documentation

  - Basic troubleshooting guides

### Technical Details

#### Infrastructure


- Python 3.10+ requirement

- UV package manager for dependency management

- Node.js for third-party NPM servers

- Comprehensive error handling and validation

#### Security


- Paper trading mode by default (no real money risk)

- Dry-run modes for destructive filesystem operations

- Comprehensive input validation across all servers

- Secure API key management through environment variables

#### Performance


- Parallel processing capabilities

- Intelligent resource management

- Caching strategies for external API calls

- Optimized tool selection and coordination

## Migration Guide

### From v1.x to v2.x


1. Update configuration files to new JSON structure

2. Install new dependencies: `uv add -e .` in each server directory

3. Review and update API keys and environment variables

4. Test all integrations with new CLI interfaces

### From v2.0 to v2.1


1. No breaking changes - all existing functionality preserved

2. New features are additive and optional

3. Configuration files remain compatible

4. Enhanced documentation provides upgrade guidance

## Compatibility

### Supported Platforms


- **macOS**: Full support (native filesystem integration)

- **Linux**: Core functionality supported

- **Windows**: Limited support (trading and weather servers)

### AI Assistant Compatibility


- **Claude Code**: Full integration with SuperClaude framework

- **Claude Desktop**: Complete MCP server support

- **Gemini**: Enhanced integration with specialized tooling

- **Other MCP-compatible assistants**: Basic functionality supported

## Contributing

See the Development Guidelines section in [README.md](README.md) for development setup and contribution processes.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
