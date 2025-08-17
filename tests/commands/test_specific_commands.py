#!/usr/bin/env python3
"""
Specific Test Cases for Individual Claude Code Commands

This module contains detailed test cases for each command in the .claude/commands directory.
"""

import unittest
from pathlib import Path
from test_framework import CommandTester, TestResult, Severity


class TestSpecificCommands(unittest.TestCase):
    """Test cases for specific commands."""
    
    def setUp(self):
        """Set up test environment."""
        self.commands_dir = Path(".claude/commands")
        self.tester = CommandTester(self.commands_dir)
        
    def test_code_review_command(self):
        """Test the code-review command specifically."""
        file_path = self.commands_dir / "ck" / "code-review.md"
        
        if not file_path.exists():
            self.fail(f"Code review command not found: {file_path}")
            
        content = file_path.read_text()
        metadata = self.tester._parse_frontmatter(content)
        
        # Specific tests for code-review command
        self.assertIn("code-review", metadata.command or "")
        self.assertIn("Quality", metadata.category or "")
        self.assertTrue(metadata.wave_enabled)
        self.assertEqual(metadata.performance_profile, "optimization")
        
        # Check for required sections
        required_sections = [
            "## Code Review Checklist",
            "### 📁 File Organization",
            "### 🔒 Security Review", 
            "### 📚 Documentation Review",
            "## Prevention Strategies"
        ]
        
        for section in required_sections:
            self.assertIn(section, content, 
                         f"Code review command missing section: {section}")
                         
        # Check for bash command patterns
        self.assertIn("!`find", content)
        self.assertIn("!`git status", content)
        self.assertIn("!`git log", content)
        
    def test_git_commit_push_command(self):
        """Test the git-commit-push command specifically."""
        file_path = self.commands_dir / "ck" / "git-commit-push.md"
        
        if not file_path.exists():
            self.fail(f"Git commit push command not found: {file_path}")
            
        content = file_path.read_text()
        metadata = self.tester._parse_frontmatter(content)
        
        # Check allowed tools include git operations
        allowed_tools = metadata.allowed_tools or []
        git_tools = [tool for tool in allowed_tools if "git" in tool.lower()]
        self.assertTrue(git_tools, "Git command should have git tools in allowed-tools")
        
        # Check for git command patterns
        git_commands = ["git add", "git status", "git commit", "git push"]
        for cmd in git_commands:
            # Should have context gathering for these commands
            self.assertTrue(
                any(f"!`{cmd}" in content or f"`{cmd}" in content for cmd in git_commands),
                "Git command should reference git operations"
            )
            
    def test_security_review_command(self):
        """Test the security-review command specifically.""" 
        file_path = self.commands_dir / "ck" / "security-review.md"
        
        if not file_path.exists():
            self.fail(f"Security review command not found: {file_path}")
            
        content = file_path.read_text()
        
        # Security-specific checks
        security_keywords = [
            "vulnerability", "security", "authentication", "authorization",
            "encryption", "sanitization", "validation"
        ]
        
        found_keywords = [kw for kw in security_keywords if kw in content.lower()]
        self.assertTrue(found_keywords, 
                       "Security review should contain security-related terminology")
                       
    def test_testcases_command(self):
        """Test the testcases command specifically."""
        file_path = self.commands_dir / "ck" / "testcases.md"
        
        if not file_path.exists():
            self.fail(f"Test cases command not found: {file_path}")
            
        content = file_path.read_text()
        metadata = self.tester._parse_frontmatter(content)
        
        # Should allow testing tools
        allowed_tools = metadata.allowed_tools or []
        test_tools = [tool for tool in allowed_tools 
                     if any(t in tool.lower() for t in ["pytest", "test", "npm", "yarn"])]
        self.assertTrue(test_tools, 
                       "Test cases command should allow testing tools")
                       
        # Check for testing terminology
        testing_keywords = ["test", "coverage", "mock", "assert", "spec"]
        found_keywords = [kw for kw in testing_keywords if kw in content.lower()]
        self.assertTrue(found_keywords,
                       "Test cases command should contain testing terminology")
                       
    def test_update_docs_command(self):
        """Test the update-docs command specifically."""
        file_path = self.commands_dir / "ck" / "update-docs.md"
        
        if not file_path.exists():
            self.fail(f"Update docs command not found: {file_path}")
            
        content = file_path.read_text()
        
        # Documentation-specific checks
        doc_keywords = [
            "documentation", "readme", "changelog", "markdown", 
            "docs", "guide", "reference"
        ]
        
        found_keywords = [kw for kw in doc_keywords if kw in content.lower()]
        self.assertTrue(found_keywords,
                       "Update docs command should contain documentation terminology")
                       
    def test_fix_issue_command(self):
        """Test the fix-issue command specifically."""
        file_path = self.commands_dir / "ck" / "fix-issue.md"
        
        if not file_path.exists():
            self.fail(f"Fix issue command not found: {file_path}")
            
        content = file_path.read_text()
        
        # Should contain problem-solving terminology
        fix_keywords = ["fix", "issue", "bug", "error", "problem", "resolve"]
        found_keywords = [kw for kw in fix_keywords if kw in content.lower()]
        self.assertTrue(found_keywords,
                       "Fix issue command should contain problem-solving terminology")
                       
    def test_rule_engine_command(self):
        """Test the rule-engine command specifically."""
        file_path = self.commands_dir / "ck" / "rule-engine.md"
        
        if not file_path.exists():
            self.fail(f"Rule engine command not found: {file_path}")
            
        content = file_path.read_text()
        
        # Should contain rule/logic terminology
        rule_keywords = ["rule", "engine", "logic", "pattern", "condition"]
        found_keywords = [kw for kw in rule_keywords if kw in content.lower()]
        self.assertTrue(found_keywords,
                       "Rule engine command should contain rule-related terminology")


class TestCommandIntegration(unittest.TestCase):
    """Integration tests for command interactions."""
    
    def setUp(self):
        """Set up test environment."""
        self.commands_dir = Path(".claude/commands")
        self.tester = CommandTester(self.commands_dir)
        
    def test_all_commands_have_unique_names(self):
        """Ensure all commands have unique names/paths."""
        command_files = list(self.commands_dir.rglob("*.md"))
        command_names = []
        
        for file_path in command_files:
            content = file_path.read_text()
            metadata = self.tester._parse_frontmatter(content)
            if metadata.command:
                command_names.append(metadata.command)
                
        # Check for duplicates
        duplicate_names = []
        seen = set()
        for name in command_names:
            if name in seen:
                duplicate_names.append(name)
            else:
                seen.add(name)
                
        self.assertEqual(duplicate_names, [], 
                        f"Duplicate command names found: {duplicate_names}")
                        
    def test_commands_follow_naming_convention(self):
        """Test that commands follow consistent naming conventions."""
        command_files = list(self.commands_dir.rglob("*.md"))
        
        for file_path in command_files:
            content = file_path.read_text()
            metadata = self.tester._parse_frontmatter(content)
            
            if metadata.command:
                # Commands should start with /ck: for this namespace
                self.assertTrue(metadata.command.startswith('/ck:'),
                               f"Command {metadata.command} should start with /ck:")
                               
                # Command names should be kebab-case
                command_name = metadata.command.replace('/ck:', '')
                self.assertTrue(all(c.islower() or c == '-' for c in command_name),
                               f"Command name should be kebab-case: {command_name}")
                               
    def test_wave_enabled_commands_have_performance_profile(self):
        """Test that wave-enabled commands specify performance profiles."""
        command_files = list(self.commands_dir.rglob("*.md"))
        
        for file_path in command_files:
            content = file_path.read_text()
            metadata = self.tester._parse_frontmatter(content)
            
            if metadata.wave_enabled:
                self.assertIsNotNone(metadata.performance_profile,
                                   f"Wave-enabled command {file_path.name} should specify performance-profile")
                                   
    def test_allowed_tools_consistency(self):
        """Test that allowed-tools declarations are consistent."""
        command_files = list(self.commands_dir.rglob("*.md"))
        common_tools = set()
        
        for file_path in command_files:
            content = file_path.read_text()
            metadata = self.tester._parse_frontmatter(content)
            
            if metadata.allowed_tools:
                for tool in metadata.allowed_tools:
                    if "(*)" in tool:  # Common tools like Read(*), Write(*)
                        common_tools.add(tool)
                        
        # Common tools should appear in multiple commands
        self.assertTrue(len(common_tools) > 0, 
                       "Should have some common tools across commands")


class TestCommandDocumentation(unittest.TestCase):
    """Tests for command documentation quality."""
    
    def setUp(self):
        """Set up test environment."""
        self.commands_dir = Path(".claude/commands")
        
    def test_commands_have_clear_descriptions(self):
        """Test that all commands have clear descriptions."""
        command_files = list(self.commands_dir.rglob("*.md"))
        
        for file_path in command_files:
            content = file_path.read_text()
            tester = CommandTester()
            metadata = tester._parse_frontmatter(content)
            
            # Should have either description or purpose
            has_description = bool(metadata.description and len(metadata.description.strip()) > 10)
            has_purpose = bool(metadata.purpose and len(metadata.purpose.strip()) > 10)
            
            self.assertTrue(has_description or has_purpose,
                           f"Command {file_path.name} should have meaningful description or purpose")
                           
    def test_commands_have_examples(self):
        """Test that commands include usage examples."""
        command_files = list(self.commands_dir.rglob("*.md"))
        
        for file_path in command_files:
            content = file_path.read_text()
            
            # Look for code blocks or example patterns
            has_code_blocks = "```" in content
            has_examples = any(keyword in content.lower() 
                             for keyword in ["example", "usage", "pattern"])
            has_arguments = "$ARGUMENTS" in content
            
            example_indicators = has_code_blocks or has_examples or has_arguments
            
            self.assertTrue(example_indicators,
                           f"Command {file_path.name} should include usage examples or patterns")


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)