---
name: add-slash-command
description: Create a new Claude Code slash command following official documentation structure
allowed-tools: Read(**), Write(**), Edit(**)
argument-hint: [command-name] [description]
model: claude-3-5-sonnet-20241022
---

# Add Slash Command

Create a new Claude Code slash command with proper YAML frontmatter and markdown structure following the official Claude Code documentation.

**Reference**: [Claude Code Slash Commands Documentation](https://docs.anthropic.com/en/docs/claude-code/slash-commands)

## Instructions

1. **Collect Command Information:**
   - Command name (kebab-case format)
   - Brief description of what the command does
   - Tools the command needs (from allowed-tools list)
   - Arguments/parameters the command accepts
   - Target model (default: claude-3-5-sonnet-20241022)

2. **Create Command File:**
   Create a new file at `~/.claude/commands/{command-name}.md` with this structure:

   ```markdown
   ---
   name: command-name
   description: Brief description of what this command does
   allowed-tools: Tool1(**), Tool2(**), etc.
   argument-hint: [arg1] [arg2] --flag
   model: claude-3-5-sonnet-20241022
   ---
   
   # Command Name (Title Case)
   
   Detailed description of what this command accomplishes.
   
   ## Instructions
   
   Step-by-step instructions for Claude on how to execute this command:
   
   1. First step with specific actions
   2. Second step with tool usage
   3. Final step with validation
   
   ## Examples
   
   ### Example 1: Basic Usage
   ```
   /command-name arg1 arg2
   ```
   Description of what this does.
   
   ### Example 2: Advanced Usage
   ```
   /command-name arg1 --flag value
   ```
   Description of advanced scenario.
   ```

3. **YAML Frontmatter Fields:**
   - `name`: Kebab-case command name (required)
   - `description`: One-line description (required)
   - `allowed-tools`: Tools with permissions - use `(**)` for broad access (required)
   - `argument-hint`: Show expected arguments in brackets `[arg]` and flags `--flag` (optional)
   - `model`: Claude model to use (optional, defaults to latest)

4. **Tool Permission Format:**
   - `Bash(**)` - Full bash access
   - `Read(**)` - Read any file
   - `Write(**)` - Write any file
   - `Edit(**)` - Edit any file
   - `Grep(**)` - Search any file
   - `Glob(**)` - File pattern matching
   - Use specific patterns when needed: `Edit(*.js)`, `Read(/specific/path/*)`

5. **Validation Steps:**
   - Verify YAML frontmatter is valid
   - Test command with `claude /command-name` syntax
   - Ensure file is in correct location: `~/.claude/commands/`
   - Check that all required fields are present

## Process

1. **Gather Requirements**: Ask user for command name, description, tools needed, and arguments
2. **Generate File**: Create the command file with proper structure and frontmatter
3. **Validate Format**: Ensure YAML is correct and follows Claude Code standards
4. **Test Command**: Suggest testing the new command with example usage
5. **Documentation**: Explain how to use the new command

## Common Tool Combinations

- **File Operations**: `Read(**), Write(**), Edit(**)`
- **System Commands**: `Bash(**), Read(**)`
- **Code Analysis**: `Read(**), Grep(**), Glob(**)`
- **Development**: `Read(**), Write(**), Edit(**), Bash(**)`
- **Documentation**: `Read(**), Edit(**), Glob(**)`

## Examples

### Example 1: Simple File Command
```
/quick-edit README.md
```
Updates README.md with basic information.

### Example 2: System Analysis Command  
```
/analyze-project --deep
```
Performs comprehensive project analysis with detailed reporting.

### Example 3: Multi-step Workflow
```
/setup-environment production --config custom.json
```
Sets up environment with configuration and validation steps.