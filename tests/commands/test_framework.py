#!/usr/bin/env python3
"""
Test Framework for Claude Code Commands

This framework validates Claude Code command prompts for:
- Proper YAML frontmatter structure
- Valid allowed-tools declarations
- Required sections and content
- Command execution patterns
- Security and best practices compliance
"""

import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Test result severity levels."""
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class TestResult:
    """Individual test result."""
    test_name: str
    status: str  # PASS, FAIL, SKIP
    severity: Severity
    message: str
    details: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class CommandMetadata:
    """Parsed command metadata from frontmatter."""
    command: Optional[str] = None
    category: Optional[str] = None
    purpose: Optional[str] = None
    description: Optional[str] = None
    allowed_tools: List[str] = None
    wave_enabled: bool = False
    performance_profile: Optional[str] = None


class CommandTester:
    """Main testing framework for Claude Code commands."""
    
    def __init__(self, commands_dir: Path = None):
        """Initialize with commands directory path."""
        self.commands_dir = commands_dir or Path(".claude/commands")
        self.results: List[TestResult] = []
        
    def run_all_tests(self) -> List[TestResult]:
        """Run all tests on all command files."""
        self.results = []
        
        if not self.commands_dir.exists():
            self.results.append(TestResult(
                "commands_directory_exists",
                "FAIL",
                Severity.CRITICAL,
                f"Commands directory not found: {self.commands_dir}"
            ))
            return self.results
            
        # Find all command files
        command_files = list(self.commands_dir.rglob("*.md"))
        
        if not command_files:
            self.results.append(TestResult(
                "command_files_exist",
                "FAIL", 
                Severity.HIGH,
                "No command files found in commands directory"
            ))
            return self.results
            
        # Test each command file
        for cmd_file in command_files:
            self._test_command_file(cmd_file)
            
        return self.results
        
    def _test_command_file(self, file_path: Path):
        """Test a single command file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            metadata = self._parse_frontmatter(content)
            
            # Run all tests for this file
            self._test_frontmatter_structure(file_path, content, metadata)
            self._test_allowed_tools_syntax(file_path, metadata)
            self._test_command_structure(file_path, content, metadata)
            self._test_security_patterns(file_path, content)
            self._test_performance_considerations(file_path, metadata)
            self._test_documentation_quality(file_path, content)
            
        except Exception as e:
            self.results.append(TestResult(
                f"file_parsing_{file_path.name}",
                "FAIL",
                Severity.CRITICAL,
                f"Failed to parse command file: {str(e)}",
                file_path=str(file_path)
            ))
            
    def _parse_frontmatter(self, content: str) -> CommandMetadata:
        """Parse YAML frontmatter from command file."""
        # Extract frontmatter
        if not content.startswith('---'):
            return CommandMetadata()
            
        parts = content.split('---', 2)
        if len(parts) < 3:
            return CommandMetadata()
            
        try:
            frontmatter = yaml.safe_load(parts[1])
            return CommandMetadata(
                command=frontmatter.get('command'),
                category=frontmatter.get('category'),
                purpose=frontmatter.get('purpose'),
                description=frontmatter.get('description'),
                allowed_tools=frontmatter.get('allowed-tools', []),
                wave_enabled=frontmatter.get('wave-enabled', False),
                performance_profile=frontmatter.get('performance-profile')
            )
        except yaml.YAMLError:
            return CommandMetadata()
            
    def _test_frontmatter_structure(self, file_path: Path, content: str, metadata: CommandMetadata):
        """Test frontmatter structure and required fields."""
        test_name = f"frontmatter_structure_{file_path.name}"
        
        # Check frontmatter exists
        if not content.startswith('---'):
            self.results.append(TestResult(
                test_name,
                "FAIL",
                Severity.HIGH,
                "Missing YAML frontmatter",
                file_path=str(file_path)
            ))
            return
            
        # Check required fields
        required_fields = ['description']
        missing_fields = []
        
        if not metadata.description and not metadata.purpose:
            missing_fields.append('description or purpose')
            
        if missing_fields:
            self.results.append(TestResult(
                test_name,
                "FAIL", 
                Severity.MEDIUM,
                f"Missing required frontmatter fields: {', '.join(missing_fields)}",
                file_path=str(file_path)
            ))
        else:
            self.results.append(TestResult(
                test_name,
                "PASS",
                Severity.INFO,
                "Frontmatter structure is valid",
                file_path=str(file_path)
            ))
            
    def _test_allowed_tools_syntax(self, file_path: Path, metadata: CommandMetadata):
        """Test allowed-tools syntax and patterns."""
        test_name = f"allowed_tools_syntax_{file_path.name}"
        
        if not metadata.allowed_tools:
            self.results.append(TestResult(
                test_name,
                "SKIP",
                Severity.INFO,
                "No allowed-tools specified",
                file_path=str(file_path)
            ))
            return
            
        valid_patterns = [
            r'^Bash\([^:]*:\*\)$',  # Bash(command:*)
            r'^Bash\([^)]*\)$',     # Bash(specific_command)
            r'^[A-Z][a-zA-Z]*\(\*\)$',  # Tool(*)
            r'^[A-Z][a-zA-Z]*\([^)]*\)$'  # Tool(params)
        ]
        
        invalid_tools = []
        if isinstance(metadata.allowed_tools, list):
            for tool in metadata.allowed_tools:
                if not any(re.match(pattern, tool) for pattern in valid_patterns):
                    invalid_tools.append(tool)
        
        if invalid_tools:
            self.results.append(TestResult(
                test_name,
                "FAIL",
                Severity.MEDIUM,
                f"Invalid allowed-tools syntax: {', '.join(invalid_tools)}",
                file_path=str(file_path)
            ))
        else:
            self.results.append(TestResult(
                test_name,
                "PASS",
                Severity.INFO,
                "Allowed-tools syntax is valid",
                file_path=str(file_path)
            ))
            
    def _test_command_structure(self, file_path: Path, content: str, metadata: CommandMetadata):
        """Test command structure and required sections."""
        test_name = f"command_structure_{file_path.name}"
        
        required_sections = ['## Context', '## Task', '## Your task']
        found_sections = []
        
        for section in required_sections:
            if section in content:
                found_sections.append(section)
                
        if not found_sections:
            self.results.append(TestResult(
                test_name,
                "FAIL",
                Severity.HIGH,
                f"Missing required sections. Expected one of: {', '.join(required_sections)}",
                file_path=str(file_path)
            ))
        else:
            self.results.append(TestResult(
                test_name,
                "PASS",
                Severity.INFO,
                f"Found required sections: {', '.join(found_sections)}",
                file_path=str(file_path)
            ))
            
    def _test_security_patterns(self, file_path: Path, content: str):
        """Test for security anti-patterns and best practices."""
        test_name = f"security_patterns_{file_path.name}"
        
        # Security anti-patterns to detect
        security_issues = []
        
        # Check for hardcoded secrets patterns
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']'
        ]
        
        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                security_issues.append(f"Potential hardcoded secret: {pattern}")
                
        # Check for unsafe file operations
        unsafe_patterns = [
            r'rm\s+-rf',
            r'sudo\s+',
            r'eval\s*\(',
            r'exec\s*\('
        ]
        
        for pattern in unsafe_patterns:
            if re.search(pattern, content):
                security_issues.append(f"Potentially unsafe operation: {pattern}")
                
        if security_issues:
            self.results.append(TestResult(
                test_name,
                "FAIL",
                Severity.HIGH,
                f"Security issues found: {'; '.join(security_issues)}",
                file_path=str(file_path)
            ))
        else:
            self.results.append(TestResult(
                test_name,
                "PASS",
                Severity.INFO,
                "No security anti-patterns detected",
                file_path=str(file_path)
            ))
            
    def _test_performance_considerations(self, file_path: Path, metadata: CommandMetadata):
        """Test performance profile and optimization indicators."""
        test_name = f"performance_profile_{file_path.name}"
        
        # Check if performance profile is specified for wave-enabled commands
        if metadata.wave_enabled and not metadata.performance_profile:
            self.results.append(TestResult(
                test_name,
                "FAIL",
                Severity.MEDIUM,
                "Wave-enabled commands should specify performance-profile",
                file_path=str(file_path)
            ))
        elif metadata.performance_profile:
            valid_profiles = ['optimization', 'standard', 'complex']
            if metadata.performance_profile not in valid_profiles:
                self.results.append(TestResult(
                    test_name,
                    "FAIL",
                    Severity.LOW,
                    f"Invalid performance-profile. Valid options: {', '.join(valid_profiles)}",
                    file_path=str(file_path)
                ))
            else:
                self.results.append(TestResult(
                    test_name,
                    "PASS",
                    Severity.INFO,
                    f"Valid performance profile: {metadata.performance_profile}",
                    file_path=str(file_path)
                ))
        else:
            self.results.append(TestResult(
                test_name,
                "PASS",
                Severity.INFO,
                "Performance considerations appropriate for command type",
                file_path=str(file_path)
            ))
            
    def _test_documentation_quality(self, file_path: Path, content: str):
        """Test documentation quality and completeness."""
        test_name = f"documentation_quality_{file_path.name}"
        
        quality_issues = []
        
        # Check for minimum content length
        content_lines = [line.strip() for line in content.split('\n') if line.strip()]
        if len(content_lines) < 10:
            quality_issues.append("Command content seems too brief")
            
        # Check for examples or usage patterns
        example_indicators = ['```', 'Example:', 'Usage:', '# ', '$ARGUMENTS']
        has_examples = any(indicator in content for indicator in example_indicators)
        if not has_examples:
            quality_issues.append("Missing usage examples or code blocks")
            
        # Check for clear task description
        task_indicators = ['task', 'Task', 'objective', 'goal', 'perform', 'execute']
        has_clear_task = any(indicator in content.lower() for indicator in task_indicators)
        if not has_clear_task:
            quality_issues.append("Task description unclear or missing")
            
        if quality_issues:
            self.results.append(TestResult(
                test_name,
                "FAIL",
                Severity.LOW,
                f"Documentation quality issues: {'; '.join(quality_issues)}",
                file_path=str(file_path)
            ))
        else:
            self.results.append(TestResult(
                test_name,
                "PASS",
                Severity.INFO,
                "Documentation quality is good",
                file_path=str(file_path)
            ))
            
    def generate_report(self, format: str = "text") -> str:
        """Generate test report in specified format."""
        if format == "json":
            return self._generate_json_report()
        elif format == "html":
            return self._generate_html_report()
        else:
            return self._generate_text_report()
            
    def _generate_text_report(self) -> str:
        """Generate text format test report."""
        if not self.results:
            return "No test results available."
            
        # Group results by status and severity
        passed = [r for r in self.results if r.status == "PASS"]
        failed = [r for r in self.results if r.status == "FAIL"]
        skipped = [r for r in self.results if r.status == "SKIP"]
        
        # Count by severity
        critical = [r for r in failed if r.severity == Severity.CRITICAL]
        high = [r for r in failed if r.severity == Severity.HIGH]
        medium = [r for r in failed if r.severity == Severity.MEDIUM]
        low = [r for r in failed if r.severity == Severity.LOW]
        
        report = []
        report.append("# Claude Code Commands Test Report")
        report.append("=" * 50)
        report.append(f"Total Tests: {len(self.results)}")
        report.append(f"✅ Passed: {len(passed)}")
        report.append(f"❌ Failed: {len(failed)}")
        report.append(f"⏭️  Skipped: {len(skipped)}")
        report.append("")
        
        if failed:
            report.append("## Failed Tests by Severity")
            report.append("")
            
            for severity, issues in [("🔴 CRITICAL", critical), ("🟠 HIGH", high), ("🟡 MEDIUM", medium), ("🔵 LOW", low)]:
                if issues:
                    report.append(f"### {severity} ({len(issues)} issues)")
                    for result in issues:
                        report.append(f"- **{result.test_name}**: {result.message}")
                        if result.file_path:
                            report.append(f"  📁 {result.file_path}")
                        if result.details:
                            report.append(f"  📋 {result.details}")
                    report.append("")
                    
        if passed:
            report.append(f"## ✅ Passed Tests ({len(passed)})")
            report.append("")
            for result in passed:
                report.append(f"- {result.test_name}: {result.message}")
                
        return "\n".join(report)
        
    def _generate_json_report(self) -> str:
        """Generate JSON format test report."""
        report_data = {
            "summary": {
                "total_tests": len(self.results),
                "passed": len([r for r in self.results if r.status == "PASS"]),
                "failed": len([r for r in self.results if r.status == "FAIL"]),
                "skipped": len([r for r in self.results if r.status == "SKIP"])
            },
            "results": []
        }
        
        for result in self.results:
            report_data["results"].append({
                "test_name": result.test_name,
                "status": result.status,
                "severity": result.severity.value,
                "message": result.message,
                "details": result.details,
                "file_path": result.file_path,
                "line_number": result.line_number
            })
            
        return json.dumps(report_data, indent=2)
        
    def _generate_html_report(self) -> str:
        """Generate HTML format test report."""
        # Basic HTML template - could be enhanced with CSS/JS
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Claude Code Commands Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .test-result {{ margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }}
        .pass {{ border-left-color: #4CAF50; }}
        .fail {{ border-left-color: #f44336; }}
        .skip {{ border-left-color: #ff9800; }}
        .critical {{ background-color: #ffebee; }}
        .high {{ background-color: #fff3e0; }}
        .medium {{ background-color: #f3e5f5; }}
        .low {{ background-color: #e8f5e8; }}
    </style>
</head>
<body>
    <h1>Claude Code Commands Test Report</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Tests: {total}</p>
        <p>✅ Passed: {passed}</p>
        <p>❌ Failed: {failed}</p>
        <p>⏭️ Skipped: {skipped}</p>
    </div>
    <div class="results">
        <h2>Test Results</h2>
        {results_html}
    </div>
</body>
</html>
        """
        
        # Generate results HTML
        results_html = []
        for result in self.results:
            css_class = f"{result.status.lower()} {result.severity.value}"
            results_html.append(f"""
                <div class="test-result {css_class}">
                    <h3>{result.test_name} - {result.status}</h3>
                    <p><strong>Message:</strong> {result.message}</p>
                    {f'<p><strong>File:</strong> {result.file_path}</p>' if result.file_path else ''}
                    {f'<p><strong>Details:</strong> {result.details}</p>' if result.details else ''}
                </div>
            """)
            
        return html_template.format(
            total=len(self.results),
            passed=len([r for r in self.results if r.status == "PASS"]),
            failed=len([r for r in self.results if r.status == "FAIL"]),
            skipped=len([r for r in self.results if r.status == "SKIP"]),
            results_html="".join(results_html)
        )


def main():
    """Main test runner function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Claude Code Commands")
    parser.add_argument("--commands-dir", type=Path, default=Path(".claude/commands"),
                       help="Path to commands directory")
    parser.add_argument("--format", choices=["text", "json", "html"], default="text",
                       help="Output format")
    parser.add_argument("--output", type=Path, help="Output file path")
    
    args = parser.parse_args()
    
    # Run tests
    tester = CommandTester(args.commands_dir)
    results = tester.run_all_tests()
    
    # Generate report
    report = tester.generate_report(args.format)
    
    if args.output:
        args.output.write_text(report, encoding='utf-8')
        print(f"Report written to: {args.output}")
    else:
        print(report)
        
    # Exit with appropriate code
    failed_count = len([r for r in results if r.status == "FAIL"])
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    exit(main())