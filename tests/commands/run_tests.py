#!/usr/bin/env python3
"""
Automated Test Runner for Claude Code Commands

This script runs all command tests and generates comprehensive reports.
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from test_framework import CommandTester, Severity
from test_specific_commands import TestSpecificCommands, TestCommandIntegration, TestCommandDocumentation


class TestRunner:
    """Automated test runner for Claude Code commands."""
    
    def __init__(self, commands_dir: Path = None, output_dir: Path = None):
        """Initialize test runner."""
        self.commands_dir = commands_dir or Path(".claude/commands")
        self.output_dir = output_dir or Path("tests/commands/reports")
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Test timestamp
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test suites and return comprehensive results."""
        print("🧪 Starting Claude Code Commands Test Suite")
        print("=" * 50)
        
        results = {
            "timestamp": self.timestamp,
            "summary": {},
            "framework_tests": {},
            "unit_tests": {},
            "integration_tests": {},
            "documentation_tests": {},
            "reports": []
        }
        
        # 1. Run framework validation tests
        print("\n📋 Running Framework Validation Tests...")
        framework_results = self._run_framework_tests()
        results["framework_tests"] = framework_results
        
        # 2. Run unittest suite
        print("\n🔧 Running Unit Tests...")
        unittest_results = self._run_unittest_suite()
        results["unit_tests"] = unittest_results
        
        # 3. Generate reports
        print("\n📊 Generating Reports...")
        report_files = self._generate_reports(framework_results, unittest_results)
        results["reports"] = report_files
        
        # 4. Print summary
        self._print_summary(results)
        
        return results
        
    def _run_framework_tests(self) -> Dict[str, Any]:
        """Run the main framework validation tests."""
        tester = CommandTester(self.commands_dir)
        test_results = tester.run_all_tests()
        
        # Categorize results
        framework_results = {
            "total_tests": len(test_results),
            "passed": len([r for r in test_results if r.status == "PASS"]),
            "failed": len([r for r in test_results if r.status == "FAIL"]),
            "skipped": len([r for r in test_results if r.status == "SKIP"]),
            "critical_issues": len([r for r in test_results if r.severity == Severity.CRITICAL]),
            "high_issues": len([r for r in test_results if r.severity == Severity.HIGH]),
            "medium_issues": len([r for r in test_results if r.severity == Severity.MEDIUM]),
            "low_issues": len([r for r in test_results if r.severity == Severity.LOW]),
            "results": test_results,
            "tester": tester
        }
        
        print(f"  ✅ Passed: {framework_results['passed']}")
        print(f"  ❌ Failed: {framework_results['failed']}")
        print(f"  ⏭️  Skipped: {framework_results['skipped']}")
        
        if framework_results['critical_issues'] > 0:
            print(f"  🔴 Critical Issues: {framework_results['critical_issues']}")
        if framework_results['high_issues'] > 0:
            print(f"  🟠 High Issues: {framework_results['high_issues']}")
            
        return framework_results
        
    def _run_unittest_suite(self) -> Dict[str, Any]:
        """Run the unittest test suite."""
        import unittest
        
        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # Add test classes
        suite.addTests(loader.loadTestsFromTestCase(TestSpecificCommands))
        suite.addTests(loader.loadTestsFromTestCase(TestCommandIntegration))
        suite.addTests(loader.loadTestsFromTestCase(TestCommandDocumentation))
        
        # Run tests with detailed output
        stream = unittest.StringIO()
        runner = unittest.TextTestRunner(stream=stream, verbosity=2)
        result = runner.run(suite)
        
        unittest_results = {
            "tests_run": result.testsRun,
            "failures": len(result.failures),
            "errors": len(result.errors),
            "skipped": len(result.skipped) if hasattr(result, 'skipped') else 0,
            "success_rate": (result.testsRun - len(result.failures) - len(result.errors)) / max(result.testsRun, 1) * 100,
            "output": stream.getvalue(),
            "failure_details": result.failures,
            "error_details": result.errors
        }
        
        print(f"  🧪 Tests Run: {unittest_results['tests_run']}")
        print(f"  ❌ Failures: {unittest_results['failures']}")
        print(f"  💥 Errors: {unittest_results['errors']}")
        print(f"  📊 Success Rate: {unittest_results['success_rate']:.1f}%")
        
        return unittest_results
        
    def _generate_reports(self, framework_results: Dict, unittest_results: Dict) -> List[str]:
        """Generate various report formats."""
        report_files = []
        
        # 1. Text Report
        text_report_path = self.output_dir / f"test_report_{self.timestamp}.txt"
        text_report = framework_results["tester"].generate_report("text")
        text_report += "\n\n" + "="*50 + "\n"
        text_report += "UNITTEST RESULTS\n"
        text_report += "="*50 + "\n"
        text_report += unittest_results["output"]
        
        text_report_path.write_text(text_report)
        report_files.append(str(text_report_path))
        
        # 2. JSON Report
        json_report_path = self.output_dir / f"test_report_{self.timestamp}.json"
        json_data = {
            "timestamp": self.timestamp,
            "framework_tests": {
                "summary": {k: v for k, v in framework_results.items() if k != "results" and k != "tester"},
                "results": [
                    {
                        "test_name": r.test_name,
                        "status": r.status,
                        "severity": r.severity.value,
                        "message": r.message,
                        "details": r.details,
                        "file_path": r.file_path
                    } for r in framework_results["results"]
                ]
            },
            "unittest_results": {k: v for k, v in unittest_results.items() if k not in ["output", "failure_details", "error_details"]}
        }
        
        json_report_path.write_text(json.dumps(json_data, indent=2))
        report_files.append(str(json_report_path))
        
        # 3. HTML Report
        html_report_path = self.output_dir / f"test_report_{self.timestamp}.html"
        html_report = framework_results["tester"].generate_report("html")
        
        # Enhance HTML with unittest results
        unittest_html = self._generate_unittest_html(unittest_results)
        html_report = html_report.replace("</body>", f"{unittest_html}</body>")
        
        html_report_path.write_text(html_report)
        report_files.append(str(html_report_path))
        
        # 4. Summary Report for CI/CD
        summary_report_path = self.output_dir / f"test_summary_{self.timestamp}.json"
        summary_data = {
            "timestamp": self.timestamp,
            "overall_status": "PASS" if (framework_results["failed"] == 0 and unittest_results["failures"] == 0 and unittest_results["errors"] == 0) else "FAIL",
            "framework_tests": {
                "passed": framework_results["passed"],
                "failed": framework_results["failed"],
                "critical_issues": framework_results["critical_issues"],
                "high_issues": framework_results["high_issues"]
            },
            "unit_tests": {
                "tests_run": unittest_results["tests_run"],
                "failures": unittest_results["failures"],
                "errors": unittest_results["errors"],
                "success_rate": unittest_results["success_rate"]
            }
        }
        
        summary_report_path.write_text(json.dumps(summary_data, indent=2))
        report_files.append(str(summary_report_path))
        
        return report_files
        
    def _generate_unittest_html(self, unittest_results: Dict) -> str:
        """Generate HTML section for unittest results."""
        return f"""
        <div class="unittest-results">
            <h2>Unit Test Results</h2>
            <div class="summary">
                <p>Tests Run: {unittest_results['tests_run']}</p>
                <p>Failures: {unittest_results['failures']}</p>
                <p>Errors: {unittest_results['errors']}</p>
                <p>Success Rate: {unittest_results['success_rate']:.1f}%</p>
            </div>
            <div class="unittest-details">
                <h3>Test Output</h3>
                <pre style="background: #f5f5f5; padding: 10px; border-radius: 5px;">
{unittest_results['output']}
                </pre>
            </div>
        </div>
        """
        
    def _print_summary(self, results: Dict[str, Any]):
        """Print test run summary."""
        print("\n" + "="*50)
        print("🎯 TEST SUMMARY")
        print("="*50)
        
        framework = results["framework_tests"]
        unittests = results["unit_tests"]
        
        total_issues = framework["critical_issues"] + framework["high_issues"] + unittests["failures"] + unittests["errors"]
        
        if total_issues == 0:
            print("✅ ALL TESTS PASSED!")
            status = "PASS"
        else:
            print("❌ TESTS FAILED - Issues Found")
            status = "FAIL"
            
        print(f"📊 Overall Status: {status}")
        print(f"🧪 Framework Tests: {framework['passed']}/{framework['total_tests']} passed")
        print(f"🔧 Unit Tests: {unittests['tests_run'] - unittests['failures'] - unittests['errors']}/{unittests['tests_run']} passed")
        
        if framework["critical_issues"] > 0:
            print(f"🔴 Critical Issues: {framework['critical_issues']}")
        if framework["high_issues"] > 0:
            print(f"🟠 High Priority Issues: {framework['high_issues']}")
            
        print(f"\n📋 Reports Generated:")
        for report_path in results["reports"]:
            print(f"  📄 {report_path}")
            
        return status == "PASS"


def main():
    """Main function for command line execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Claude Code Commands Test Suite")
    parser.add_argument("--commands-dir", type=Path, default=Path(".claude/commands"),
                       help="Path to commands directory")
    parser.add_argument("--output-dir", type=Path, default=Path("tests/commands/reports"),
                       help="Output directory for reports")
    parser.add_argument("--format", choices=["all", "text", "json", "html"], default="all",
                       help="Report format to generate")
    parser.add_argument("--ci", action="store_true",
                       help="CI mode - exit with non-zero status on failures")
                       
    args = parser.parse_args()
    
    # Create and run test runner
    runner = TestRunner(args.commands_dir, args.output_dir)
    results = runner.run_all_tests()
    
    # Exit with appropriate status for CI
    if args.ci:
        framework_failed = results["framework_tests"]["failed"] > 0
        unittest_failed = (results["unit_tests"]["failures"] + results["unit_tests"]["errors"]) > 0
        critical_issues = results["framework_tests"]["critical_issues"] > 0
        
        if framework_failed or unittest_failed or critical_issues:
            print("\n❌ Tests failed - exiting with error status")
            sys.exit(1)
        else:
            print("\n✅ All tests passed - exiting with success status")
            sys.exit(0)


if __name__ == "__main__":
    main()