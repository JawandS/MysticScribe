#!/usr/bin/env python3
"""
Test runner for MysticScribe - supports both pytest and standalone execution.
"""

import sys
import subprocess
from pathlib import Path

def run_with_pytest():
    """Run tests with pytest if available."""
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short"
        ], cwd=Path(__file__).parent)
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def run_standalone():
    """Run standalone test runner."""
    try:
        result = subprocess.run([
            sys.executable, 
            "tests/test_main.py"
        ], cwd=Path(__file__).parent)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def main():
    """Main test runner."""
    print("🧪 MysticScribe Test Runner")
    print("=" * 40)
    
    # Try pytest first
    print("Trying pytest...")
    if run_with_pytest():
        print("✅ Tests completed with pytest")
        return 0
    
    print("⚠️  pytest not available, using standalone runner...")
    
    # Fall back to standalone
    if run_standalone():
        print("✅ Tests completed with standalone runner")
        return 0
    else:
        print("❌ Tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
