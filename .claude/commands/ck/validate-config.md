---
command: "/ck:validate-config"
category: "Configuration & Validation"
purpose: "Comprehensive configuration validation and environment setup verification"
description: "Validate all configuration files, environment variables, and project setup for consistency and completeness"
allowed-tools: Bash(find:*), Bash(cat:*), Bash(node:*), Bash(python:*), Read(*), Grep(*), Glob(*)
wave-enabled: true
performance-profile: "standard"
agent: "bug-fixer"
---

## Context

- Project configuration files: !`find . -maxdepth 2 -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml"`
- Environment files: !`find . -name ".env*" -o -name "config.*"`
- Package files: @package.json @pyproject.toml @Cargo.toml @go.mod
- MCP configuration: @mcp.json @apify.json
- Current directory: !`pwd`
- Git status: !`git status --porcelain`

## Task

**Perform comprehensive validation of all project configuration files, environment setup, and dependencies.**

## Configuration Validation Workflow

### Phase 1: Configuration File Discovery & Analysis

#### File Discovery:
```bash
echo "=== Configuration File Discovery ==="

# Find all configuration files
find . -maxdepth 3 \( -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" -o -name "*.ini" \) -type f | while read file; do
    echo "📄 Config file: $file"
    # Check file size and modification time
    ls -lh "$file" | awk '{print "   Size: " $5 ", Modified: " $6 " " $7 " " $8}'
done

# Find environment files
find . -name ".env*" -type f | while read file; do
    echo "🔐 Environment file: $file"
done

# Find package configuration
find . -maxdepth 2 \( -name "package.json" -o -name "pyproject.toml" -o -name "Cargo.toml" -o -name "go.mod" -o -name "composer.json" \) | while read file; do
    echo "📦 Package config: $file"
done
```

### Phase 2: JSON/YAML Syntax Validation

#### Syntax Validation:
```bash
echo "=== Configuration Syntax Validation ==="

# Validate JSON files
find . -name "*.json" -type f | while read file; do
    echo "🔍 Validating JSON: $file"
    if ! python -m json.tool "$file" > /dev/null 2>&1; then
        echo "❌ Invalid JSON syntax in $file"
        python -m json.tool "$file" 2>&1 | head -3
    else
        echo "✅ Valid JSON: $file"
    fi
done

# Validate YAML files
find . \( -name "*.yaml" -o -name "*.yml" \) -type f | while read file; do
    echo "🔍 Validating YAML: $file"
    if command -v python >/dev/null 2>&1; then
        python -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Valid YAML: $file"
        else
            echo "❌ Invalid YAML syntax in $file"
        fi
    else
        echo "⚠️ Python not available for YAML validation"
    fi
done

# Validate TOML files
find . -name "*.toml" -type f | while read file; do
    echo "🔍 Validating TOML: $file"
    if command -v python >/dev/null 2>&1; then
        python -c "import tomllib; tomllib.load(open('$file', 'rb'))" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ Valid TOML: $file"
        else
            echo "❌ Invalid TOML syntax in $file"
        fi
    else
        echo "⚠️ Python tomllib not available for TOML validation"
    fi
done
```

### Phase 3: MCP Configuration Validation

#### MCP Server Configuration:
```bash
echo "=== MCP Configuration Validation ==="

# Validate mcp.json structure
if [ -f "mcp.json" ]; then
    echo "🔍 Validating MCP configuration..."
    
    # Check required structure
    python -c "
import json
try:
    with open('mcp.json') as f:
        config = json.load(f)
    
    if 'mcpServers' not in config:
        print('❌ Missing mcpServers section in mcp.json')
    else:
        servers = config['mcpServers']
        print(f'✅ Found {len(servers)} MCP servers configured')
        
        for name, server_config in servers.items():
            print(f'📡 Server: {name}')
            if 'command' not in server_config:
                print(f'   ❌ Missing command for server {name}')
            else:
                print(f'   ✅ Command: {server_config[\"command\"]}')
            
            if 'args' in server_config:
                print(f'   ✅ Args: {len(server_config[\"args\"])} arguments')
            
            if 'env' in server_config:
                print(f'   🔐 Environment variables: {len(server_config[\"env\"])}')

except Exception as e:
    print(f'❌ Error validating mcp.json: {e}')
" 2>/dev/null || echo "⚠️ Could not validate mcp.json"
else
    echo "⚠️ No mcp.json found"
fi

# Validate apify.json if present
if [ -f "apify.json" ]; then
    echo "🔍 Validating Apify configuration..."
    python -m json.tool apify.json > /dev/null 2>&1 && echo "✅ Valid apify.json" || echo "❌ Invalid apify.json"
fi
```

### Phase 4: Package Configuration Validation

#### Node.js Package Validation:
```bash
if [ -f "package.json" ]; then
    echo "=== Node.js Package Validation ==="
    
    # Check package.json structure
    echo "🔍 Validating package.json structure..."
    node -e "
    const pkg = require('./package.json');
    console.log('✅ Package name:', pkg.name || 'Not specified');
    console.log('✅ Version:', pkg.version || 'Not specified');
    console.log('✅ Dependencies:', Object.keys(pkg.dependencies || {}).length);
    console.log('✅ DevDependencies:', Object.keys(pkg.devDependencies || {}).length);
    console.log('✅ Scripts:', Object.keys(pkg.scripts || {}).length);
    
    // Check for common required scripts
    const scripts = pkg.scripts || {};
    const recommendedScripts = ['start', 'test', 'build', 'lint'];
    recommendedScripts.forEach(script => {
        if (scripts[script]) {
            console.log('✅ Script found:', script);
        } else {
            console.log('⚠️ Recommended script missing:', script);
        }
    });
    " 2>/dev/null || echo "❌ Could not validate package.json"
    
    # Check for package-lock.json or yarn.lock
    if [ -f "package-lock.json" ]; then
        echo "✅ package-lock.json found (npm)"
    elif [ -f "yarn.lock" ]; then
        echo "✅ yarn.lock found (yarn)"
    else
        echo "⚠️ No lock file found (package-lock.json or yarn.lock)"
    fi
fi
```

#### Python Package Validation:
```bash
if [ -f "pyproject.toml" ]; then
    echo "=== Python Package Validation ==="
    
    echo "🔍 Validating pyproject.toml structure..."
    python -c "
import tomllib
try:
    with open('pyproject.toml', 'rb') as f:
        config = tomllib.load(f)
    
    if 'project' in config:
        project = config['project']
        print('✅ Project name:', project.get('name', 'Not specified'))
        print('✅ Version:', project.get('version', 'Not specified'))
        print('✅ Dependencies:', len(project.get('dependencies', [])))
        
        if 'optional-dependencies' in project:
            opt_deps = project['optional-dependencies']
            for group, deps in opt_deps.items():
                print(f'✅ Optional dependencies ({group}):', len(deps))
    
    if 'build-system' in config:
        print('✅ Build system configured')
    else:
        print('⚠️ No build-system specified')
        
    if 'tool' in config:
        tools = config['tool']
        for tool in ['black', 'pytest', 'mypy', 'ruff']:
            if tool in tools:
                print(f'✅ Tool configured: {tool}')

except Exception as e:
    print(f'❌ Error validating pyproject.toml: {e}')
" 2>/dev/null || echo "❌ Could not validate pyproject.toml"
    
    # Check for UV lock file
    if [ -f "uv.lock" ]; then
        echo "✅ uv.lock found"
    else
        echo "⚠️ No uv.lock found"
    fi
fi
```

### Phase 5: Environment Variable Validation

#### Environment Configuration:
```bash
echo "=== Environment Configuration Validation ==="

# Check for environment files
if [ -f ".env" ]; then
    echo "🔐 Found .env file"
    echo "   ⚠️ Warning: .env files should not be committed to git"
    
    # Check if .env is in .gitignore
    if [ -f ".gitignore" ] && grep -q "\.env" .gitignore; then
        echo "   ✅ .env is in .gitignore"
    else
        echo "   ❌ .env should be added to .gitignore"
    fi
fi

if [ -f ".env.example" ]; then
    echo "✅ Found .env.example template"
    
    # Compare .env and .env.example if both exist
    if [ -f ".env" ]; then
        echo "🔍 Comparing .env with .env.example..."
        
        # Extract variable names (ignore comments and empty lines)
        env_vars=$(grep -E '^[A-Z_]+=.*' .env 2>/dev/null | cut -d= -f1 | sort)
        example_vars=$(grep -E '^[A-Z_]+=.*' .env.example 2>/dev/null | cut -d= -f1 | sort)
        
        # Check for missing variables
        for var in $example_vars; do
            if ! echo "$env_vars" | grep -q "^$var$"; then
                echo "   ⚠️ Variable $var missing from .env"
            fi
        done
        
        # Check for extra variables
        for var in $env_vars; do
            if ! echo "$example_vars" | grep -q "^$var$"; then
                echo "   ℹ️ Extra variable $var in .env (not in example)"
            fi
        done
    fi
else
    echo "⚠️ No .env.example template found"
fi

# Check for environment variables in current shell
echo "🔍 Checking critical environment variables..."
critical_vars="NODE_ENV PYTHON_PATH PATH"
for var in $critical_vars; do
    if [ -n "${!var}" ]; then
        echo "✅ $var is set"
    else
        echo "⚠️ $var is not set"
    fi
done
```

### Phase 6: Dependency and Version Validation

#### Dependency Validation:
```bash
echo "=== Dependency Validation ==="

# Node.js dependencies
if [ -f "package.json" ]; then
    echo "🔍 Checking Node.js dependencies..."
    
    # Check for npm audit
    if command -v npm >/dev/null 2>&1; then
        echo "🔒 Running npm audit..."
        npm audit --audit-level=high 2>/dev/null | head -10 || echo "⚠️ npm audit check completed"
    fi
    
    # Check for outdated packages
    if command -v npm >/dev/null 2>&1; then
        echo "📦 Checking for outdated packages..."
        npm outdated 2>/dev/null | head -5 || echo "✅ Package versions checked"
    fi
fi

# Python dependencies
if [ -f "pyproject.toml" ]; then
    echo "🔍 Checking Python dependencies..."
    
    # Check for safety (security audit)
    if command -v safety >/dev/null 2>&1; then
        echo "🔒 Running safety check..."
        safety check 2>/dev/null | head -5 || echo "⚠️ Safety check completed"
    fi
    
    # Check UV sync status
    if command -v uv >/dev/null 2>&1; then
        echo "📦 Checking UV sync status..."
        uv sync --dry-run 2>/dev/null | head -3 || echo "✅ UV dependencies checked"
    fi
fi
```

### Phase 7: File Permissions and Security

#### Security Validation:
```bash
echo "=== Security and Permissions Validation ==="

# Check file permissions on config files
echo "🔒 Checking configuration file permissions..."
find . -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" | while read file; do
    perms=$(ls -l "$file" | cut -d' ' -f1)
    if [[ "$perms" == *"w"*"w"* ]]; then
        echo "⚠️ $file is world-writable ($perms)"
    else
        echo "✅ $file has appropriate permissions ($perms)"
    fi
done

# Check for sensitive data in config files
echo "🔍 Scanning for potential sensitive data..."
find . -name "*.json" -o -name "*.yaml" -o -name "*.yml" | xargs grep -iE "password|secret|key|token" 2>/dev/null | while read match; do
    echo "⚠️ Potential sensitive data: $match"
done

# Check .gitignore coverage
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore found"
    
    # Check for common patterns
    patterns=("node_modules" "*.log" ".env" "__pycache__" "*.pyc" "target/" "dist/")
    for pattern in "${patterns[@]}"; do
        if grep -q "$pattern" .gitignore; then
            echo "✅ .gitignore includes: $pattern"
        else
            echo "⚠️ Consider adding to .gitignore: $pattern"
        fi
    done
else
    echo "❌ No .gitignore found"
fi
```

## Validation Report Generation

### Summary Report:
```bash
generate_validation_report() {
    echo "=== Configuration Validation Summary ==="
    echo "Generated on: $(date)"
    echo "Project: $(basename $(pwd))"
    echo ""
    
    # Count files validated
    config_files=$(find . -maxdepth 3 \( -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" \) | wc -l)
    env_files=$(find . -name ".env*" | wc -l)
    
    echo "📊 Files Validated:"
    echo "   - Configuration files: $config_files"
    echo "   - Environment files: $env_files"
    echo "   - Package files: $(find . -maxdepth 2 \( -name "package.json" -o -name "pyproject.toml" \) | wc -l)"
    echo ""
    
    echo "🎯 Validation Categories:"
    echo "   ✅ Syntax validation completed"
    echo "   ✅ MCP configuration checked"
    echo "   ✅ Package configuration validated"
    echo "   ✅ Environment setup verified"
    echo "   ✅ Dependencies analyzed"
    echo "   ✅ Security permissions checked"
    echo ""
    
    echo "💡 Recommendations:"
    echo "   - Review any ⚠️ warnings above"
    echo "   - Ensure sensitive data is not committed"
    echo "   - Keep dependencies updated and secure"
    echo "   - Validate changes after configuration updates"
}
```

## Quick Fix Suggestions

### Common Issues and Fixes:
```bash
# Fix common configuration issues
echo "=== Quick Fix Suggestions ==="

# Missing .gitignore entries
if [ -f ".gitignore" ]; then
    if ! grep -q "node_modules" .gitignore 2>/dev/null; then
        echo "💡 Add to .gitignore: node_modules/"
    fi
    if ! grep -q "\.env$" .gitignore 2>/dev/null; then
        echo "💡 Add to .gitignore: .env"
    fi
    if ! grep -q "__pycache__" .gitignore 2>/dev/null; then
        echo "💡 Add to .gitignore: __pycache__/"
    fi
fi

# Package.json improvements
if [ -f "package.json" ]; then
    if ! grep -q '"engines"' package.json; then
        echo "💡 Consider adding engines field to package.json"
    fi
    if ! grep -q '"repository"' package.json; then
        echo "💡 Consider adding repository field to package.json"
    fi
fi

# Environment template
if [ -f ".env" ] && [ ! -f ".env.example" ]; then
    echo "💡 Create .env.example template from .env (without sensitive values)"
fi
```

## Success Criteria

### Validation Completeness:
- ✅ **All Config Files Found**: Discovered and analyzed all configuration files
- ✅ **Syntax Validation**: All JSON/YAML/TOML files have valid syntax
- ✅ **MCP Configuration**: MCP servers properly configured and validated
- ✅ **Package Configuration**: Node.js/Python packages properly structured
- ✅ **Environment Setup**: Environment variables properly configured
- ✅ **Security Check**: No sensitive data in committed files
- ✅ **Dependencies**: All dependencies valid and secure

### Quality Standards:
- ✅ **No Syntax Errors**: All configuration files parse correctly
- ✅ **Complete Coverage**: All required configuration present
- ✅ **Security Compliance**: Sensitive data properly handled
- ✅ **Dependency Health**: No critical security vulnerabilities
- ✅ **File Permissions**: Appropriate permissions on all files
- ✅ **Documentation**: Configuration properly documented
