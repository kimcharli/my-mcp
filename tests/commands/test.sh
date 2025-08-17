#!/bin/bash
# Quick test runner script for Claude Code Commands

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Claude Code Commands Test Suite${NC}"
echo "=================================="

# Check if we're in the right directory
if [[ ! -d ".claude/commands" ]]; then
    echo -e "${RED}❌ Error: .claude/commands directory not found${NC}"
    echo -e "${YELLOW}💡 Run this script from the project root directory${NC}"
    exit 1
fi

# Check Python dependencies
echo -e "${BLUE}📦 Checking Python dependencies...${NC}"
if ! python3 -c "import yaml" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installing PyYAML...${NC}"
    pip3 install PyYAML
fi

# Create reports directory
mkdir -p tests/commands/reports

# Navigate to test directory
cd tests/commands

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo -e "${BLUE}🚀 Running tests...${NC}"
echo ""

# Run the test suite
if python3 run_tests.py "$@"; then
    echo ""
    echo -e "${GREEN}✅ All tests completed successfully!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed${NC}"
    echo -e "${YELLOW}📋 Check the reports in tests/commands/reports/${NC}"
    exit 1
fi