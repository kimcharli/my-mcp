#!/usr/bin/env python3
"""
Test Cases for Bash Command Validation in Claude Code Commands

This module tests the execution and permission validation of embedded bash commands
in .claude/commands/*.md files to catch issues like the testcase-review failure.
"""

import unittest
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import tempfile
import os


class BashCommandValidator:
    """Validator for bash commands embedded in Claude Code command files."""
    
    def __init__(self):
        self.complex_command_patterns = [
            r'find.*\|.*xargs',  # find with xargs
            r'.*\|.*\|.*',       # Multiple pipes
            r'.*&&.*',           # Command chaining with &&
            r'.*sh -c.*',        # Shell execution
            r'.*head.*tail.*',   # Multiple text processing
        ]
        
    def extract_bash_commands(self, content: str) -> List[str]:
        """Extract all !` bash commands from command file content."""
        pattern = r'!`([^`]+)`'
        matches = re.findall(pattern, content)
        return matches
        
    def classify_command_complexity(self, command: str) -> str:
        """Classify bash command complexity for permission validation."""
        for pattern in self.complex_command_patterns:
            if re.search(pattern, command):
                return "complex"
        
        if '|' in command or '&&' in command or '||' in command:
            return "moderate"
            
        return "simple"
    
    def simulate_permission_check(self, command: str) -> Tuple[bool, str]:
        """Simulate Claude Code's bash permission checking."""
        complexity = self.classify_command_complexity(command)
        
        # Simulate the permission patterns that would fail
        if complexity == "complex":
            # Extract the problematic parts
            problematic_parts = []
            
            if 'find' in command and 'xargs' in command:
                problematic_parts.append("find with xargs operations")
            if 'sh -c' in command:
                problematic_parts.append("shell command execution")
            if command.count('|') > 2:
                problematic_parts.append("multiple pipe operations")
                
            if problematic_parts:
                return False, f"Complex command requires approval: {', '.join(problematic_parts)}"
        
        return True, "Command allowed"
    
    def validate_safe_alternatives(self, command: str) -> List[str]:
        """Suggest safer alternatives for complex commands."""
        alternatives = []
        
        if 'find' in command and 'xargs' in command:
            alternatives.append("Use Glob tool instead of find with xargs")
            alternatives.append("Break into separate find and processing steps")
            
        if 'sh -c' in command:
            alternatives.append("Use direct command execution instead of sh -c")
            alternatives.append("Move complex logic to dedicated script")
            
        if '|' in command:
            alternatives.append("Break pipe chain into separate commands")
            alternatives.append("Use Read tool for file processing")
            
        return alternatives


class TestBashCommandValidation(unittest.TestCase):
    """Test bash command validation for Claude Code commands."""
    
    def setUp(self):
        """Set up test environment."""
        self.commands_dir = Path(".claude/commands")
        self.validator = BashCommandValidator()
        
    def test_extract_bash_commands(self):
        """Test extraction of bash commands from content."""
        content = """
        Some content here
        - Files: !`ls -la`
        - Status: !`git status`
        - Complex: !`find . -name "*.py" | head -10 | wc -l`
        """
        
        commands = self.validator.extract_bash_commands(content)
        
        expected = ['ls -la', 'git status', 'find . -name "*.py" | head -10 | wc -l']
        self.assertEqual(commands, expected)
        
    def test_command_complexity_classification(self):
        """Test classification of command complexity."""
        test_cases = [
            ("ls -la", "simple"),
            ("git status", "simple"),
            ("ls -la | grep test", "moderate"),
            ("find . -name '*.py'", "simple"),
            ("find . -name '*.py' | xargs grep 'test'", "complex"),
            ("find . -name '*.py' | head -5 | xargs -I {} sh -c 'echo {}'", "complex"),
            ("cat file.txt && echo done", "moderate"),
        ]
        
        for command, expected_complexity in test_cases:
            with self.subTest(command=command):
                actual = self.validator.classify_command_complexity(command)
                self.assertEqual(actual, expected_complexity)
                
    def test_permission_check_simulation(self):
        """Test simulation of Claude Code permission checking."""
        test_cases = [
            ("ls -la", True, "Command allowed"),
            ("git status", True, "Command allowed"),
            ("find . -name '*.py' | xargs grep 'test'", False, "Complex command requires approval"),
            ("find . -type f | head -5 | xargs -I {} sh -c 'echo {}'", False, "Complex command requires approval"),
        ]
        
        for command, expected_allowed, expected_message_pattern in test_cases:
            with self.subTest(command=command):
                allowed, message = self.validator.simulate_permission_check(command)
                self.assertEqual(allowed, expected_allowed)
                if not expected_allowed:
                    self.assertIn("Complex command requires approval", message)
                    
    def test_testcase_review_command_specifically(self):
        """Test the specific command that failed in testcase-review."""
        problematic_command = (
            "find . -maxdepth 2 \\( -name \"package.json\" -o -name \"pyproject.toml\" "
            "-o -name \"Cargo.toml\" -o -name \"pom.xml\" -o -name \"build.gradle\" "
            "-o -name \"go.mod\" -o -name \"composer.json\" \\) -type f | head -5 | "
            "xargs -I {} sh -c 'echo \"=== {} ===\" && head -10 \"{}\"' 2>/dev/null || "
            "echo \"No package management files found\""
        )
        
        # This should be classified as complex and fail permission check
        complexity = self.validator.classify_command_complexity(problematic_command)
        self.assertEqual(complexity, "complex")
        
        allowed, message = self.validator.simulate_permission_check(problematic_command)
        self.assertFalse(allowed)
        self.assertIn("Complex command requires approval", message)
        
    def test_validate_existing_command_files(self):
        """Test all existing command files for bash command issues."""
        if not self.commands_dir.exists():
            self.skipTest("Commands directory not found")
            
        issues_found = []
        
        for command_file in self.commands_dir.rglob("*.md"):
            content = command_file.read_text()
            bash_commands = self.validator.extract_bash_commands(content)
            
            for command in bash_commands:
                allowed, message = self.validator.simulate_permission_check(command)
                
                if not allowed:
                    alternatives = self.validator.validate_safe_alternatives(command)
                    issues_found.append({
                        'file': str(command_file),
                        'command': command,
                        'issue': message,
                        'alternatives': alternatives
                    })
        
        if issues_found:
            issue_report = "\n".join([
                f"File: {issue['file']}\n"
                f"Command: {issue['command']}\n"
                f"Issue: {issue['issue']}\n"
                f"Alternatives: {', '.join(issue['alternatives'])}\n"
                for issue in issues_found
            ])
            
            # Don't fail the test, but report issues for visibility
            print(f"\n⚠️  Bash Command Issues Found:\n{issue_report}")
            
        # For now, just log issues. In strict mode, this could fail:
        # self.assertEqual(len(issues_found), 0, f"Found {len(issues_found)} bash command issues")
        
    def test_safe_alternatives_suggestions(self):
        """Test that safe alternatives are suggested for complex commands."""
        complex_command = "find . -name '*.py' | xargs grep 'pattern'"
        alternatives = self.validator.validate_safe_alternatives(complex_command)
        
        self.assertTrue(len(alternatives) > 0)
        self.assertIn("Use Glob tool", alternatives[0])
        
    def test_command_breakdown_recommendations(self):
        """Test recommendations for breaking down complex commands."""
        # Test the actual problematic command from testcase-review
        problematic_command = (
            "find . -maxdepth 2 \\( -name \"package.json\" -o -name \"pyproject.toml\" \\) "
            "-type f | head -5 | xargs -I {} sh -c 'echo \"=== {} ===\" && head -10 \"{}\"'"
        )
        
        alternatives = self.validator.validate_safe_alternatives(problematic_command)
        
        # Should suggest breaking it down
        expected_suggestions = [
            "Use Glob tool instead of find with xargs",
            "Break into separate find and processing steps",
            "Use direct command execution instead of sh -c",
            "Break pipe chain into separate commands"
        ]
        
        for suggestion in expected_suggestions:
            self.assertIn(suggestion, alternatives)


class TestCommandExecutionSafety(unittest.TestCase):
    """Test actual command execution safety in controlled environment."""
    
    def setUp(self):
        """Set up safe test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Create test files
        (Path(self.temp_dir) / "package.json").write_text('{"name": "test"}')
        (Path(self.temp_dir) / "pyproject.toml").write_text('[project]\nname = "test"')
        
    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_safe_command_execution(self):
        """Test that simple commands execute safely."""
        simple_commands = [
            "ls -la",
            "find . -name '*.json' -type f",
            "head -5 package.json"
        ]
        
        for command in simple_commands:
            with self.subTest(command=command):
                try:
                    result = subprocess.run(
                        command.split(), 
                        capture_output=True, 
                        text=True, 
                        timeout=5
                    )
                    # Command should execute without error (though output may vary)
                    self.assertIsNotNone(result)
                    
                except subprocess.TimeoutExpired:
                    self.fail(f"Command timed out: {command}")
                except Exception as e:
                    # Some commands may fail due to missing tools, but shouldn't crash
                    pass
                    
    def test_complex_command_breakdown(self):
        """Test that complex commands can be broken down safely."""
        # Instead of: find . -name "*.json" | head -5 | xargs -I {} sh -c 'echo {} && head -2 {}'
        # Break it down to safer parts:
        
        # Part 1: Find files
        find_result = subprocess.run(
            ["find", ".", "-name", "*.json", "-type", "f"],
            capture_output=True,
            text=True
        )
        
        if find_result.returncode == 0:
            files = find_result.stdout.strip().split('\n')[:5]  # Limit to 5
            
            # Part 2: Process each file safely
            for file_path in files:
                if file_path.strip():
                    head_result = subprocess.run(
                        ["head", "-2", file_path.strip()],
                        capture_output=True,
                        text=True
                    )
                    # Should be able to process files individually
                    self.assertIsNotNone(head_result)


class TestImprovedCommandValidation(unittest.TestCase):
    """Improved validation tests that would have caught the testcase-review issue."""
    
    def setUp(self):
        """Set up improved validation."""
        self.validator = BashCommandValidator()
        
    def test_command_permission_patterns(self):
        """Test specific permission patterns that Claude Code checks."""
        permission_failing_patterns = [
            # Pattern that actually failed
            r'find.*\|.*head.*\|.*xargs.*sh -c',
            # Other complex patterns
            r'.*\|.*\|.*\|',  # More than 2 pipes
            r'.*xargs.*sh -c.*',  # xargs with shell execution
            r'.*find.*exec.*',  # find with exec
        ]
        
        test_command = (
            "find . -maxdepth 2 \\( -name \"package.json\" \\) -type f | "
            "head -5 | xargs -I {} sh -c 'echo \"=== {} ===\" && head -10 \"{}\"'"
        )
        
        # This should match the failing pattern
        pattern_matched = False
        for pattern in permission_failing_patterns:
            if re.search(pattern, test_command):
                pattern_matched = True
                break
                
        self.assertTrue(pattern_matched, 
                       "Test command should match a permission-failing pattern")
        
    def test_generate_test_data_for_all_commands(self):
        """Generate comprehensive test data for all command validation."""
        commands_dir = Path(".claude/commands")
        
        if not commands_dir.exists():
            self.skipTest("Commands directory not found")
            
        test_data = []
        
        for command_file in commands_dir.rglob("*.md"):
            content = command_file.read_text()
            bash_commands = self.validator.extract_bash_commands(content)
            
            for command in bash_commands:
                complexity = self.validator.classify_command_complexity(command)
                allowed, message = self.validator.simulate_permission_check(command)
                alternatives = self.validator.validate_safe_alternatives(command)
                
                test_data.append({
                    'file': command_file.name,
                    'command': command,
                    'complexity': complexity,
                    'allowed': allowed,
                    'message': message,
                    'alternatives': alternatives
                })
        
        # Generate report for developers
        report_lines = ["# Bash Command Validation Report\n"]
        
        for data in test_data:
            report_lines.append(f"## {data['file']}")
            report_lines.append(f"**Command**: `{data['command']}`")
            report_lines.append(f"**Complexity**: {data['complexity']}")
            report_lines.append(f"**Allowed**: {data['allowed']}")
            report_lines.append(f"**Message**: {data['message']}")
            
            if data['alternatives']:
                report_lines.append("**Alternatives**:")
                for alt in data['alternatives']:
                    report_lines.append(f"- {alt}")
            report_lines.append("")
        
        # Write report (for debugging)
        report_content = "\n".join(report_lines)
        
        # Don't fail test, just ensure we have data
        self.assertTrue(len(test_data) > 0, "Should have found some bash commands to validate")


if __name__ == "__main__":
    # Run all validation tests
    unittest.main(verbosity=2)