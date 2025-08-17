#!/usr/bin/env python3
"""
Test cases for /ck:code-review security scanning functionality.
Validates that the updated command catches security issues that were previously missed.
"""

import os
import tempfile
import subprocess
import shutil
from pathlib import Path


class TestCodeReviewSecurity:
    """Test the enhanced security scanning in /ck:code-review command."""
    
    def setup_method(self):
        """Create a temporary test project directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
    def teardown_method(self):
        """Clean up test directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, filename: str, content: str):
        """Helper to create test files."""
        with open(filename, 'w') as f:
            f.write(content)
    
    def run_security_scan_commands(self):
        """Run the security scan commands from the updated prompt."""
        results = {}
        
        # Step 1: Find executable files in root
        try:
            result = subprocess.run([
                'find', '.', '-maxdepth', '1', '(',
                '-name', '*.js', '-o', '-name', '*.py', '-o', 
                '-name', '*.ts', '-o', '-name', '*.sh', '-o', 
                '-name', '*.bat', ')', '-type', 'f'
            ], capture_output=True, text=True)
            import re

from security_test_helper import run_security_scan

class TestCodeReviewSecurity:
    """Test the enhanced security scanning in /ck:code-review command."""
    
    def setup_method(self):
        """Create a temporary test project directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
    def teardown_method(self):
        """Clean up test directory."""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, filename: str, content: str):
        """Helper to create test files."""
        with open(filename, 'w') as f:
            f.write(content)
    
    def run_security_scan_commands(self):
        """Run the security scan commands from the updated prompt."""
        return run_security_scan('.')

        except Exception as e:
            results['root_files'] = []
        
        # Step 3: Credential scan
        try:
            result = subprocess.run([
                'grep', '-r', '-i', 
                'password\\|secret\\|token\\|api.*key\\|admin:admin\\|10\\.\\|192\\.168\\.',
                '--include=*.js', '--include=*.ts', '--include=*.py', '--include=*.json',
                '--exclude-dir=node_modules', '--exclude-dir=dist', '.'
            ], capture_output=True, text=True)
            results['credentials'] = result.stdout.strip().split('\n') if result.stdout.strip() else []
        except Exception as e:
            results['credentials'] = []
        
        # Step 4: Production URL scan
        try:
            result = subprocess.run([
                'grep', '-r', '-E', 'https://.*\\.(46|85)\\.',
                '--include=*.js', '--include=*.ts', '.'
            ], capture_output=True, text=True)
            results['production_urls'] = result.stdout.strip().split('\n') if result.stdout.strip() else []
        except Exception as e:
            results['production_urls'] = []
        
        return results

    def test_root_file_detection(self):
        """Test that executable files in root are detected."""
        # Create test files that should be detected
        self.create_test_file('debug-test.js', '// Debug script')
        self.create_test_file('temp-script.py', '# Temp script')
        self.create_test_file('test-runner.ts', '// Test runner')
        
        results = self.run_security_scan_commands()
        
        # Should find all three files
        assert './debug-test.js' in results['root_files']
        assert './temp-script.py' in results['root_files']
        assert './test-runner.ts' in results['root_files']
        
        print("✅ Root file detection working correctly")

    def test_credential_detection(self):
        """Test that hardcoded credentials are detected."""
        # Create files with various credential patterns
        self.create_test_file('debug-credentials.js', '''
            const adminUser = "admin";
            const adminPassword = "admin";
            const apiKey = "sk-1234567890abcdef";
            const dbPassword = "secret123";
            const token = "bearer-token-here";
        ''')
        
        self.create_test_file('config.py', '''
            API_SECRET = "my-secret-key"
            PASSWORD = "admin:admin"
            DB_TOKEN = "database-token"
        ''')
        
        results = self.run_security_scan_commands()
        
        # Should detect credential patterns
        credential_matches = [line for line in results['credentials'] if line]
        assert len(credential_matches) > 0
        
        # Check specific patterns
        credential_text = '\n'.join(credential_matches)
        assert 'admin' in credential_text.lower()
        assert 'secret' in credential_text.lower() or 'password' in credential_text.lower()
        
        print(f"✅ Credential detection found {len(credential_matches)} matches")

    def test_production_ip_detection(self):
        """Test that production IPs are detected."""
        self.create_test_file('network-config.js', '''
            const serverIP = "10.0.1.100";
            const dbHost = "192.168.1.50";
            const internalAPI = "172.16.0.10";
        ''')
        
        results = self.run_security_scan_commands()
        
        # Should detect IP patterns (these will be in credentials results due to regex overlap)
        ip_matches = [line for line in results['credentials'] if any(ip in line for ip in ['10.', '192.168.', '172.'])]
        assert len(ip_matches) > 0
        
        print(f"✅ Production IP detection found {len(ip_matches)} matches")

    def test_production_url_detection(self):
        """Test that production URLs with specific patterns are detected."""
        self.create_test_file('api-config.js', '''
            const prodAPI = "https://api.example.46.com";
            const backupAPI = "https://backup.service.85.net";
            const adminPanel = "https://admin.system.46.org";
        ''')
        
        results = self.run_security_scan_commands()
        
        # Should detect .46 and .85 URL patterns
        url_matches = [line for line in results['production_urls'] if line]
        assert len(url_matches) > 0
        
        url_text = '\n'.join(url_matches)
        assert '.46.' in url_text or '.85.' in url_text
        
        print(f"✅ Production URL detection found {len(url_matches)} matches")

    def test_debug_file_patterns(self):
        """Test that debug file patterns are detected in root."""
        # Create files with debug patterns that should be flagged
        debug_files = [
            'debug-connect.js',
            'debug-correct-path.js',  # The original issue!
            'temp-fix.js',
            'test-connection.js',
            'scratch-pad.py'
        ]
        
        for filename in debug_files:
            self.create_test_file(filename, f'// {filename} - should not be in root!')
        
        results = self.run_security_scan_commands()
        
        # All debug files should be detected
        for filename in debug_files:
            assert f'./{filename}' in results['root_files']
        
        print(f"✅ Debug file pattern detection found {len(debug_files)} files")

    def test_comprehensive_security_scenario(self):
        """Test the exact scenario that was missed in the original review."""
        # Recreate the original issue scenario
        self.create_test_file('debug-correct-path.js', '''
            // Debug script that was missed in original review
            const admin = "admin";
            const pass = "admin"; 
            const serverUrl = "https://production.46.example.com";
            const dbHost = "10.0.0.85";
            
            // This should have been caught!
            console.log("Connecting to production...");
        ''')
        
        self.create_test_file('test-connection.js', '''
            const apiKey = "secret-key-here";
            const prodDB = "192.168.100.50";
        ''')
        
        results = self.run_security_scan_commands()
        
        # Verify comprehensive detection
        issues_found = 0
        
        # 1. Root files detected
        assert './debug-correct-path.js' in results['root_files']
        assert './test-connection.js' in results['root_files']
        issues_found += 2
        
        # 2. Credentials detected
        credential_matches = [line for line in results['credentials'] if line]
        assert len(credential_matches) > 0
        issues_found += len(credential_matches)
        
        # 3. Production URLs detected
        url_matches = [line for line in results['production_urls'] if line]
        assert len(url_matches) > 0
        issues_found += len(url_matches)
        
        print(f"🚨 COMPREHENSIVE TEST: Found {issues_found} security issues")
        print("✅ This would have caught the original debug-correct-path.js issue!")
        
        return issues_found > 0

    def test_clean_project_scenario(self):
        """Test that a clean project structure passes security scan."""
        # Create a proper project structure
        os.makedirs('src', exist_ok=True)
        os.makedirs('tests', exist_ok=True)
        os.makedirs('scripts', exist_ok=True)
        
        # Essential files only in root
        self.create_test_file('package.json', '{"name": "test-project"}')
        self.create_test_file('README.md', '# Test Project')
        
        # Source code in proper location
        self.create_test_file('src/main.js', 'console.log("Hello world");')
        
        # Debug scripts in proper location
        self.create_test_file('scripts/debug-helper.js', '// Debug helper in correct location')
        
        results = self.run_security_scan_commands()
        
        # Should find no executable files in root
        assert len(results['root_files']) == 0 or results['root_files'] == ['']
        
        # Should find no credentials
        credential_matches = [line for line in results['credentials'] if line]
        assert len(credential_matches) == 0
        
        # Should find no production URLs
        url_matches = [line for line in results['production_urls'] if line]
        assert len(url_matches) == 0
        
        print("✅ Clean project structure passes all security scans")


def run_manual_tests():
    """Run tests manually for demonstration."""
    print("🧪 Testing Enhanced /ck:code-review Security Scanning")
    print("=" * 60)
    
    test_suite = TestCodeReviewSecurity()
    
    try:
        test_suite.setup_method()
        
        print("\n1. Testing Root File Detection...")
        test_suite.test_root_file_detection()
        
        print("\n2. Testing Credential Detection...")
        test_suite.test_credential_detection()
        
        print("\n3. Testing Production IP Detection...")
        test_suite.test_production_ip_detection()
        
        print("\n4. Testing Production URL Detection...")
        test_suite.test_production_url_detection()
        
        print("\n5. Testing Debug File Patterns...")
        test_suite.test_debug_file_patterns()
        
        print("\n6. Testing Comprehensive Security Scenario...")
        issues_found = test_suite.test_comprehensive_security_scenario()
        
        test_suite.teardown_method()
        test_suite.setup_method()
        
        print("\n7. Testing Clean Project Scenario...")
        test_suite.test_clean_project_scenario()
        
        print(f"\n🎉 All security scanning tests passed!")
        print("✅ The updated /ck:code-review command will catch security issues!")
        
    finally:
        test_suite.teardown_method()


if __name__ == "__main__":
    run_manual_tests()