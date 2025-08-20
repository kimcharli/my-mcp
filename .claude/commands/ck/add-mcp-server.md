---
command: "/ck:add-mcp-server"
category: "Documentation & Configuration"
purpose: "Add MCP server entry to README.md with description, URL, and installation command"
wave-enabled: false
performance-profile: "standard"
agent: "feature-developer"
allowed-tools: Read(*), Edit(*), Write(*)
---

## Context

- Current README.md: @README.md
- MCP server configurations: @mcp.json @apify.json
- Project structure: !`find . -maxdepth 2 -type d`

## Task

Add a new MCP server entry to the README.md file in the "Third-Party Integrations" section. This command will:

1. **Server Information**: Gather server name, description, and reference URL
2. **Installation Command**: Generate appropriate `claude mcp add` command
3. **README Update**: Add entry to the Third-Party Integrations section
4. **Validation**: Ensure proper formatting and placement

## Server Entry Format

Each MCP server entry should follow this format in the Third-Party Integrations section:

```
- **Server Name** - One line description ([Reference URL](https://github.com/user/repo))
```

And if applicable, add installation command in the Client Configuration section:

```bash
claude mcp add server-name -- npx -y package-name
# or
claude mcp add server-name -e API_KEY=your_key -- npx -y package-name
```

## Workflow

### Phase 1: Information Gathering
- [ ] Extract server name from user input
- [ ] Extract or generate concise description (one line)
- [ ] Identify GitHub repository URL or reference URL
- [ ] Determine installation method (npm, GitHub, etc.)

### Phase 2: README Update
- [ ] Read current README.md structure
- [ ] Locate "Third-Party Integrations" section
- [ ] Add server entry in alphabetical order
- [ ] Maintain consistent formatting with existing entries

### Phase 3: Installation Commands
- [ ] Generate appropriate `claude mcp add` command
- [ ] Add to Client Configuration section if needed
- [ ] Include environment variable setup if required

### Phase 4: Validation
- [ ] Verify proper markdown formatting
- [ ] Check alphabetical ordering
- [ ] Ensure consistent style with existing entries
- [ ] Validate URL format and accessibility

## Usage Examples

```bash
# Add a server with basic info
/ck:add-mcp-server "glyph" "Symbol and icon management system" "https://github.com/benmyles/glyph"

# Add a server with npm package
/ck:add-mcp-server "weather-api" "Weather data and forecasting" "https://github.com/user/weather-mcp" "npx -y weather-mcp-server"

# Add a server with environment variables
/ck:add-mcp-server "api-service" "Custom API integration" "https://github.com/user/api-mcp" "npx -y api-mcp-server" "API_KEY"
```

## Integration Notes

- Maintains README.md consistency and formatting
- Follows existing documentation patterns
- Preserves alphabetical ordering in Third-Party Integrations
- Integrates with Claude Code MCP configuration workflow