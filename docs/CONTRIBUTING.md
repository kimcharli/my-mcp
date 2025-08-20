# Contributing to My MCP Server Collection

Thank you for your interest in contributing to the my-mcp project! This document provides guidelines for contributing to our MCP server collection.

## Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/my-mcp.git
   cd my-mcp
   ```
3. **Set up development environment**:
   ```bash
   # Install UV package manager
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install pre-commit hooks
   pip install pre-commit
   pre-commit install
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

- 🐛 **Bug Reports**: Found an issue? Let us know!
- ✨ **Feature Requests**: Have an idea for improvement?
- 🔧 **Code Contributions**: New servers, bug fixes, enhancements
- 📚 **Documentation**: Improve docs, add examples, fix typos
- 🧪 **Testing**: Add tests, improve test coverage
- 🎨 **Design**: UI/UX improvements for tools and interfaces

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to avoid duplicates
2. **Use the issue templates** when available
3. **Provide clear reproduction steps** for bugs
4. **Include system information** (OS, Python version, UV version)

**Bug Report Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**System Information**
- OS: [e.g., macOS 14.0]
- Python: [e.g., 3.11.5]
- UV: [e.g., 0.1.0]
- Server: [e.g., trading, filesystem]

**Additional context**
Any other context about the problem.
```

### Development Process

1. **Follow the Development Guide**: See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed guidelines

2. **Code Standards**:
   - Use type hints for all functions
   - Follow PEP 8 style guidelines
   - Write comprehensive docstrings
   - Add tests for new functionality

3. **Commit Guidelines**:
   - Use [Conventional Commits](https://www.conventionalcommits.org/)
   - Keep commits focused and atomic
   - Write clear commit messages

   **Examples:**
   ```bash
   feat(trading): add options trading support
   fix(filesystem): handle permission errors gracefully
   docs(api): update trading server documentation
   test(weather): add integration tests for forecast API
   ```

4. **Testing Requirements**:
   - All new code must include tests
   - Maintain or improve test coverage
   - Tests must pass before submission
   
   ```bash
   # Run tests
   python run_all_tests.py
   
   # Run specific server tests
   cd server/trading && uv run pytest -v
   ```

### Pull Request Process

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**:
   - Implement your feature or fix
   - Add comprehensive tests
   - Update documentation
   - Follow code standards

3. **Test Your Changes**:
   ```bash
   # Run all tests
   python run_all_tests.py
   
   # Run linting
   pre-commit run --all-files
   
   # Test MCP integration
   python tests/test_mcp_integration.py
   ```

4. **Update Documentation**:
   - Update relevant README files
   - Add or update API documentation
   - Include usage examples

5. **Submit Pull Request**:
   - Use the PR template
   - Link related issues
   - Provide clear description
   - Include test results

**Pull Request Template:**
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Updated documentation

## Related Issues
Fixes #(issue number)

## Additional Notes
Any additional information for reviewers.
```

### Code Review Process

**For Contributors:**
- Respond to feedback constructively
- Make requested changes promptly
- Keep discussions focused on the code
- Be patient during the review process

**Review Criteria:**
- Code correctness and functionality
- Test coverage and quality
- Documentation completeness
- Performance impact
- Security considerations
- Code style and maintainability

## Specific Contribution Areas

### 🏦 Trading Server Contributions

**Priority Areas:**
- Options trading support
- Advanced order types
- Portfolio analysis tools
- Risk management features
- Additional market data providers

**Getting Started:**
```bash
cd server/trading
uv add -e .
uv run cli.py setup --cash 100000
uv run pytest tests/ -v
```

### 🗂️ Filesystem Server Contributions

**Priority Areas:**
- Cross-platform support (Windows, Linux)
- Advanced file analysis
- Automated cleanup schedules
- Security scanning features
- Performance optimizations

**Getting Started:**
```bash
cd server/filesystem
uv add -e .
uv run filesystem.py disk-usage
uv run pytest tests/ -v
```

### 🌤️ Weather Server Contributions

**Priority Areas:**
- Additional weather providers
- Historical data analysis
- Weather alerts and notifications
- Agricultural/marine forecasts
- Climate data integration

### 🛠️ New Server Ideas

**Suggested Servers:**
- **Database Server**: SQL query execution, schema analysis
- **Social Media Server**: Twitter, LinkedIn, Reddit integration
- **IoT Server**: Smart home device control
- **Email Server**: Gmail, Outlook integration
- **Calendar Server**: Google Calendar, Outlook Calendar
- **Cloud Storage**: Dropbox, OneDrive, S3 integration

**Server Creation Process:**
1. Review [add-demo/](add-demo/) for templates
2. Follow [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) guidelines
3. Implement basic MCP protocol compliance
4. Add comprehensive tests
5. Create documentation and examples

## Documentation Contributions

### Areas Needing Documentation

- **API Reference**: Complete server API documentation
- **Tutorials**: Step-by-step guides for common tasks
- **Examples**: Real-world usage scenarios
- **Troubleshooting**: Common issues and solutions
- **Architecture**: System design and patterns

### Documentation Standards

- Use clear, concise language
- Include code examples
- Provide context and background
- Keep content up-to-date
- Follow markdown best practices

## Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and diverse perspectives  
- **Be collaborative**: Work together towards common goals
- **Be patient**: Help others learn and grow
- **Be constructive**: Provide helpful feedback and suggestions

### Communication

- **GitHub Issues**: Bug reports, feature requests, discussions
- **Pull Requests**: Code contributions and reviews
- **Discussions**: General questions, ideas, and community chat
- **Documentation**: Guides, tutorials, and reference materials

## Recognition

Contributors are recognized in several ways:

- **Contributors List**: Listed in project documentation
- **Changelog Credits**: Mentioned in release notes
- **GitHub Metrics**: Contribution graphs and statistics
- **Community Recognition**: Highlighted in discussions and announcements

## Getting Help

### Resources for Contributors

- **[Development Guide](docs/DEVELOPMENT.md)**: Detailed development instructions
- **[Installation Guide](docs/INSTALL.md)**: Setup and configuration
- **[Troubleshooting Guide](docs/TROUBLESHOOTING.md)**: Common issues and solutions
- **[Advanced Usage](docs/ADVANCED.md)**: Advanced features and patterns

### Support Channels

- **GitHub Issues**: Technical questions and bug reports
- **GitHub Discussions**: General questions and ideas
- **Code Review**: Implementation guidance and feedback
- **Documentation**: Usage questions and examples

### Mentorship

New contributors can get help through:

- **Good First Issues**: Issues labeled for beginners
- **Mentorship Program**: Experienced contributors helping newcomers
- **Code Review**: Learning through the review process
- **Pair Programming**: Collaborative development sessions

## License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Thank You!

We appreciate all contributions, whether big or small. Every contribution helps make this project better for the entire community. Thank you for being part of the my-mcp project! 🎉
