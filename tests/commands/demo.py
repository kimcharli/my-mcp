#!/usr/bin/env python3
"""
Demo of the Claude Code Commands Testing Framework

This script demonstrates how to use the testing framework to validate commands.
"""

import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from test_framework import CommandTester


def demo_basic_usage():
    """Demonstrate basic testing framework usage."""
    print("🧪 Claude Code Commands Testing Framework Demo")
    print("=" * 50)
    
    # Initialize tester
    commands_dir = Path("../../.claude/commands")
    tester = CommandTester(commands_dir)
    
    print(f"📁 Testing commands in: {commands_dir}")
    print(f"📊 Commands found: {len(list(commands_dir.rglob('*.md')))}")
    print()
    
    # Run tests
    print("🚀 Running validation tests...")
    results = tester.run_all_tests()
    
    # Show summary
    passed = len([r for r in results if r.status == "PASS"])
    failed = len([r for r in results if r.status == "FAIL"]) 
    skipped = len([r for r in results if r.status == "SKIP"])
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped: {skipped}")
    
    # Show any critical or high issues
    critical = [r for r in results if r.status == "FAIL" and r.severity.value == "critical"]
    high = [r for r in results if r.status == "FAIL" and r.severity.value == "high"]
    
    if critical:
        print(f"\n🔴 Critical Issues: {len(critical)}")
        for result in critical:
            print(f"  - {result.message}")
            
    if high:
        print(f"\n🟠 High Priority Issues: {len(high)}")
        for result in high:
            print(f"  - {result.message}")
    
    print("\n📋 Generate detailed report with:")
    print("  python3 test_framework.py --format text")
    print("  python3 test_framework.py --format json")
    print("  python3 test_framework.py --format html")
    
    return len(critical) == 0 and len(high) == 0


def demo_specific_command_test():
    """Demonstrate testing a specific command."""
    print("\n" + "=" * 50)
    print("🎯 Specific Command Testing Demo")
    print("=" * 50)
    
    commands_dir = Path("../../.claude/commands")
    tester = CommandTester(commands_dir)
    
    # Test a specific command file
    code_review_path = commands_dir / "ck" / "code-review.md"
    
    if code_review_path.exists():
        print(f"🔍 Testing specific command: {code_review_path}")
        
        # This would normally be called internally, but we can demo it
        tester._test_command_file(code_review_path)
        
        # Show results for this file
        file_results = [r for r in tester.results if r.file_path and "code-review.md" in r.file_path]
        
        for result in file_results:
            status_emoji = "✅" if result.status == "PASS" else "❌"
            print(f"  {status_emoji} {result.test_name}: {result.message}")
    else:
        print(f"❌ Command file not found: {code_review_path}")


def demo_report_generation():
    """Demonstrate different report formats."""
    print("\n" + "=" * 50)
    print("📊 Report Generation Demo")
    print("=" * 50)
    
    commands_dir = Path("../../.claude/commands")
    tester = CommandTester(commands_dir)
    
    # Run tests
    results = tester.run_all_tests()
    
    # Generate different report formats
    reports_dir = Path("demo_reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Text report
    text_report = tester.generate_report("text")
    text_file = reports_dir / "demo_report.txt"
    text_file.write_text(text_report)
    print(f"📄 Text report: {text_file}")
    
    # JSON report  
    json_report = tester.generate_report("json")
    json_file = reports_dir / "demo_report.json"
    json_file.write_text(json_report)
    print(f"📄 JSON report: {json_file}")
    
    # HTML report
    html_report = tester.generate_report("html")
    html_file = reports_dir / "demo_report.html"
    html_file.write_text(html_report)
    print(f"📄 HTML report: {html_file}")
    
    print(f"\n📁 All demo reports saved to: {reports_dir}")


if __name__ == "__main__":
    print("🎬 Starting Claude Code Commands Testing Framework Demo\n")
    
    try:
        # Run demos
        success = demo_basic_usage()
        demo_specific_command_test()
        demo_report_generation()
        
        print("\n" + "=" * 50)
        if success:
            print("🎉 Demo completed successfully!")
            print("✅ All critical and high priority tests passed")
        else:
            print("⚠️  Demo completed with issues found")
            print("🔧 Check the reports for details on what needs to be fixed")
            
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        sys.exit(1)