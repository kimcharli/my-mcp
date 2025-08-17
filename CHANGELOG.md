# Changelog

All notable changes to the MCP Server Collection project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Claude Code SuperClaude framework integration
- Custom command system with specialized commands
- Gemini AI integration with command tooling
- Apstra network automation server integration
- Enhanced AI assistant coordination and context sharing

### Enhanced
- CLAUDE.md with advanced integration features documentation
- Multi-AI model coordination capabilities
- Intelligent task routing and orchestration

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