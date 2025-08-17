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

Ensure consistency across user, developer, and AI agent documentation.

## 1. Documentation Structure

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

### Execution Steps

1. **Analyze Impact** - Review code changes and identify documentation needs
2. **Structure Analysis** - Run smart documentation organization analysis
3. **Smart Reorganization** - Execute file migration and link updates FIRST (if needed)
4. **Update Core Files** - README.md, CLAUDE.md, CHANGELOG.md with new features using correct paths
5. **Update Specialized Docs** - API references, configuration guides, troubleshooting with correct paths
6. **Quality Check** - Validate links, examples, consistency, completeness

## 6. Smart Documentation Organization

> ⚠️ **CRITICAL SEQUENCING**: File reorganization MUST happen BEFORE content updates to prevent broken cross-references. The execution steps are ordered correctly to avoid this issue.

### Analyze Current Structure
```bash
# Discover documentation structure issues
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
# Execute smart reorganization (with safety checks) 
# ⚠️ MUST RUN BEFORE updating file content to avoid broken links
reorganize_documentation() {
    echo "=== Documentation Reorganization (BEFORE content updates) ==="
    
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

### Essential Updates

- ✅ **README.md** - Feature coverage, installation, usage examples
- ✅ **CLAUDE.md** - AI assistant context and integration patterns  
- ✅ **CHANGELOG.md** - Version history with recent changes
- ✅ **Configuration docs** - Environment variables, setup guides
- ✅ **API/Technical docs** - Updated specifications and procedures

### Quality Validation

- ✅ **Link integrity** - All cross-references working
- ✅ **Example accuracy** - Code snippets tested and current
- ✅ **Consistency** - Terminology, formatting, versioning aligned
- ✅ **Completeness** - All features documented appropriately

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
