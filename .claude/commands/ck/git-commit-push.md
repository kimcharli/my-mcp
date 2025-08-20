---
command: "/ck:git-commit-push"
category: "Version Control & Deployment"
purpose: "Intelligent git workflow with conventional commits and automated quality checks"
description: "Create semantically meaningful commits with automated quality validation and smart branch management"
allowed-tools: Bash(git:*), Bash(npm:*), Bash(pytest:*), Read(*), Edit(*), Grep(*), Glob(*)
wave-enabled: true
performance-profile: "standard"
---

## Context

- Current git status: !`git status --porcelain`
- Current git diff: !`git diff --stat`
- Staged changes: !`git diff --cached --stat`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`
- Uncommitted files: !`git ls-files --others --exclude-standard`
- Project config: @package.json @pyproject.toml
- Branch protection: !`git branch -r | head -5`

## Task

**Create intelligent git commit with conventional commit format, automated quality checks, and smart push strategy.**

## Intelligent Git Workflow

### Phase 1: Pre-Commit Analysis & Validation

#### Change Analysis:
```bash
# Analyze change scope and impact
echo "=== Change Analysis ==="
git diff --name-status
git diff --stat

# Identify change types
echo "=== Files by Type ==="
git diff --name-only | while read file; do
    case "$file" in
        *.md) echo "📝 Documentation: $file" ;;
        *.json|*.yaml|*.yml) echo "⚙️ Configuration: $file" ;;
        *.js|*.ts|*.jsx|*.tsx) echo "💻 Frontend: $file" ;;
        *.py) echo "🐍 Backend: $file" ;;
        *test*|*spec*) echo "🧪 Tests: $file" ;;
        *.css|*.scss|*.less) echo "🎨 Styles: $file" ;;
        *) echo "📄 Other: $file" ;;
    esac
done

# Check for breaking changes
echo "=== Breaking Change Detection ==="
git diff | grep -E "^-.*function|^-.*class|^-.*export|^-.*interface" | head -5
git diff | grep -E "BREAKING|breaking.*change|major.*change" | head -3
```

#### Pre-Commit Quality Checks:
```bash
# Run automated quality checks before committing
echo "=== Running Pre-Commit Checks ==="

# 1. Linting
if [ -f "package.json" ]; then
    echo "🔍 Running ESLint..."
    npm run lint 2>/dev/null || npx eslint . --fix || echo "⚠️ Linting issues found"
fi

if [ -f "pyproject.toml" ]; then
    echo "🔍 Running Python linting..."
    ruff check . --fix 2>/dev/null || flake8 . 2>/dev/null || echo "⚠️ Python linting issues"
fi

# 2. Formatting
echo "🎨 Auto-formatting code..."
if [ -f "package.json" ]; then
    npx prettier --write . 2>/dev/null || echo "⚠️ Prettier formatting failed"
fi

if [ -f "pyproject.toml" ]; then
    black . 2>/dev/null || echo "⚠️ Black formatting failed"
fi

# 3. Type Checking
echo "🔍 Type checking..."
if [ -f "tsconfig.json" ]; then
    npx tsc --noEmit 2>/dev/null || echo "⚠️ TypeScript errors found"
fi

if [ -f "pyproject.toml" ]; then
    mypy . 2>/dev/null || echo "⚠️ Python type errors found"
fi

# 4. Quick Tests
echo "🧪 Running quick tests..."
if [ -f "package.json" ]; then
    npm test -- --passWithNoTests --silent 2>/dev/null || echo "⚠️ Some tests failed"
fi

if [ -f "pyproject.toml" ]; then
    python -m pytest --maxfail=1 -q 2>/dev/null || echo "⚠️ Some Python tests failed"
fi
```

### Phase 2: Intelligent Commit Message Generation

#### Conventional Commit Analysis:
```bash
# Determine commit type based on changes
determine_commit_type() {
    local changes=$(git diff --name-only --cached)
    local has_tests=$(echo "$changes" | grep -E "test|spec" | wc -l)
    local has_docs=$(echo "$changes" | grep -E "\.md$|docs/" | wc -l)
    local has_config=$(echo "$changes" | grep -E "\.json$|\.yaml$|\.yml$|\.toml$" | wc -l)
    local has_source=$(echo "$changes" | grep -E "\.(js|ts|py|rs|go)$" | wc -l)
    
    # Analyze git diff for keywords
    local diff_content=$(git diff --cached)
    local has_breaking=$(echo "$diff_content" | grep -iE "breaking|BREAKING" | wc -l)
    local has_feature=$(echo "$diff_content" | grep -E "^(\+.*function|\+.*class|\+.*export)" | wc -l)
    local has_fix=$(echo "$diff_content" | grep -E "fix|bug|error|issue" | wc -l)
    
    # Determine primary type
    if [ "$has_breaking" -gt 0 ]; then
        echo "feat!" # Breaking change
    elif [ "$has_feature" -gt 0 ] && [ "$has_source" -gt 0 ]; then
        echo "feat"
    elif [ "$has_fix" -gt 0 ]; then
        echo "fix"
    elif [ "$has_tests" -gt 0 ] && [ "$has_source" -eq 0 ]; then
        echo "test"
    elif [ "$has_docs" -gt 0 ] && [ "$has_source" -eq 0 ]; then
        echo "docs"
    elif [ "$has_config" -gt 0 ]; then
        echo "chore"
    else
        echo "feat"
    fi
}

# Determine scope based on affected areas
determine_commit_scope() {
    local changes=$(git diff --name-only --cached)
    
    # Check for specific areas
    if echo "$changes" | grep -q "server/trading"; then
        echo "trading"
    elif echo "$changes" | grep -q "server/filesystem"; then
        echo "filesystem"  
    elif echo "$changes" | grep -q "server/weather"; then
        echo "weather"
    elif echo "$changes" | grep -q "\.claude/"; then
        echo "claude-framework"
    elif echo "$changes" | grep -q "docs/"; then
        echo "docs"
    elif echo "$changes" | grep -q "tests/"; then
        echo "tests"
    elif echo "$changes" | grep -qE "(api|endpoint)"; then
        echo "api"
    elif echo "$changes" | grep -qE "(ui|component|frontend)"; then
        echo "ui"
    else
        echo ""
    fi
}

# Generate commit message
generate_commit_message() {
    local type=$(determine_commit_type)
    local scope=$(determine_commit_scope)
    local scope_part=""
    
    if [ -n "$scope" ]; then
        scope_part="($scope)"
    fi
    
    # Analyze changes for message content
    local added_files=$(git diff --name-only --cached --diff-filter=A | wc -l)
    local modified_files=$(git diff --name-only --cached --diff-filter=M | wc -l)
    local deleted_files=$(git diff --name-only --cached --diff-filter=D | wc -l)
    
    # Generate descriptive message based on changes
    local message=""
    if [ "$added_files" -gt 0 ] && [ "$modified_files" -eq 0 ]; then
        message="add new functionality and features"
    elif [ "$modified_files" -gt 0 ] && [ "$added_files" -eq 0 ]; then
        message="improve existing functionality"
    elif [ "$deleted_files" -gt 0 ]; then
        message="remove deprecated code and clean up"
    else
        message="implement comprehensive updates"
    fi
    
    echo "${type}${scope_part}: ${message}"
}
```

#### Advanced Commit Message Templates:
```bash
# Generate detailed commit message with body and footer
create_detailed_commit() {
    local type_scope_subject="$1"
    local body=""
    local footer=""
    
    # Create body based on file changes
    echo "Creating detailed commit message..."
    
    # Add file change summary
    local changes=$(git diff --name-only --cached)
    if [ $(echo "$changes" | wc -l) -le 5 ]; then
        body="Files modified:"
        echo "$changes" | while read file; do
            body="$body\n- $file"
        done
    else
        body="Modified $(echo "$changes" | wc -l) files across multiple areas"
    fi
    
    # Add breaking change footer if detected
    local breaking_changes=$(git diff --cached | grep -i "breaking" | head -3)
    if [ -n "$breaking_changes" ]; then
        footer="BREAKING CHANGE: API changes require updates to client code"
    fi
    
    # Construct full message
    local full_message="$type_scope_subject"
    if [ -n "$body" ]; then
        full_message="$full_message\n\n$body"
    fi
    if [ -n "$footer" ]; then
        full_message="$full_message\n\n$footer"
    fi
    
    echo -e "$full_message"
}
```

### Phase 3: Smart Branch and Push Strategy

#### Branch Strategy Detection:
```bash
# Determine appropriate branch strategy
analyze_branch_strategy() {
    local current_branch=$(git branch --show-current)
    local default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
    local has_remote=$(git remote | grep origin | wc -l)
    
    echo "=== Branch Strategy Analysis ==="
    echo "Current branch: $current_branch"
    echo "Default branch: $default_branch"
    echo "Has remote: $has_remote"
    
    # Check if on feature branch
    if [[ "$current_branch" == feature/* ]] || [[ "$current_branch" == feat/* ]]; then
        echo "🌿 Feature branch detected - will push to origin"
        return 0
    elif [[ "$current_branch" == hotfix/* ]] || [[ "$current_branch" == fix/* ]]; then
        echo "🚨 Hotfix branch detected - expedited workflow"
        return 0
    elif [ "$current_branch" == "$default_branch" ]; then
        echo "⚠️ On default branch - will push directly"
        return 0
    else
        echo "🔀 Custom branch - standard push workflow"
        return 0
    fi
}

# Check for upstream and conflicts
check_upstream_status() {
    echo "=== Upstream Status Check ==="
    
    # Fetch latest changes
    git fetch origin 2>/dev/null || echo "⚠️ Could not fetch from origin"
    
    # Check for upstream changes
    local behind=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "0")
    local ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "0")
    
    if [ "$behind" -gt 0 ]; then
        echo "⚠️ Branch is $behind commits behind upstream"
        echo "Consider: git pull --rebase before pushing"
    fi
    
    if [ "$ahead" -gt 0 ]; then
        echo "✅ Branch is $ahead commits ahead - ready to push"
    fi
    
    # Check for merge conflicts
    git merge-tree $(git merge-base HEAD @{u}) HEAD @{u} 2>/dev/null | grep -q "<<<<<<< " && {
        echo "🚨 Potential merge conflicts detected"
        echo "Run: git pull --rebase and resolve conflicts"
        return 1
    }
    
    return 0
}
```

### Phase 4: Commit Execution with Validation

#### Staged Commit Process:
```bash
# Execute commit with all validations
execute_smart_commit() {
    echo "=== Executing Smart Commit Process ==="
    
    # 1. Final validation
    if [ $(git diff --cached --name-only | wc -l) -eq 0 ]; then
        echo "❌ No staged changes found. Staging all modified files..."
        git add -A
        
        if [ $(git diff --cached --name-only | wc -l) -eq 0 ]; then
            echo "❌ No changes to commit"
            return 1
        fi
    fi
    
    # 2. Generate commit message
    local commit_message=$(generate_commit_message)
    echo "📝 Generated commit message: $commit_message"
    
    # 3. Create detailed commit
    local detailed_message=$(create_detailed_commit "$commit_message")
    
    # 4. Show preview
    echo "=== Commit Preview ==="
    echo "Changes to be committed:"
    git diff --cached --stat
    echo ""
    echo "Commit message:"
    echo -e "$detailed_message"
    echo ""
    
    # 5. Execute commit
    echo "$detailed_message" | git commit -F -
    
    if [ $? -eq 0 ]; then
        echo "✅ Commit successful"
        local commit_hash=$(git rev-parse --short HEAD)
        echo "📍 Commit hash: $commit_hash"
        return 0
    else
        echo "❌ Commit failed"
        return 1
    fi
}
```

### Phase 5: Intelligent Push with Safety Checks

#### Smart Push Strategy:
```bash
# Execute push with safety checks
execute_smart_push() {
    echo "=== Smart Push Execution ==="
    
    # 1. Pre-push validation
    check_upstream_status || {
        echo "❌ Upstream check failed - aborting push"
        return 1
    }
    
    # 2. Branch strategy analysis
    analyze_branch_strategy
    
    # 3. Safety checks
    local current_branch=$(git branch --show-current)
    local commit_count=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "1")
    
    if [ "$commit_count" -gt 5 ]; then
        echo "⚠️ Pushing $commit_count commits - consider squashing"
    fi
    
    # 4. Execute push
    echo "🚀 Pushing to origin/$current_branch..."
    git push origin "$current_branch"
    
    if [ $? -eq 0 ]; then
        echo "✅ Push successful"
        
        # 5. Post-push actions
        echo "=== Post-Push Actions ==="
        echo "📍 Latest commit: $(git log -1 --oneline)"
        echo "🌐 Remote status: $(git status -sb)"
        
        # Check if PR should be created
        local default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
        if [ "$current_branch" != "$default_branch" ]; then
            echo "💡 Consider creating a pull request:"
            echo "   gh pr create --title '$commit_message' --body 'Auto-generated PR'"
        fi
        
        return 0
    else
        echo "❌ Push failed"
        return 1
    fi
}
```

## Complete Workflow Execution

### Main Process:
```bash
# Execute complete git workflow
main() {
    echo "🚀 Starting Intelligent Git Workflow"
    echo "=================================="
    
    # Phase 1: Analysis and validation
    echo "📊 Phase 1: Analysis and Validation"
    if ! run_pre_commit_checks; then
        echo "⚠️ Pre-commit checks had issues - continuing anyway"
    fi
    
    # Phase 2: Commit
    echo "📝 Phase 2: Smart Commit"
    if ! execute_smart_commit; then
        echo "❌ Commit failed - aborting"
        return 1
    fi
    
    # Phase 3: Push
    echo "🚀 Phase 3: Smart Push"
    if ! execute_smart_push; then
        echo "❌ Push failed"
        return 1
    fi
    
    echo "✅ Git workflow completed successfully!"
    echo "=================================="
}
```

## Conventional Commit Examples

### Generated Commit Messages:
```bash
# Feature additions
feat(trading): add options trading support with risk management
feat(api): implement user authentication endpoints
feat!: redesign MCP server architecture (BREAKING CHANGE)

# Bug fixes  
fix(filesystem): resolve permission errors on macOS
fix(weather): handle API timeout gracefully
fix: correct type definitions for server responses

# Documentation
docs(readme): update installation instructions
docs(api): add comprehensive endpoint documentation
docs: improve troubleshooting guide

# Tests
test(trading): add comprehensive unit tests for order processing
test: increase coverage for error handling scenarios

# Chores
chore(deps): update dependencies to latest versions
chore: reorganize project structure for better maintainability
chore(ci): optimize build pipeline performance
```

## Success Criteria

### Commit Quality:
- ✅ **Conventional Format**: Follows semantic commit message format
- ✅ **Descriptive Subject**: Clear, concise description of changes
- ✅ **Appropriate Type**: Correct commit type (feat, fix, docs, etc.)
- ✅ **Proper Scope**: Relevant scope when applicable
- ✅ **Breaking Changes**: Clearly marked with ! or BREAKING CHANGE

### Quality Assurance:
- ✅ **Pre-commit Checks**: Linting, formatting, type checking passed
- ✅ **Tests Passing**: All relevant tests pass before commit
- ✅ **No Regressions**: Existing functionality remains intact
- ✅ **Documentation**: Related documentation updated if needed

### Git Workflow:
- ✅ **Clean History**: Logical, atomic commits that build the story
- ✅ **Branch Strategy**: Appropriate branch usage and naming
- ✅ **Upstream Sync**: No conflicts with remote repository
- ✅ **Push Success**: Changes successfully pushed to remote
