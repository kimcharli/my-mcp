#!/usr/bin/env python3
"""
Test runner script that makes it easy to run tests with proper configuration.
"""
import os
import sys
import subprocess

def run_tests():
    """Run pytest with coverage reporting."""
    # Change to the directory of this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Default arguments
    args = [
        "pytest",
        "-xvs",  # -x: exit on first failure, -v: verbose, -s: show print statements
        "--cov=.",  # measure coverage for all files
        "--cov-report=term",  # show coverage in terminal
        "--cov-report=html:coverage_html",  # generate HTML report
    ]
    
    # Add any additional arguments passed to this script
    args.extend(sys.argv[1:])
    
    # Run pytest with the arguments
    result = subprocess.run(args)
    
    # Return the exit code
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())