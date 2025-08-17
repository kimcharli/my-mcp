#!/usr/bin/env python3
"""
Comprehensive test runner for MCP server collection.
Runs tests for all servers and generates coverage reports.
"""
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple


def run_command(cmd: List[str], cwd: str = None) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 5 minutes"
    except Exception as e:
        return 1, "", str(e)


def detect_server_type(server_path: Path) -> str:
    """Detect the server type and testing framework."""
    if (server_path / "pyproject.toml").exists():
        return "python"
    elif (server_path / "package.json").exists():
        return "javascript"
    elif (server_path / "Cargo.toml").exists():
        return "rust"
    elif (server_path / "pom.xml").exists() or (server_path / "build.gradle").exists():
        return "java"
    else:
        return "unknown"


def _parse_pytest_output(output: str) -> Tuple[int, int, int]:
    """Parse pytest output to extract test counts and coverage."""
    passed = 0
    failed = 0
    coverage = 0
    lines = output.split('\n')
    for line in lines:
        if " passed" in line and "failed" in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if part == "passed":
                    passed = int(parts[i-1])
                elif part == "failed":
                    failed = int(parts[i-1])
        elif " passed" in line and "failed" not in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if part == "passed":
                    passed = int(parts[i-1])
    for line in lines:
        if "TOTAL" in line and "%" in line:
            parts = line.split()
            for part in parts:
                if part.endswith("%"):
                    try:
                        coverage = int(part.replace("%", ""))
                    except ValueError:
                        pass
    return passed, failed, coverage

def _run_test_commands(commands: List[List[str]], cwd: str) -> Tuple[int, str, str]:
    """Run a series of test commands until one succeeds."""
    for cmd in commands:
        print(f"  Running: {" ".join(cmd)}")
        exit_code, stdout, stderr = run_command(cmd, cwd)
        if exit_code == 0:
            return exit_code, stdout, stderr
    return 1, "", "All test commands failed."

def run_python_tests(server_path: Path, server_name: str) -> Dict:
    """Run tests for a Python-based MCP server."""
    print(f"\n🧪 Testing {server_name} (Python)...")
    
    # Change to server directory
    os.chdir(server_path)
    
    results = {
        "server": server_name,
        "type": "python",
        "tests_found": False,
        "tests_passed": 0,
        "tests_failed": 0,
        "coverage": 0,
        "errors": []
    }
    
    # Check if tests directory exists
    tests_dir = server_path / "tests"
    if not tests_dir.exists():
        results["errors"].append("No tests directory found")
        return results
    
    # Check for test files
    test_files = list(tests_dir.glob("test_*.py"))
    if not test_files:
        results["errors"].append("No test files found")
        return results
    
    results["tests_found"] = True
    
    # Try running tests with uv first, then fallback to pytest
    test_commands = [
        ["uv", "run", "pytest", "tests/", "-v", "--cov=.", "--cov-report=term"],
        ["python", "-m", "pytest", "tests/", "-v"],
        ["pytest", "tests/", "-v"]
    ]
    
    exit_code, stdout, stderr = _run_test_commands(test_commands, str(server_path))
    
    if exit_code == 0:
        passed, failed, coverage = _parse_pytest_output(stdout)
        results["tests_passed"] = passed
        results["tests_failed"] = failed
        results["coverage"] = coverage
    else:
        results["errors"].append("All test commands failed.")
        if stderr:
            results["errors"].append(f"Error: {stderr[:500]}")
    
    return results



def run_integration_tests() -> Dict:
    """Run integration tests."""
    print(f"\n🔗 Running integration tests...")
    
    results = {
        "server": "integration",
        "type": "integration",
        "tests_found": False,
        "tests_passed": 0,
        "tests_failed": 0,
        "coverage": 0,
        "errors": []
    }
    
    # Check if integration tests exist
    integration_test_file = Path("tests/test_mcp_integration.py")
    if not integration_test_file.exists():
        results["errors"].append("Integration test file not found")
        return results
    
    results["tests_found"] = True
    
    # Run integration tests
    cmd = ["python", "-m", "pytest", "tests/test_mcp_integration.py", "-v"]
    exit_code, stdout, stderr = run_command(cmd)
    
    if exit_code == 0:
        # Parse output for test counts
        lines = stdout.split('\n')
        for line in lines:
            if " passed" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed":
                        results["tests_passed"] = int(parts[i-1])
                        break
    else:
        results["errors"].append(f"Integration tests failed: {stderr[:500]}")
    
    return results


def generate_report(all_results: List[Dict]) -> str:
    """Generate a comprehensive test report."""
    report = []
    report.append("=" * 80)
    report.append("🧪 MCP SERVER COLLECTION - TEST RESULTS SUMMARY")
    report.append("=" * 80)
    
    total_servers = 0
    total_tests_passed = 0
    total_tests_failed = 0
    servers_with_tests = 0
    
    for result in all_results:
        total_servers += 1
        total_tests_passed += result["tests_passed"]
        total_tests_failed += result["tests_failed"]
        
        if result["tests_found"]:
            servers_with_tests += 1
        
        # Server summary
        status = "✅ PASS" if result["tests_passed"] > 0 and result["tests_failed"] == 0 else "❌ FAIL"
        if not result["tests_found"]:
            status = "⚠️  NO TESTS"
        
        report.append(f"\n📦 {result['server'].upper()} ({result['type']})")
        report.append(f"   Status: {status}")
        
        if result["tests_found"]:
            report.append(f"   Tests Passed: {result['tests_passed']}")
            report.append(f"   Tests Failed: {result['tests_failed']}")
            if result["coverage"] > 0:
                report.append(f"   Coverage: {result['coverage']}%")
        
        if result["errors"]:
            report.append(f"   Errors: {len(result['errors'])}")
            for error in result["errors"][:3]:  # Show first 3 errors
                report.append(f"     - {error}")
    
    # Overall summary
    report.append("\n" + "=" * 80)
    report.append("📊 OVERALL SUMMARY")
    report.append("=" * 80)
    report.append(f"Total Servers: {total_servers}")
    report.append(f"Servers with Tests: {servers_with_tests}")
    report.append(f"Total Tests Passed: {total_tests_passed}")
    report.append(f"Total Tests Failed: {total_tests_failed}")
    
    if total_tests_passed + total_tests_failed > 0:
        success_rate = (total_tests_passed / (total_tests_passed + total_tests_failed)) * 100
        report.append(f"Success Rate: {success_rate:.1f}%")
    
    # Recommendations
    report.append("\n📝 RECOMMENDATIONS")
    report.append("-" * 40)
    
    missing_tests = total_servers - servers_with_tests
    if missing_tests > 0:
        report.append(f"• Add tests for {missing_tests} servers without test coverage")
    
    if total_tests_failed > 0:
        report.append(f"• Fix {total_tests_failed} failing tests")
    
    avg_coverage = sum(r["coverage"] for r in all_results if r["coverage"] > 0) / max(1, len([r for r in all_results if r["coverage"] > 0]))
    if avg_coverage < 80:
        report.append(f"• Improve code coverage (current avg: {avg_coverage:.1f}%, target: 80%)")
    
    report.append("• Add integration tests for cross-server workflows")
    report.append("• Implement performance tests for response times")
    
    return "\n".join(report)


def main():
    """Main test runner function."""
    print("🚀 Starting MCP Server Collection Test Suite")
    print("=" * 60)
    
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    all_results = []
    
    # Test individual servers
    server_dirs = [
        "server/trading",
        "server/filesystem", 
        "server/weather",
        "add-demo"
    ]
    
    for server_dir in server_dirs:
        server_path = Path(server_dir)
        if server_path.exists():
            server_name = server_path.name
            server_type = detect_server_type(server_path)
            
            if server_type == "python":
                result = run_python_tests(server_path, server_name)
                all_results.append(result)
            else:
                # Placeholder for other server types
                result = {
                    "server": server_name,
                    "type": server_type,
                    "tests_found": False,
                    "tests_passed": 0,
                    "tests_failed": 0,
                    "coverage": 0,
                    "errors": [f"Testing not implemented for {server_type}"]
                }
                all_results.append(result)
    
    # Run integration tests
    os.chdir(project_root)
    integration_result = run_integration_tests()
    all_results.append(integration_result)
    
    # Generate and display report
    report = generate_report(all_results)
    print("\n" + report)
    
    # Save results to JSON file
    with open("test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    # Return appropriate exit code
    total_failed = sum(r["tests_failed"] for r in all_results)
    servers_without_tests = len([r for r in all_results if not r["tests_found"]])
    
    if total_failed > 0 or servers_without_tests > 2:  # Allow some servers without tests
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()