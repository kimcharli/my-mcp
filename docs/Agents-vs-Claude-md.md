# AGENTS.md vs CLAUDE.md: Understanding the Difference

Both `AGENTS.md` and `CLAUDE.md` are designed for AI agents, but they serve **different purposes** in the AI-assisted development workflow.

## The Core Difference

**AGENTS.md** = "How to work on this project" (Machine-readable instructions)

**CLAUDE.md** = "What this project does and how to help users with it" (AI context and capabilities)

## Conceptual Framework

### AGENTS.md (Developer Agent Instructions)
**Role**: AI as a **developer/contributor** to the codebase

**Questions it answers:**
- How do I build this project?
- How do I run tests?
- What are the commit message conventions?
- What coding style should I follow?
- Where are the key files located?

**Example content:**
```markdown
### Building and Testing
- Run `pnpm turbo run test --filter <project_name>`
- Fix any test or type errors until the whole suite is green
- After moving files, run `pnpm lint --filter <project_name>`

### PR instructions
- Title format: [<project_name>] <Title>
- Always run `pnpm lint` and `pnpm test` before committing
```

### CLAUDE.md (Project Capabilities Guide)
**Role**: AI as a **user assistant** working with the project's features

**Questions it answers:**
- What can this project do for users?
- What APIs/tools are available?
- How should I help users interact with these capabilities?
- What are the safety considerations?
- What workflows should I guide users through?

**Example content:**
```markdown
### Trading Server
**Primary Use Case:** Stock market analysis, paper trading

**Key Tools Available:**
- `get_quote(symbol)` - Real-time stock prices
- `submit_order(symbol, action, quantity)` - Place trades

**AI Usage Patterns:**
"Get the current price for Apple (AAPL)"
"Place a buy order for 50 shares of Tesla"

**Safety Features:**
- Paper trading mode by default (no real money at risk)
```

## Practical Example: Weather Service

### AGENTS.md Content
```markdown
# Weather Service Agent Guide

## Setup
1. Install dependencies: `npm install`
2. Set API key in `.env`: `WEATHER_API_KEY=xxx`
3. Run tests: `npm test`

## Coding Conventions
- Use TypeScript strict mode
- All API calls must have timeout handling
- Cache weather data for 5 minutes

## Commit Format
- feat: Add new weather endpoint
- fix: Handle API timeout errors
```

### CLAUDE.md Content
```markdown
# Weather Service - AI Assistant Guide

## Core Capabilities

### Weather API
**Primary Use Case:** Real-time weather data and forecasting

**Key Tools Available:**
- `get_current_weather(location)` - Current conditions
- `get_forecast(location, days)` - Multi-day forecast

**AI Usage Patterns:**
"What's the weather in San Francisco?"
"Give me a 7-day forecast for London"

**Safety Features:**
- Input validation for location names
- Rate limiting (100 requests/hour)

## AI Assistant Best Practices
1. Always validate location before querying
2. Suggest related queries (e.g., "Want the weekly forecast?")
3. Handle API failures gracefully with cached data
```

## When AI Uses Each File

| Scenario | Uses AGENTS.md | Uses CLAUDE.md |
|----------|----------------|----------------|
| User: "Add a new feature to show humidity" | ✅ (needs build/test process) | ✅ (needs to understand existing weather features) |
| User: "What's the weather in Tokyo?" | ❌ (not building code) | ✅ (using project capabilities) |
| User: "Fix the failing tests" | ✅ (needs test commands) | ❌ (doesn't need feature context) |
| User: "Help me analyze stocks" | ❌ (not building code) | ✅ (needs trading tool context) |
| User: "Refactor the authentication module" | ✅ (needs coding standards) | ✅ (needs to understand auth features) |
| User: "Create a pull request for my changes" | ✅ (needs PR conventions) | ❌ (process-focused) |

## Detailed Comparison

| Aspect | AGENTS.md | CLAUDE.md |
|--------|-----------|-----------|
| **Primary Purpose** | Development workflow instructions | Feature capabilities and usage guidance |
| **Target Audience** | AI as code contributor | AI as user assistant |
| **Content Type** | Commands, conventions, build steps | APIs, tools, workflows, examples |
| **Format Style** | Machine-readable, imperative | Rich documentation, explanatory |
| **Focus** | How to build/test/commit | What the project does and how to use it |
| **Examples Include** | Shell commands, lint rules | User prompts, API calls, safety features |
| **Updates When** | Build process changes | Features added or APIs change |
| **Validation** | CI/CD compatibility | User interaction accuracy |

## Content Breakdown

### AGENTS.md Typical Sections
1. **Project Structure** - Directory layout, file organization
2. **Setup and Build Commands** - Installation, compilation, packaging
3. **Test Commands** - Running tests, coverage requirements
4. **Code Style and Conventions** - Linting, formatting, naming
5. **Commit Guidelines** - Message format, PR templates
6. **Security Policies** - Vulnerability reporting, secrets handling
7. **Dependencies** - Package management, version constraints

### CLAUDE.md Typical Sections
1. **Repository Overview** - What the project does, key features
2. **Core Capabilities** - Features with usage patterns and examples
3. **Third-Party Integrations** - External services, APIs, SDKs
4. **AI Assistant Best Practices** - Tool selection, error handling, safety
5. **Configuration Context** - Environment setup, API keys
6. **Development Guidance** - Coding standards for feature development
7. **Troubleshooting Context** - Common issues, resolution strategies
8. **AI Assistant Expectations** - Response quality, explanation level

## Why Both Are Needed

### AGENTS.md Ensures:
- ✅ Code contributions follow project standards
- ✅ Tests pass before commits
- ✅ Build process is consistent
- ✅ Development environment is correct
- ✅ Code quality is maintained
- ✅ Team conventions are followed

### CLAUDE.md Ensures:
- ✅ AI understands what the project can do
- ✅ AI guides users to use features correctly
- ✅ Safety features are respected
- ✅ Workflows are helpful and accurate
- ✅ Integration context is available
- ✅ Best practices are followed when assisting users

## Complementary Relationship

These files work together to make AI assistants effective at **both building the project AND helping users use it**.

### Example: Adding a New Feature

**Step 1: Development Phase** (Uses AGENTS.md)
```
AI reads AGENTS.md to understand:
- Where to place new code files
- What testing framework to use
- What coding style to follow
- How to commit the changes
```

**Step 2: User Assistance Phase** (Uses CLAUDE.md)
```
AI reads CLAUDE.md to understand:
- What the new feature does
- How users should invoke it
- What safety features are in place
- What workflows to suggest
```

## Best Practices for Maintaining Both

### Keep AGENTS.md Updated When:
- Build system changes (new tools, commands)
- Testing framework updates
- Coding standards evolve
- Commit conventions change
- Project structure reorganizes

### Keep CLAUDE.md Updated When:
- New features are added
- APIs change or deprecate
- Integration points are added
- Safety features are enhanced
- Common user workflows change

### Cross-Reference When Appropriate
```markdown
# AGENTS.md
See CLAUDE.md for detailed feature capabilities and user workflows

# CLAUDE.md
See AGENTS.md for development setup and build instructions
```

## Common Mistakes to Avoid

❌ **Don't put build commands in CLAUDE.md**
- Build commands belong in AGENTS.md
- CLAUDE.md focuses on feature usage, not development process

❌ **Don't put feature documentation in AGENTS.md**
- Feature docs belong in CLAUDE.md
- AGENTS.md focuses on how to contribute, not what features exist

❌ **Don't duplicate content across both files**
- Each file has a distinct purpose
- Reference the other file when context overlaps

✅ **Do use both files together**
- AI needs both perspectives for comprehensive assistance
- Development context (AGENTS.md) + Feature context (CLAUDE.md) = Complete AI capability

## File Location Conventions

### AGENTS.md Placement
```
project-root/
├── AGENTS.md              # Root level, primary instructions
├── packages/
│   ├── service-a/
│   │   └── AGENTS.md      # Service-specific build instructions
│   └── service-b/
│       └── AGENTS.md      # Service-specific build instructions
```

### CLAUDE.md Placement
```
project-root/
├── CLAUDE.md              # Root level, project-wide context
├── .claude/
│   └── CLAUDE.md          # Alternative: hidden directory
└── packages/
    ├── service-a/
    │   └── CLAUDE.md      # Service-specific capabilities
    └── service-b/
        └── CLAUDE.md      # Service-specific capabilities
```

### Global User Configuration
```
~/.claude/
└── CLAUDE.md              # User-wide preferences (not in repo)
```

## Summary

**AGENTS.md and CLAUDE.md are complementary, not redundant:**

- **AGENTS.md** = Instructions for AI to **work on** the codebase
- **CLAUDE.md** = Context for AI to **work with** the project's capabilities

Both files enable AI assistants to be maximally effective, covering the full spectrum from code contribution to user assistance. Use both files together for the best AI-assisted development experience.

## Quick Reference

**When writing AGENTS.md, ask yourself:**
- "What commands does a developer need to run?"
- "What standards must code contributions follow?"
- "How do we ensure quality and consistency?"

**When writing CLAUDE.md, ask yourself:**
- "What can this project do for users?"
- "How should AI help users interact with features?"
- "What context makes AI assistance more accurate and helpful?"
