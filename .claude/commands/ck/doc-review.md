---
description: Comprehensively update all documentation after implementation
allowed-tools: Bash(ls:*), Bash(find:*), Bash(cat:*), Bash(git:*), Read(*), Write(*), Edit(*), MultiEdit(*), Grep(*), Glob(*), WebFetch(*)
---

## Context

- Project structure: !`find . -name "*.md" -o -name "*.rst" -o -name "*.txt" | head -20`
- Documentation files: !`find . -name "README*" -o -name "CHANGELOG*" -o -name "CLAUDE*" -o -name "GEMINI*" -o -name "*DOC*" -o -name "docs"`
- Recent changes: !`git diff --name-only HEAD~5..HEAD`
- Project info: !`cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null || cat Cargo.toml 2>/dev/null || echo "No package file found"`

## Task

**Update all documentation for:** $ARGUMENTS

**🚨 CRITICAL: Context-aware documentation updates that respect project design principles**

Ensure consistency across user, developer, and AI agent documentation while maintaining project-specific documentation philosophy.

## 🎯 STEP 0: PROJECT DOCUMENTATION PRINCIPLES EXTRACTION (CRITICAL - RUN FIRST)

**Before making ANY documentation changes, extract and validate project-specific documentation principles:**

### Documentation Philosophy Analysis:
```bash
# Extract key documentation design claims
grep -i "no.*config.*files\|zero.*setup\|interactive.*config\|self.*contained\|minimal.*docs\|single.*file\|documentation.*philosophy" README.md CLAUDE.md *.md

# Check for explicit documentation structure preferences
grep -i "directory.*structure\|file.*organization\|docs.*folder\|keep.*root\|avoid.*dirs" README.md CLAUDE.md *.md

# Look for configuration philosophy
grep -i "no.*env\|environment.*files\|configuration.*approach\|setup.*method" README.md CLAUDE.md *.md
```

### Critical Documentation Principles Detection:
- **"No .env files required"** → Flag any documentation suggesting .env setup
- **"Zero-config setup"** → Flag documentation adding configuration steps  
- **"Interactive configuration"** → Flag automated config file creation
- **"Self-contained architecture"** → Flag external dependency documentation
- **"Minimal documentation"** → Flag extensive documentation reorganization
- **"Single-file approach"** → Flag docs/ directory creation

### Contradiction Detection:
- Does project claim "no config files" but we're documenting .env setup?
- Does project claim "zero setup" but we're adding configuration documentation?
- Does project claim "minimal docs" but we're creating extensive structure?
- Does project have custom documentation philosophy that generic updates would violate?

**🚨 CRITICAL CHECKPOINT: If ANY contradiction detected, STOP and request user confirmation**

## 1. Context-Aware Documentation Structure

### Root Files (Keep for Visibility)
- `README.md` - Project overview & quick start
- `CLAUDE.md` - AI assistant integration guide  
- `GEMINI.md` - Gemini-specific docs (if applicable)
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - Legal information

### Optional Organized Structure (`docs/`)
```
docs/
├── user/           # Setup, usage, config, troubleshooting, FAQ
├── developer/      # Architecture, API, development, testing, deployment  
├── ai-agents/      # Context, templates, tool usage, best practices
└── technical/      # Requirements, security, performance, integration
```

### Organization Strategy
1. **Keep Essential** - Core info stays at root for discoverability
2. **Organize Detailed** - Move extensive content to `docs/` if project grows
3. **Link & Navigate** - Root files link to detailed docs, create index files
4. **Maintain Consistency** - Update cross-references, use relative links

Identify impact of changes on:
- Features, APIs, configurations, dependencies
- Installation, setup, testing procedures  
- Performance, security, compatibility

## 3. Documentation Updates

### README.md
- Update project description, features, installation
- Add quick start examples with new functionality
- Update configuration options and troubleshooting

### AI Agent Documentation
- **CLAUDE.md**: Add new feature context, tools, usage patterns, error handling
- **GEMINI.md**: Update model-specific instructions, function calling, optimization
- **AI Context**: Capability descriptions, business logic, decision trees

### Developer Documentation  
- **CHANGELOG.md**: Version entry, added/changed/fixed/deprecated sections
- **CONTRIBUTING.md**: Development setup, testing, code style updates
- **Architecture**: System design, API changes, security, performance considerations

### User & Technical Documentation
- **Configuration**: Environment variables, settings, security configuration
- **Deployment**: Infrastructure, Docker, CI/CD, monitoring updates
- **Testing**: New test categories, procedures, coverage requirements

## 4. Quality Assurance

### Consistency Checks
- Terminology alignment across documents
- Version consistency in references and examples  
- Link validation (internal and external)
- Format consistency (markdown, headings, code blocks)
- Example accuracy with actual implementation

### Completeness Validation
- Feature coverage in relevant documents
- Cross-reference validation between documents
- Remove outdated information
- Add missing documentation

### Context-Aware Execution Steps

**🚨 MANDATORY WORKFLOW: EXTRACT PRINCIPLES → VALIDATE CHANGES → APPLY OR FLAG → CONTINUE**

1. **Extract Design Principles** - Run STEP 0 project documentation principles analysis
2. **Validate Against Principles** - Check ALL proposed changes against documented philosophy
3. **Analyze Impact** - Review code changes and identify documentation needs (respecting principles)
4. **Structure Analysis** - Run smart documentation organization analysis (validate against principles)
5. **Principle-Validated Reorganization** - Execute file migration ONLY if doesn't violate documented philosophy
6. **Context-Aware Core Updates** - README.md, CLAUDE.md, CHANGELOG.md respecting project architecture claims
7. **Validated Specialized Docs** - API references, configuration guides (NO .env docs if "no .env files" documented)
8. **Quality Check** - Validate links, examples, consistency, completeness, principle compliance

## 6. Context-Aware Smart Documentation Organization

> ⚠️ **CRITICAL SEQUENCING**: Design principle validation → File reorganization → Content updates. The execution steps are ordered correctly to avoid this issue.

> 🚨 **CRITICAL**: Respect documented project philosophy. If project claims "minimal docs" or "single-file approach", DO NOT create extensive docs/ structure.

### Principle-Validated Structure Analysis
```bash
# STEP 1: Validate reorganization against project principles
echo "=== Design Principle Validation Check ==="

# Check if project forbids docs/ organization
if grep -q "minimal.*docs\|single.*file\|keep.*root\|avoid.*dirs" README.md CLAUDE.md *.md 2>/dev/null; then
    echo "⚠️  Project documents minimal/single-file approach - SKIP extensive reorganization"
    echo "✅ Respecting documented philosophy: maintain current structure"
    exit 0
fi

# STEP 2: Discover documentation structure issues (ONLY if principles allow)
echo "=== Documentation Structure Analysis ==="

# Find potential misplaced files in root
find . -maxdepth 1 -name "*.md" | grep -E "(EXAMPLES?|GUIDE|TUTORIAL|REFERENCE|API|SPEC|MANUAL)" | while read file; do
    echo "⚠️ Consider moving $file to docs/ - appears to be detailed documentation"
done

# Identify content that belongs in specific categories
find . -maxdepth 1 -name "*.md" -exec grep -l "## API\|### Endpoints\|curl.*http" {} \; | while read file; do
    echo "📘 $file contains API documentation - consider docs/developer/"
done

find . -maxdepth 1 -name "*.md" -exec grep -l "## Installation\|### Setup\|Getting Started" {} \; | while read file; do
    echo "👤 $file contains user guidance - consider docs/user/"
done

find . -maxdepth 1 -name "*.md" -exec grep -l "## Architecture\|### Design\|Technical.*Spec" {} \; | while read file; do
    echo "🏗️ $file contains architecture info - consider docs/technical/"
done

# Check file sizes to identify detailed vs summary docs
find . -maxdepth 1 -name "*.md" -exec wc -l {} \; | sort -nr | head -5 | while read lines file; do
    if [ "$lines" -gt 200 ]; then
        echo "📄 $file is large ($lines lines) - candidate for docs/ organization"
    fi
done
```

### Smart File Categorization
```bash
# Analyze file content and suggest reorganization
analyze_doc_files() {
    echo "=== Smart File Analysis ==="
    
    for file in *.md; do
        [ ! -f "$file" ] && continue
        
        # Skip essential root files
        case "$file" in
            "README.md"|"CLAUDE.md"|"GEMINI.md"|"CHANGELOG.md"|"CONTRIBUTING.md"|"LICENSE.md") 
                echo "✅ $file - Keep at root (essential)"
                continue ;;
        esac
        
        # Analyze content patterns
        local category=""
        local keywords=""
        
        if grep -q "## API\|### Endpoints\|Request/Response\|curl.*http\|POST\|GET\|PUT" "$file"; then
            category="developer"
            keywords="API documentation"
        elif grep -q "## Installation\|### Setup\|Getting Started\|Quick Start\|## Usage\|### Examples" "$file"; then
            category="user" 
            keywords="User guide"
        elif grep -q "## Architecture\|### Design\|Technical.*Spec\|## Security\|Performance\|Requirements" "$file"; then
            category="technical"
            keywords="Technical specification"
        elif grep -q "AI\|Claude\|Gemini\|Assistant\|Tool.*Usage\|Prompt" "$file"; then
            category="ai-agents"
            keywords="AI integration"
        fi
        
        if [ -n "$category" ]; then
            echo "📁 $file → docs/$category/ ($keywords)"
        else
            echo "❓ $file - Manual review needed"
        fi
    done
}
```

### Automated File Migration (CRITICAL: Do BEFORE content updates)
```bash
# Execute context-aware smart reorganization (with design principle validation) 
# ⚠️ MUST RUN BEFORE updating file content to avoid broken links
reorganize_documentation() {
    echo "=== Context-Aware Documentation Reorganization (AFTER principle validation) ==="
    
    # CRITICAL: Validate against project documentation principles first
    if grep -q "minimal.*docs\|single.*file\|keep.*root\|avoid.*dirs" README.md CLAUDE.md *.md 2>/dev/null; then
        echo "🚨 Project documents preference for minimal/single-file structure"
        echo "✅ SKIPPING reorganization to respect documented philosophy"
        return 0
    fi
    
    # STEP 1: Analyze and plan moves without executing
    echo "Planning file movements..."
    declare -a moves=()
    
    for file in *.md; do
        [ ! -f "$file" ] && continue
        
        # Skip essential root files
        case "$file" in
            "README.md"|"CLAUDE.md"|"GEMINI.md"|"CHANGELOG.md"|"CONTRIBUTING.md"|"LICENSE.md") 
                continue ;;
        esac
        
        # Determine target directory
        local target_dir=""
        if grep -q "## API\|### Endpoints" "$file"; then
            target_dir="docs/developer"
        elif grep -q "## Installation\|### Setup\|Getting Started" "$file"; then
            target_dir="docs/user"
        elif grep -q "## Architecture\|Technical.*Spec\|## Security" "$file"; then
            target_dir="docs/technical"
        elif grep -q "AI\|Claude\|Gemini\|Assistant" "$file"; then
            target_dir="docs/ai-agents"
        fi
        
        if [ -n "$target_dir" ]; then
            moves+=("$file:$target_dir")
            echo "📋 Plan: $file → $target_dir/"
        fi
    done
    
    # STEP 2: Create directory structure
    mkdir -p docs/{user,developer,ai-agents,technical}
    
    # STEP 3: Execute moves
    for move in "${moves[@]}"; do
        file="${move%:*}"
        target_dir="${move#*:}"
        echo "Moving $file to $target_dir/"
        mv "$file" "$target_dir/"
        echo "✅ Moved $file → $target_dir/"
    done
    
    # STEP 4: Update all cross-references immediately after moves
    update_documentation_links
    
    # STEP 5: Create navigation indexes
    create_docs_index_files
    
    echo "✅ Reorganization complete - files moved and links updated"
    echo "✅ Ready for content updates with correct file paths"
}
```

### Link Management & Updates
```bash
# Update cross-references after reorganization
update_documentation_links() {
    echo "=== Updating Cross-References ==="
    
    # Find and update broken links after file moves
    find . -name "*.md" -exec grep -l "]\(.*/.*\.md\)" {} \; | while read file; do
        echo "🔗 Checking links in $file"
        # Update relative links that may be broken after moves
        sed -i.bak 's|\](\.\/\([^)]*\)\.md)|\](docs/\1.md)|g' "$file"
        rm -f "$file.bak"
    done
    
    # Create navigation index files
    create_docs_index_files
}

create_docs_index_files() {
    # Create main docs index
    cat > docs/index.md << 'EOF'
# Documentation Index

## User Documentation
- [Getting Started](user/getting-started.md)
- [Usage Guide](user/usage-guide.md)
- [Configuration](user/configuration.md)
- [Troubleshooting](user/troubleshooting.md)

## Developer Documentation  
- [Architecture](developer/architecture.md)
- [API Reference](developer/api-reference.md)
- [Development Setup](developer/development.md)
- [Testing](developer/testing.md)

## AI Agent Integration
- [AI Context](ai-agents/context.md)
- [Tool Usage](ai-agents/tool-usage.md)
- [Best Practices](ai-agents/best-practices.md)

## Technical Specifications
- [Requirements](technical/requirements.md)
- [Security](technical/security.md)
- [Performance](technical/performance.md)
EOF

    # Create category-specific index files
    for category in user developer ai-agents technical; do
        [ -d "docs/$category" ] && ls "docs/$category"/*.md 2>/dev/null | while read file; do
            basename "$file" .md
        done | head -1 > /dev/null && cat > "docs/$category/index.md" << EOF
# $(echo $category | tr '-' ' ' | sed 's/\b\w/\U&/g') Documentation

$(ls docs/$category/*.md 2>/dev/null | while read file; do
    title=$(basename "$file" .md | tr '-' ' ' | sed 's/\b\w/\U&/g')
    echo "- [$title]($(basename "$file"))"
done)
EOF
    done
}
```

## Deliverables

### Context-Aware Essential Updates

- ✅ **README.md** - Feature coverage, installation, usage examples (respecting documented setup philosophy)
- ✅ **CLAUDE.md** - AI assistant context and integration patterns (maintaining project-specific approach)
- ✅ **CHANGELOG.md** - Version history with recent changes
- ✅ **Configuration docs** - ONLY if project design allows (NO .env docs if "no .env files" documented)
- ✅ **API/Technical docs** - Updated specifications respecting architectural claims

### Context-Aware Quality Validation

- ✅ **Design Principle Compliance** - ALL changes respect documented project philosophy
- ✅ **Link integrity** - All cross-references working
- ✅ **Example accuracy** - Code snippets tested and current (using project's preferred approach)
- ✅ **Consistency** - Terminology, formatting, versioning aligned with project claims
- ✅ **Completeness** - All features documented appropriately without violating architectural principles

### Smart Organization Features

- ✅ **Intelligent File Analysis** - Content-based categorization of documentation
- ✅ **Automated Migration** - Smart file movement with safety checks
- ✅ **Link Management** - Automatic cross-reference updates after reorganization
- ✅ **Index Generation** - Auto-created navigation files for organized structure

### Benefits Achieved

- **Comprehensive Coverage** - All changes documented with intelligent organization
- **User-Friendly** - Clear setup and usage guidance with logical structure
- **AI-Optimized** - Enhanced context for AI assistants with proper categorization
- **Maintainable** - Consistent structure, automated cross-references, and smart navigation
- **Scalable Organization** - Grows from simple to complex based on actual content analysis
