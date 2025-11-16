#!/bin/bash
# Frontend Debug Script - Systematic debugging for React/TypeScript issues
# Part of the frontend-debugger agent system

set -e

echo "🚀 Frontend Debug Workflow - Tauri + React + TypeScript"
echo "======================================================"

# Configuration
PROJECT_DIR="${PWD}"
DEV_SERVER_URL="http://localhost:1420"
DEV_SERVER_PORT="1420"
TYPESCRIPT_LOG="typescript-errors.log"
DEBUG_LOG="frontend-debug.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1" | tee -a "$DEBUG_LOG"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$DEBUG_LOG"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$DEBUG_LOG"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$DEBUG_LOG"
}

# Phase 1: TypeScript Compilation Check (CRITICAL FIRST STEP)
phase1_typescript_check() {
    log "🔍 Phase 1: TypeScript Compilation Validation (CRITICAL)"
    echo "TypeScript compilation errors prevent bundle creation and cause blank pages"
    echo "----------------------------------------------------------------------"
    
    if npm run lint 2>&1 | tee "$TYPESCRIPT_LOG"; then
        success "TypeScript compilation passed ✅"
        return 0
    else
        error "TypeScript compilation failed ❌ - MUST FIX BEFORE PROCEEDING"
        echo ""
        echo "Common TypeScript fixes needed:"
        echo "1. Remove unused imports/variables (TS6133 errors)"
        echo "2. Fix type mismatches (TS2339, TS2322 errors)" 
        echo "3. Add missing properties to interfaces"
        echo "4. Fix import/export issues"
        echo ""
        echo "Run this script with --fix-typescript to auto-fix common issues"
        return 1
    fi
}

# Phase 2: Development Server Health Check
phase2_dev_server_check() {
    log "🔍 Phase 2: Development Server Health Check"
    echo "Checking if Tauri development server is running and responding"
    echo "-------------------------------------------------------------"
    
    # Check if server is running
    if ! pgrep -f "tauri dev" > /dev/null; then
        warning "Tauri dev server not running"
        echo "To start: npm run tauri:dev"
        return 1
    fi
    
    # Wait a moment for server startup
    sleep 2
    
    # Check server response
    HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$DEV_SERVER_URL" || echo "000")
    
    if [ "$HTTP_RESPONSE" = "200" ]; then
        success "Development server responding (HTTP $HTTP_RESPONSE) ✅"
        
        # Check if HTML contains React root div
        HTML_CONTENT=$(curl -s "$DEV_SERVER_URL")
        if echo "$HTML_CONTENT" | grep -q '<div id="root"'; then
            success "React root div found ✅"
        else
            warning "React root div not found in HTML"
        fi
        
        return 0
    else
        error "Development server issue (HTTP $HTTP_RESPONSE) ❌"
        echo "Check if server is fully started: ps aux | grep tauri"
        return 1
    fi
}

# Phase 3: Browser Console Check
phase3_browser_check() {
    log "🔍 Phase 3: Browser Console Verification"
    echo "Manual step: Check browser console for JavaScript errors"
    echo "--------------------------------------------------------"
    
    echo "Instructions:"
    echo "1. Open browser and navigate to: $DEV_SERVER_URL"
    echo "2. Open DevTools (F12 or Cmd+Opt+I)"
    echo "3. Check Console tab for:"
    echo "   - Red error messages"
    echo "   - Failed network requests"
    echo "   - JavaScript runtime errors"
    echo "4. Check Elements tab:"
    echo "   - Verify <div id='root'> exists"
    echo "   - Check if React components are in DOM"
    echo ""
    echo "Press Enter after checking browser console..."
    read -r
}

# Phase 4: Component Isolation Test
phase4_component_test() {
    log "🔍 Phase 4: Component Isolation Testing"
    echo "Creating minimal test component to isolate rendering issues"
    echo "----------------------------------------------------------"
    
    # Backup original App.tsx
    if [ -f "src/App.tsx" ] && [ ! -f "src/App.tsx.backup" ]; then
        cp "src/App.tsx" "src/App.tsx.backup"
        log "Backed up original App.tsx"
    fi
    
    # Create minimal test component
    cat > "src/MinimalTest.tsx" << 'EOF'
import React from 'react';

const MinimalTestComponent = () => {
  console.log('MinimalTestComponent rendered successfully');
  
  return (
    <div style={{ 
      padding: '40px', 
      backgroundColor: '#f0f8ff',
      fontFamily: 'Arial, sans-serif',
      textAlign: 'center'
    }}>
      <h1 style={{ color: '#2c3e50' }}>✅ React Rendering Test</h1>
      <p>If you see this message, React is working correctly!</p>
      <p style={{ fontSize: '14px', color: '#7f8c8d' }}>
        Timestamp: {new Date().toLocaleString()}
      </p>
    </div>
  );
};

export default MinimalTestComponent;
EOF
    
    success "Created MinimalTest.tsx component"
    echo "Next steps:"
    echo "1. Temporarily replace App component with MinimalTestComponent"
    echo "2. Check if browser shows the test component"
    echo "3. If working, gradually add complexity back"
    echo "4. If not working, the issue is deeper than component logic"
}

# Auto-fix common TypeScript issues
fix_typescript_issues() {
    log "🔧 Auto-fixing common TypeScript issues"
    echo "Attempting to fix unused imports and variables"
    echo "----------------------------------------------"
    
    # Find files with TS6133 errors (unused variables/imports)
    if [ -f "$TYPESCRIPT_LOG" ]; then
        grep "error TS6133" "$TYPESCRIPT_LOG" | while read -r line; do
            # Extract filename and variable name
            FILE=$(echo "$line" | cut -d'(' -f1)
            VARIABLE=$(echo "$line" | grep -o "'[^']*'" | head -1 | tr -d "'")
            
            if [ -f "$FILE" ]; then
                log "Attempting to remove unused variable '$VARIABLE' from $FILE"
                
                # Remove unused imports
                if echo "$line" | grep -q "is declared but its value is never read"; then
                    # Create a backup
                    cp "$FILE" "${FILE}.backup"
                    
                    # Try to remove the unused import/variable (basic pattern)
                    # This is a simple approach - more complex cases may need manual fix
                    if grep -q "import.*$VARIABLE" "$FILE"; then
                        log "Removing unused import: $VARIABLE"
                        sed -i.tmp "/import.*$VARIABLE.*from/d" "$FILE"
                    fi
                fi
            fi
        done
    else
        warning "No TypeScript error log found. Run phase 1 first."
    fi
}

# Progressive complexity test
progressive_test() {
    log "🔍 Progressive Complexity Testing"
    echo "Testing components with increasing complexity"
    echo "--------------------------------------------"
    
    cat > "src/ProgressiveTest.tsx" << 'EOF'
import React, { useState } from 'react';

const ProgressiveTestComponent = () => {
  const [step, setStep] = useState(1);
  const [log, setLog] = useState<string[]>(['Progressive test started']);
  
  const addLog = (message: string) => {
    setLog(prev => [...prev, `Step ${step}: ${message}`]);
  };
  
  const renderByStep = () => {
    switch(step) {
      case 1:
        addLog('Basic render working');
        return <div style={{color: 'green'}}>✅ Step 1: Basic Render Working</div>;
        
      case 2:
        addLog('State management working');
        return <div style={{color: 'blue'}}>✅ Step 2: State Management Working</div>;
        
      case 3:
        return (
          <div>
            <div style={{color: 'orange'}}>⚠️ Step 3: Testing Service Integration</div>
            <p>This step would test your services (comment out for now)</p>
          </div>
        );
        
      case 4:
        return (
          <div>
            <div style={{color: 'purple'}}>⚠️ Step 4: Testing Complex Components</div>
            <p>This step would test your full application components</p>
          </div>
        );
        
      default:
        return (
          <div style={{color: 'red'}}>
            🎉 All Steps Completed - React is Working!
            <p>You can now restore your original App component</p>
          </div>
        );
    }
  };
  
  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h2>Progressive Complexity Test</h2>
      <div style={{ margin: '20px 0' }}>
        {renderByStep()}
      </div>
      
      <div style={{ margin: '20px 0' }}>
        <button 
          onClick={() => setStep(step + 1)}
          style={{ 
            padding: '10px 20px', 
            marginRight: '10px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px'
          }}
        >
          Next Step ({step + 1})
        </button>
        
        <button 
          onClick={() => setStep(1)}
          style={{ 
            padding: '10px 20px',
            backgroundColor: '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '4px'
          }}
        >
          Reset
        </button>
      </div>
      
      <div style={{ 
        marginTop: '20px', 
        padding: '10px', 
        backgroundColor: '#f8f9fa',
        border: '1px solid #dee2e6',
        borderRadius: '4px',
        maxHeight: '200px',
        overflowY: 'auto'
      }}>
        <h4>Test Log:</h4>
        {log.map((entry, i) => (
          <div key={i} style={{ fontSize: '12px', margin: '2px 0' }}>
            {entry}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProgressiveTestComponent;
EOF
    
    success "Created ProgressiveTest.tsx component"
}

# Emergency recovery
emergency_recovery() {
    log "🚨 Emergency Recovery Sequence"
    echo "Attempting to restore working state"
    echo "----------------------------------"
    
    # Restore backups
    if [ -f "src/App.tsx.backup" ]; then
        mv "src/App.tsx.backup" "src/App.tsx"
        success "Restored original App.tsx"
    fi
    
    # Clean and reinstall
    log "Cleaning node_modules and package-lock.json"
    rm -rf node_modules package-lock.json
    
    log "Reinstalling dependencies"
    npm install
    
    log "Running TypeScript check"
    npm run lint
    
    success "Emergency recovery complete. Try: npm run tauri:dev"
}

# Generate debug report
generate_report() {
    log "📊 Generating Debug Report"
    echo "Collecting diagnostic information"
    echo "--------------------------------"
    
    REPORT_FILE="frontend-debug-report-$(date +%Y%m%d-%H%M%S).md"
    
    cat > "$REPORT_FILE" << EOF
# Frontend Debug Report

**Generated**: $(date)
**Project**: $(pwd)

## System Information
- Node.js: $(node --version 2>/dev/null || echo "Not found")
- npm: $(npm --version 2>/dev/null || echo "Not found")
- Tauri CLI: $(tauri --version 2>/dev/null || echo "Not found")

## TypeScript Compilation Status
\`\`\`
$(cat "$TYPESCRIPT_LOG" 2>/dev/null || echo "No TypeScript log available")
\`\`\`

## Development Server Status
- Server URL: $DEV_SERVER_URL
- Response Code: $(curl -s -o /dev/null -w "%{http_code}" "$DEV_SERVER_URL" 2>/dev/null || echo "Not accessible")

## Running Processes
\`\`\`
$(ps aux | grep -E "(tauri|node|npm)" | grep -v grep)
\`\`\`

## Project Structure
\`\`\`
$(find src -type f -name "*.tsx" -o -name "*.ts" | head -20)
\`\`\`

## Recommended Next Steps
1. Fix all TypeScript compilation errors first
2. Ensure development server is running and accessible
3. Test with minimal React component
4. Gradually add complexity back
5. Check browser console for runtime errors

---
*Generated by frontend-debugger agent*
EOF
    
    success "Debug report saved to: $REPORT_FILE"
}

# Main execution
main() {
    # Initialize log
    echo "Frontend Debug Session Started: $(date)" > "$DEBUG_LOG"
    
    case "${1:-full}" in
        "typescript"|"ts")
            phase1_typescript_check
            ;;
        "server")
            phase2_dev_server_check
            ;;
        "browser")
            phase3_browser_check
            ;;
        "test"|"component")
            phase4_component_test
            ;;
        "fix-typescript")
            fix_typescript_issues
            ;;
        "progressive")
            progressive_test
            ;;
        "recovery")
            emergency_recovery
            ;;
        "report")
            generate_report
            ;;
        "full")
            echo "🔍 Running Full Diagnostic Workflow"
            echo "==================================="
            phase1_typescript_check || {
                error "TypeScript compilation failed. Fix errors before continuing."
                echo "Run: $0 fix-typescript"
                exit 1
            }
            phase2_dev_server_check || {
                warning "Development server issues detected"
            }
            phase3_browser_check
            generate_report
            ;;
        "help")
            echo "Frontend Debug Script Usage:"
            echo "  $0 [command]"
            echo ""
            echo "Commands:"
            echo "  full            - Run complete diagnostic workflow (default)"
            echo "  typescript|ts   - Check TypeScript compilation only"
            echo "  server          - Check development server health"
            echo "  browser         - Guide through browser console check"
            echo "  test|component  - Create minimal test component"
            echo "  progressive     - Create progressive complexity test"
            echo "  fix-typescript  - Auto-fix common TypeScript issues"
            echo "  recovery        - Emergency recovery sequence"
            echo "  report          - Generate diagnostic report"
            echo "  help            - Show this help"
            echo ""
            echo "Examples:"
            echo "  $0 typescript    # Check compilation only"
            echo "  $0 fix-typescript # Auto-fix TS issues"
            echo "  $0 recovery      # Emergency recovery"
            ;;
        *)
            error "Unknown command: $1"
            echo "Run: $0 help"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"