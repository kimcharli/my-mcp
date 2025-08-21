---
name: add-subagent
description: Create a new subagent for Claude Code following official guidelines
allowed-tools: Read(**), Write(**), Edit(**), Glob(**)
argument-hint: [name] [description] --tools tool1,tool2 --proactive
model: claude-3-5-sonnet-20241022
---

# Add Subagent

Creates a new subagent configuration file following Claude Code guidelines. The subagent will be created in `.claude/agents/` directory with proper YAML frontmatter and structured markdown sections.

**Reference**: [Claude Code Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## Instructions

1. **Parse Command Arguments**
   - Extract subagent name from first argument (use kebab-case format)
   - Get description from second argument or remaining text
   - Parse optional flags:
     - `--tools`: Comma-separated list of tools the subagent can use
     - `--proactive`: Include proactive usage guidance in description

2. **Validate Subagent Specification**
   - Ensure name follows naming conventions (lowercase, hyphens)
   - Verify description is clear and specific about subagent's purpose
   - Validate tool names against available Claude Code tools:
     - Core tools: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`
     - Advanced tools: `Task`, `TodoWrite`, `MultiEdit`, `NotebookEdit`
     - External tools: `WebSearch`, `WebFetch`, `mcp__*`

3. **Create Subagent File Structure**
   Generate file at `.claude/agents/{name}-agent.md` with:

   **YAML Frontmatter:**
   ```yaml
   ---
   name: {name}
   description: {description with USE PROACTIVELY clause if --proactive flag}
   tools: {comma-separated tool list}
   ---
   ```

   **Markdown Sections:**
   - Main heading with subagent purpose
   - "When to Use Me" section with bullet points
   - "My Approach" section with numbered methodology
   - "Output Format" section describing deliverables
   - "Examples" section with concrete use cases

4. **Validate Generated File**
   - Check YAML frontmatter syntax
   - Verify all required sections are present
   - Ensure examples align with the subagent's stated purpose
   - Confirm file is saved in correct location

## Examples

### Example 1: Code Review Specialist
```
/ck:add-subagent code-reviewer "Reviews code for best practices, security issues, and maintainability" --tools Read,Grep,Edit --proactive
```
Creates a proactive code reviewer that analyzes pull requests and suggests improvements.

### Example 2: Database Migration Helper
```
/ck:add-subagent migration-helper "Assists with database schema changes and data migration scripts" --tools Read,Write,Bash,Grep
```
Creates a specialized subagent for database operations and migrations.

### Example 3: Documentation Generator
```
/ck:add-subagent doc-generator "Generates comprehensive documentation from code comments and structure" --tools Read,Write,Glob,Grep --proactive
```
Creates a documentation specialist that proactively identifies undocumented code.

### Example 4: Security Auditor
```
/ck:add-subagent security-auditor "Performs security analysis and vulnerability assessment" --tools Read,Grep,Glob,WebSearch
```
Creates a security-focused subagent with research capabilities.

## Subagent Structure Template

The generated subagent will follow this structure:

```markdown
---
name: {name}
description: {description}
tools: {tools}
---

# {Title Case Name}

{Expanded description of capabilities and specialization}

## When to Use Me

Invoke me when you need:
- {Specific use case 1}
- {Specific use case 2}
- {Specific use case 3}

## My Approach

### 1. {Phase 1 Name}
{Description of first phase}

### 2. {Phase 2 Name}  
{Description of second phase}

### 3. {Phase 3 Name}
{Description of final phase}

## Output Format

I always provide:
- **{Deliverable 1}**: {Description}
- **{Deliverable 2}**: {Description}
- **{Deliverable 3}**: {Description}

## Examples

**{Example 1 Title}**: {Brief description}
**{Example 2 Title}**: {Brief description}
```

## Tool Categories

**File Operations:** `Read`, `Write`, `Edit`, `MultiEdit`
**Search & Analysis:** `Grep`, `Glob`, `mcp__glyph__extract_symbols`
**System Operations:** `Bash`, `LS`
**Task Management:** `Task`, `TodoWrite`
**External Services:** `WebSearch`, `WebFetch`, `mcp__*`
**Development:** `NotebookEdit`, `mcp__ide__*`