---
command: "/ck:init-project"
category: "Project Initialization & Setup"
purpose: "Initialize new project with comprehensive structure, templates, and documentation"
wave-enabled: true
performance-profile: "standard"
agent: "project-initializer"
allowed-tools: Write(*), Edit(*), MultiEdit(*), Bash(*), Glob(*), Grep(*), Task(*)
---

## Context

- Current directory: !`pwd`
- Directory contents: !`ls -la`
- Git status: !`git status 2>/dev/null || echo "Not a git repository"`
- Node version: !`node --version 2>/dev/null || echo "Node.js not installed"`
- npm version: !`npm --version 2>/dev/null || echo "npm not installed"`

## Task

Initialize a new project with comprehensive structure, documentation, and development tooling. This command will:

1. **Project Setup**: Create directory structure and core files
2. **Template Application**: Generate README.md and configuration files from templates
3. **Documentation**: Create essential documentation files
4. **Development Setup**: Configure tooling, testing, and CI/CD
5. **Git Initialization**: Set up version control with initial commit

## Project Initialization Workflow

### Phase 1: Requirements Gathering
- [ ] Collect project name and description
- [ ] Determine technology stack and framework
- [ ] Identify database and external services
- [ ] Define deployment strategy and environment
- [ ] Gather author information and licensing

### Phase 2: Structure Creation
- [ ] Create standard directory structure
- [ ] Generate core configuration files
- [ ] Set up development tooling configuration
- [ ] Create environment template files
- [ ] Initialize testing framework structure

### Phase 3: Template Application
- [ ] Generate README.md from template with project variables
- [ ] Create package.json with appropriate dependencies
- [ ] Generate TypeScript and build configurations
- [ ] Create Docker and CI/CD configuration files
- [ ] Set up linting and formatting configurations

### Phase 4: Documentation Setup
- [ ] Create REQUIREMENTS.md for project specifications
- [ ] Generate ARCHITECTURE.md for technical decisions
- [ ] Set up API_DESIGN.md for API documentation
- [ ] Create TESTING_STRATEGY.md for testing approach
- [ ] Generate DEPLOYMENT.md for deployment instructions

### Phase 5: Development Environment
- [ ] Install base dependencies and development tools
- [ ] Configure IDE settings and extensions
- [ ] Set up pre-commit hooks and quality gates
- [ ] Initialize database schema and migrations
- [ ] Create sample environment configuration

### Phase 6: Version Control & Finalization
- [ ] Initialize git repository with appropriate .gitignore
- [ ] Create initial commit with project setup
- [ ] Set up branch protection and workflow rules
- [ ] Generate project summary and next steps
- [ ] Validate setup with basic health checks

## Template Variables

The following variables will be collected and applied to templates:

### Required Variables
- **PROJECT_NAME** - Project name in kebab-case (e.g., "my-awesome-app")
- **PROJECT_TITLE** - Project title in Title Case (e.g., "My Awesome App")  
- **PROJECT_DESCRIPTION** - Brief description of project purpose and functionality

### Optional Variables
- **TECH_STACK** - Primary technology stack (React, Node.js, Python, etc.)
- **NODE_VERSION** - Required Node.js version (default: 18)
- **DATABASE** - Database system (PostgreSQL, MongoDB, Redis, etc.)
- **AUTHOR_NAME** - Project author/maintainer name
- **LICENSE** - License type (MIT, Apache 2.0, GPL, etc.)
- **REPOSITORY_URL** - Git repository URL (if known)

## Generated File Structure

```
{PROJECT_NAME}/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD
├── docs/
│   ├── REQUIREMENTS.md           # Project requirements and specs
│   ├── ARCHITECTURE.md          # Technical architecture decisions
│   ├── API_DESIGN.md            # API documentation and contracts
│   ├── TESTING_STRATEGY.md      # Testing approach and guidelines
│   └── DEPLOYMENT.md            # Deployment instructions
├── src/
│   ├── components/              # Reusable UI components
│   ├── pages/                   # Application pages/routes
│   ├── services/               # Business logic and API calls
│   ├── utils/                  # Helper functions and utilities
│   └── types/                  # TypeScript type definitions
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore patterns
├── .eslintrc.js               # ESLint configuration
├── .prettierrc                # Prettier configuration
├── docker-compose.yml         # Docker Compose for development
├── Dockerfile                 # Docker container configuration
├── package.json               # Node.js dependencies and scripts
├── README.md                  # Project documentation (from template)
├── tsconfig.json              # TypeScript configuration
└── vite.config.ts             # Vite build configuration
```

## Usage Examples

```bash
# Initialize new React TypeScript project
/ck:init-project "My Dashboard App" "A modern dashboard for analytics and reporting"

# Initialize API project with specific database
/ck:init-project "User Management API" "RESTful API for user authentication and management" --database=postgresql

# Initialize full-stack project with specific tech stack
/ck:init-project "E-commerce Platform" "Modern e-commerce solution with React and Node.js" --stack="React,Node.js,PostgreSQL"
```

## Quality Assurance

### Pre-Generation Checks
- [ ] Verify directory is empty or confirm overwrite
- [ ] Check Node.js and npm installation
- [ ] Validate project name follows conventions
- [ ] Ensure required template variables are provided

### Post-Generation Validation
- [ ] Verify all files created successfully
- [ ] Check template variable substitution completed
- [ ] Test npm install runs without errors
- [ ] Validate TypeScript compilation works
- [ ] Confirm git repository initialized properly

### Integration Testing
- [ ] Run development server starts correctly
- [ ] Execute test suite passes
- [ ] Verify linting and type checking work
- [ ] Check build process completes successfully
- [ ] Validate Docker configuration works

## Best Practices Applied

- **Consistent Structure**: Follow established project organization patterns
- **Modern Tooling**: Use current best practices for development tools
- **Comprehensive Documentation**: Include all necessary project documentation
- **Security First**: Apply security best practices from project start
- **Testing Ready**: Set up testing framework and example tests
- **CI/CD Prepared**: Include GitHub Actions workflow for automation
- **Docker Support**: Include containerization for consistent environments
- **Environment Management**: Proper environment variable handling

## Integration Points

- **Claude Code Framework**: Integrates with existing commands and agents
- **Development Workflow**: Works with feature-developer and bug-fixer agents
- **Template System**: Uses standardized templates with variable substitution
- **Quality Gates**: Includes linting, testing, and type checking setup
- **Documentation Standards**: Creates consistent documentation structure