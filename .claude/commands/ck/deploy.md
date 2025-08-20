---
command: "/ck:deploy"
category: "Deployment & Operations"
purpose: "Intelligent deployment with environment validation and rollback capabilities"
description: "Deploy MCP servers and applications with comprehensive pre-deployment validation, environment setup, and automated rollback capabilities"
allowed-tools: Bash(git:*), Bash(npm:*), Bash(python:*), Bash(docker:*), Bash(ssh:*), Read(*), Write(*), Edit(*), Grep(*), Glob(*)
wave-enabled: true
performance-profile: "standard"
agent: "feature-developer"
---

## Context

- Current git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -5`
- Package configuration: @package.json @pyproject.toml
- Deployment config: !`find . -name "deploy*" -o -name "Dockerfile" -o -name "docker-compose*"`
- Environment files: !`find . -name ".env*"`
- Build artifacts: !`find . -name "dist" -o -name "build" -o -name "target" -type d`

## Task

**Execute intelligent deployment with comprehensive validation, environment setup, and rollback capabilities.**

## Deployment Workflow

### Phase 1: Pre-Deployment Validation

#### Environment and Prerequisites Check:
```bash
echo "=== Pre-Deployment Validation ==="

# 1. Git repository status
echo "🔍 Checking Git status..."
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️ Uncommitted changes detected:"
    git status --short
    echo "💡 Consider committing changes before deployment"
fi

# 2. Branch validation
current_branch=$(git branch --show-current)
echo "📍 Current branch: $current_branch"

# Check if on deployable branch
deployable_branches="main master production release"
is_deployable=false
for branch in $deployable_branches; do
    if [ "$current_branch" = "$branch" ]; then
        is_deployable=true
        break
    fi
done

if [ "$is_deployable" = false ]; then
    echo "⚠️ Deploying from non-standard branch: $current_branch"
    echo "💡 Consider deploying from: main, master, production, or release"
fi

# 3. Version tag validation
latest_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "No tags")
echo "🏷️ Latest tag: $latest_tag"

# 4. Remote sync check
echo "🌐 Checking remote sync..."
git fetch origin 2>/dev/null || echo "⚠️ Could not fetch from origin"

behind=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "0")
ahead=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "0")

if [ "$behind" -gt 0 ]; then
    echo "⚠️ Local branch is $behind commits behind remote"
    echo "💡 Run: git pull before deployment"
fi

if [ "$ahead" -gt 0 ]; then
    echo "✅ Local branch is $ahead commits ahead of remote"
fi
```

#### Build and Test Validation:
```bash
echo "=== Build and Test Validation ==="

# 1. Clean build
echo "🏗️ Performing clean build..."

if [ -f "package.json" ]; then
    echo "📦 Node.js project detected"
    
    # Clean previous builds
    rm -rf dist/ build/ node_modules/.cache/
    
    # Install dependencies
    if [ -f "package-lock.json" ]; then
        echo "🔧 Installing npm dependencies..."
        npm ci --silent || echo "⚠️ npm ci failed"
    elif [ -f "yarn.lock" ]; then
        echo "🔧 Installing yarn dependencies..."
        yarn install --frozen-lockfile --silent || echo "⚠️ yarn install failed"
    else
        npm install --silent || echo "⚠️ npm install failed"
    fi
    
    # Run build
    if npm run build --silent 2>/dev/null; then
        echo "✅ Build successful"
    else
        echo "❌ Build failed - aborting deployment"
        return 1
    fi
fi

if [ -f "pyproject.toml" ]; then
    echo "🐍 Python project detected"
    
    # Install dependencies with UV
    if command -v uv >/dev/null 2>&1; then
        echo "🔧 Installing Python dependencies with UV..."
        uv sync || echo "⚠️ uv sync failed"
    else
        echo "⚠️ UV not found, using pip"
        pip install -e . || echo "⚠️ pip install failed"
    fi
fi

# 2. Run tests
echo "🧪 Running test suite..."

test_passed=true

if [ -f "package.json" ]; then
    if npm test --silent 2>/dev/null; then
        echo "✅ JavaScript tests passed"
    else
        echo "❌ JavaScript tests failed"
        test_passed=false
    fi
fi

if [ -f "pyproject.toml" ]; then
    if python -m pytest -q 2>/dev/null; then
        echo "✅ Python tests passed"
    else
        echo "❌ Python tests failed"
        test_passed=false
    fi
fi

if [ "$test_passed" = false ]; then
    echo "❌ Tests failed - aborting deployment"
    return 1
fi

# 3. Security audit
echo "🔒 Running security audit..."

if [ -f "package.json" ] && command -v npm >/dev/null 2>&1; then
    npm audit --audit-level=high --silent || echo "⚠️ npm audit found issues"
fi

if [ -f "pyproject.toml" ] && command -v safety >/dev/null 2>&1; then
    safety check --silent || echo "⚠️ Python safety check found issues"
fi
```

### Phase 2: Environment-Specific Deployment

#### Deployment Target Detection:
```bash
echo "=== Deployment Target Detection ==="

# Detect deployment environment
deploy_env="development"

if [[ "$current_branch" == "production" ]] || [[ "$current_branch" == "main" ]]; then
    deploy_env="production"
elif [[ "$current_branch" == "staging" ]] || [[ "$current_branch" == "release"* ]]; then
    deploy_env="staging"
fi

echo "🎯 Deployment environment: $deploy_env"

# Load environment-specific configuration
env_file=".env.${deploy_env}"
if [ -f "$env_file" ]; then
    echo "✅ Environment file found: $env_file"
    source "$env_file"
else
    echo "⚠️ No environment file found: $env_file"
    if [ -f ".env" ]; then
        echo "📋 Using default .env file"
        source ".env"
    fi
fi
```

#### MCP Server Deployment:
```bash
echo "=== MCP Server Deployment ==="

# Deploy individual MCP servers
deploy_mcp_servers() {
    local servers_dir="server"
    
    if [ -d "$servers_dir" ]; then
        echo "🖥️ Deploying MCP servers..."
        
        for server_dir in "$servers_dir"/*; do
            if [ -d "$server_dir" ]; then
                server_name=$(basename "$server_dir")
                echo "📡 Deploying MCP server: $server_name"
                
                cd "$server_dir" || continue
                
                # Install dependencies
                if [ -f "pyproject.toml" ]; then
                    echo "  🔧 Installing Python dependencies..."
                    uv sync --quiet || echo "  ⚠️ Dependency installation failed"
                    
                    # Test server startup
                    echo "  🧪 Testing server startup..."
                    timeout 10s uv run python "$(ls *.py | head -1)" --help >/dev/null 2>&1 && \
                        echo "  ✅ Server startup test passed" || \
                        echo "  ⚠️ Server startup test failed"
                fi
                
                cd - >/dev/null
            fi
        done
    else
        echo "⚠️ No server directory found"
    fi
}

deploy_mcp_servers
```

#### Application Deployment:
```bash
echo "=== Application Deployment ==="

# Deploy based on deployment method
deploy_application() {
    # Docker deployment
    if [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ]; then
        echo "🐳 Docker deployment detected"
        
        if [ -f "docker-compose.yml" ]; then
            echo "🔧 Building and deploying with Docker Compose..."
            
            # Build images
            docker-compose build || echo "⚠️ Docker build failed"
            
            # Deploy with zero-downtime strategy
            docker-compose up -d --remove-orphans || echo "⚠️ Docker deployment failed"
            
            # Health check
            echo "🏥 Performing health check..."
            sleep 10
            docker-compose ps | grep -q "Up" && echo "✅ Containers are running" || echo "❌ Container health check failed"
            
        elif [ -f "Dockerfile" ]; then
            echo "🔧 Building Docker image..."
            
            image_name=$(basename $(pwd)):latest
            docker build -t "$image_name" . || echo "⚠️ Docker build failed"
            
            # Run container
            docker run -d --name "$(basename $(pwd))-${deploy_env}" "$image_name" || echo "⚠️ Container start failed"
        fi
    
    # Direct deployment
    else
        echo "📦 Direct deployment"
        
        # Create deployment directory
        deploy_dir="/opt/$(basename $(pwd))"
        backup_dir="/opt/$(basename $(pwd)).backup.$(date +%Y%m%d_%H%M%S)"
        
        echo "🎯 Deployment directory: $deploy_dir"
        
        # Backup existing deployment
        if [ -d "$deploy_dir" ]; then
            echo "💾 Creating backup: $backup_dir"
            sudo cp -r "$deploy_dir" "$backup_dir" || echo "⚠️ Backup failed"
        fi
        
        # Copy files
        echo "📂 Copying application files..."
        sudo mkdir -p "$deploy_dir"
        
        # Copy source files (excluding development files)
        rsync -av --exclude='node_modules' --exclude='__pycache__' --exclude='.git' \
              --exclude='*.log' --exclude='.env' --exclude='dist' \
              . "$deploy_dir/" || echo "⚠️ File copy failed"
        
        # Set permissions
        sudo chown -R $(whoami):$(whoami) "$deploy_dir"
        sudo chmod -R 755 "$deploy_dir"
    fi
}

deploy_application
```

### Phase 3: Service Management and Health Checks

#### Service Management:
```bash
echo "=== Service Management ==="

# Restart services based on deployment type
restart_services() {
    echo "🔄 Managing services..."
    
    # Check for systemd services
    service_name="$(basename $(pwd))"
    
    if systemctl list-units --type=service | grep -q "$service_name"; then
        echo "🔧 Restarting systemd service: $service_name"
        sudo systemctl restart "$service_name" || echo "⚠️ Service restart failed"
        sudo systemctl enable "$service_name" || echo "⚠️ Service enable failed"
        
        # Check service status
        if systemctl is-active --quiet "$service_name"; then
            echo "✅ Service is active: $service_name"
        else
            echo "❌ Service failed to start: $service_name"
            systemctl status "$service_name" --lines=5
        fi
    
    # Check for PM2 processes (Node.js)
    elif command -v pm2 >/dev/null 2>&1 && [ -f "package.json" ]; then
        echo "🔧 Managing PM2 process..."
        
        if pm2 list | grep -q "$service_name"; then
            pm2 restart "$service_name" || echo "⚠️ PM2 restart failed"
        else
            pm2 start npm --name "$service_name" -- start || echo "⚠️ PM2 start failed"
        fi
        
        pm2 save || echo "⚠️ PM2 save failed"
    
    # Manual process management
    else
        echo "📋 Manual service management required"
        echo "💡 Consider setting up systemd service or PM2 for process management"
    fi
}

restart_services
```

#### Health Checks:
```bash
echo "=== Health Checks ==="

# Comprehensive health validation
perform_health_checks() {
    echo "🏥 Performing comprehensive health checks..."
    
    # 1. Process checks
    echo "🔍 Checking processes..."
    if pgrep -f "$(basename $(pwd))" >/dev/null; then
        echo "✅ Application processes are running"
    else
        echo "⚠️ No application processes found"
    fi
    
    # 2. Port checks
    echo "🔍 Checking ports..."
    common_ports="3000 8000 8080 5000"
    for port in $common_ports; do
        if netstat -tuln | grep -q ":$port "; then
            echo "✅ Port $port is listening"
        fi
    done
    
    # 3. HTTP health checks
    echo "🔍 Checking HTTP endpoints..."
    health_urls="http://localhost:3000/health http://localhost:8000/health"
    for url in $health_urls; do
        if curl -s -f "$url" >/dev/null 2>&1; then
            echo "✅ Health check passed: $url"
        else
            echo "⚠️ Health check failed: $url"
        fi
    done
    
    # 4. MCP server checks
    echo "🔍 Checking MCP servers..."
    if command -v claude >/dev/null 2>&1; then
        claude mcp list 2>/dev/null | grep -E "(trading|filesystem|weather)" && \
            echo "✅ MCP servers registered" || \
            echo "⚠️ MCP servers not found"
    fi
    
    # 5. Log checks
    echo "🔍 Checking logs for errors..."
    if [ -d "logs" ]; then
        recent_errors=$(find logs -name "*.log" -mtime -1 -exec grep -l "ERROR\|CRITICAL" {} \; 2>/dev/null | wc -l)
        if [ "$recent_errors" -gt 0 ]; then
            echo "⚠️ Found $recent_errors log files with recent errors"
        else
            echo "✅ No recent errors in logs"
        fi
    fi
    
    # 6. Resource checks
    echo "🔍 Checking system resources..."
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    memory_usage=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
    
    echo "📊 CPU usage: ${cpu_usage}%"
    echo "📊 Memory usage: ${memory_usage}%"
    
    # Resource warnings
    if [ "${cpu_usage%.*}" -gt 80 ]; then
        echo "⚠️ High CPU usage detected"
    fi
    
    if [ "${memory_usage%.*}" -gt 80 ]; then
        echo "⚠️ High memory usage detected"
    fi
}

perform_health_checks
```

### Phase 4: Rollback Capabilities

#### Rollback Strategy:
```bash
echo "=== Rollback Capabilities ==="

# Create rollback function
create_rollback_script() {
    local rollback_script="rollback_$(date +%Y%m%d_%H%M%S).sh"
    
    cat > "$rollback_script" << 'EOF'
#!/bin/bash
# Automatic rollback script generated during deployment

echo "🔄 Starting rollback process..."

# Rollback git commit
CURRENT_COMMIT=$(git rev-parse HEAD)
PREVIOUS_COMMIT=$(git rev-parse HEAD~1)

echo "📍 Rolling back from $CURRENT_COMMIT to $PREVIOUS_COMMIT"
git checkout "$PREVIOUS_COMMIT"

# Rollback services
if systemctl list-units --type=service | grep -q "$(basename $(pwd))"; then
    echo "🔧 Restarting service after rollback..."
    sudo systemctl restart "$(basename $(pwd))"
fi

# Rollback Docker containers
if [ -f "docker-compose.yml" ]; then
    echo "🐳 Rolling back Docker deployment..."
    docker-compose down
    git checkout "$PREVIOUS_COMMIT"
    docker-compose up -d
fi

echo "✅ Rollback completed"
echo "💡 Run health checks to verify rollback success"
EOF

    chmod +x "$rollback_script"
    echo "📋 Rollback script created: $rollback_script"
    echo "💡 To rollback this deployment, run: ./$rollback_script"
}

create_rollback_script
```

### Phase 5: Post-Deployment Tasks

#### Monitoring and Alerts:
```bash
echo "=== Post-Deployment Tasks ==="

# Set up monitoring
setup_monitoring() {
    echo "📊 Setting up post-deployment monitoring..."
    
    # Create deployment record
    deployment_log="deployments.log"
    echo "$(date): Deployed $(git rev-parse --short HEAD) to $deploy_env by $(whoami)" >> "$deployment_log"
    
    # Set up log rotation if not exists
    if [ ! -f "/etc/logrotate.d/$(basename $(pwd))" ]; then
        echo "🔄 Setting up log rotation..."
        sudo tee "/etc/logrotate.d/$(basename $(pwd))" > /dev/null << EOF
/opt/$(basename $(pwd))/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    notifempty
    create 644 $(whoami) $(whoami)
}
EOF
    fi
    
    # Schedule health checks
    cron_job="*/5 * * * * /opt/$(basename $(pwd))/health_check.sh"
    if ! crontab -l 2>/dev/null | grep -q "health_check.sh"; then
        echo "⏰ Setting up health check cron job..."
        (crontab -l 2>/dev/null; echo "$cron_job") | crontab -
    fi
}

setup_monitoring
```

#### Documentation Updates:
```bash
echo "=== Documentation Updates ==="

# Update deployment documentation
update_deployment_docs() {
    echo "📝 Updating deployment documentation..."
    
    # Create deployment summary
    cat > "DEPLOYMENT_SUMMARY.md" << EOF
# Deployment Summary

**Date:** $(date)
**Environment:** $deploy_env
**Branch:** $current_branch
**Commit:** $(git rev-parse --short HEAD)
**Deployed by:** $(whoami)

## Services Deployed
- MCP Servers: $(ls server/ 2>/dev/null | tr '\n' ', ' | sed 's/,$//')
- Application: $(basename $(pwd))

## Health Status
$(curl -s http://localhost:3000/health 2>/dev/null | head -1 || echo "Health endpoint not available")

## Rollback Instructions
To rollback this deployment:
\`\`\`bash
./rollback_$(date +%Y%m%d_%H%M%S).sh
\`\`\`

## Monitoring
- Logs: /opt/$(basename $(pwd))/logs/
- Health checks: Every 5 minutes via cron
- Service status: systemctl status $(basename $(pwd))
EOF

    echo "✅ Deployment summary created: DEPLOYMENT_SUMMARY.md"
}

update_deployment_docs
```

## Deployment Strategies

### Blue-Green Deployment:
```bash
# Blue-Green deployment for zero downtime
blue_green_deploy() {
    echo "🔵🟢 Executing Blue-Green deployment..."
    
    # Determine current environment
    if docker ps | grep -q "blue"; then
        current_env="blue"
        new_env="green"
    else
        current_env="green"
        new_env="blue"
    fi
    
    echo "📍 Current environment: $current_env"
    echo "🎯 Deploying to: $new_env"
    
    # Deploy to new environment
    docker-compose -f "docker-compose.$new_env.yml" up -d
    
    # Health check new environment
    sleep 30
    if curl -s -f "http://localhost:8081/health" >/dev/null; then
        echo "✅ New environment health check passed"
        
        # Switch traffic
        echo "🔄 Switching traffic to $new_env"
        # Update load balancer configuration here
        
        # Stop old environment
        docker-compose -f "docker-compose.$current_env.yml" down
        echo "✅ Blue-Green deployment completed"
    else
        echo "❌ New environment health check failed"
        docker-compose -f "docker-compose.$new_env.yml" down
        return 1
    fi
}
```

### Canary Deployment:
```bash
# Canary deployment for gradual rollout
canary_deploy() {
    echo "🐤 Executing Canary deployment..."
    
    # Deploy canary version (10% traffic)
    echo "📡 Deploying canary version..."
    docker-compose -f "docker-compose.canary.yml" up -d
    
    # Monitor canary metrics
    echo "📊 Monitoring canary metrics for 5 minutes..."
    sleep 300
    
    # Check error rates
    error_rate=$(curl -s "http://localhost:8080/metrics" | grep error_rate | awk '{print $2}')
    
    if [ "${error_rate%.*}" -lt 5 ]; then
        echo "✅ Canary metrics look good, proceeding with full deployment"
        docker-compose up -d --scale app=3
        docker-compose -f "docker-compose.canary.yml" down
        echo "✅ Canary deployment completed"
    else
        echo "❌ Canary metrics show issues, rolling back"
        docker-compose -f "docker-compose.canary.yml" down
        return 1
    fi
}
```

## Success Criteria

### Deployment Validation:
- ✅ **Pre-deployment Checks**: All validation passed (git, build, tests, security)
- ✅ **Clean Build**: Application built successfully without errors
- ✅ **Environment Setup**: Correct environment configuration loaded
- ✅ **Service Deployment**: All services deployed and running
- ✅ **Health Checks**: All health endpoints responding correctly
- ✅ **Rollback Capability**: Rollback script created and tested

### Quality Standards:
- ✅ **Zero Downtime**: Deployment completed without service interruption
- ✅ **Performance**: No performance degradation after deployment
- ✅ **Security**: No security vulnerabilities introduced
- ✅ **Monitoring**: Logging and monitoring properly configured
- ✅ **Documentation**: Deployment documented and rollback instructions provided
- ✅ **Automation**: Process repeatable and automated where possible

## Post-Deployment Verification

### Final Checklist:
- [ ] All services running and healthy
- [ ] Health checks passing
- [ ] Logs show no critical errors
- [ ] Performance metrics within acceptable ranges
- [ ] Rollback script tested and available
- [ ] Monitoring and alerts configured
- [ ] Documentation updated
- [ ] Team notified of successful deployment
