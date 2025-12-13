#!/usr/bin/env python3
"""
Comprehensive test runner for AI Accountant API.

Creates test database, runs all tests, and reports results.

Usage:
    python scripts/run_tests.py              # Run all tests
    python scripts/run_tests.py --skip-ai    # Skip AI tests
    python scripts/run_tests.py --verbose    # Verbose output
"""
import subprocess
import sys
import argparse
from pathlib import Path


def check_test_database():
    """Check if test database exists."""
    print("📊 Checking test database...")
    
    result = subprocess.run(
        ["psql", "-U", "postgres", "-lqt"],
        capture_output=True,
        text=True
    )
    
    if "midas_test_db" not in result.stdout:
        print("⚠️  Test database 'midas_test_db' not found!")
        print("\nCreate it with:")
        print("   createdb midas_test_db")
        print("\nOr run:")
        print("   psql -U postgres -c 'CREATE DATABASE midas_test_db;'")
        return False
    
    print("✅ Test database found")
    return True


def run_tests(skip_ai: bool = False, verbose: bool = False):
    """Run pytest with appropriate options."""
    print("\n" + "="*60)
    print("🧪 Running AI Accountant API Tests")
    print("="*60 + "\n")
    
    # Build pytest command
    cmd = ["pytest", "tests/"]
    
    if skip_ai:
        cmd.extend(["-m", "not ai"])
        print("ℹ️  Skipping AI tests (no OpenAI API calls)")
    
    if verbose:
        cmd.append("-vv")
    
    # Add coverage if available
    try:
        import pytest_cov
        cmd.extend(["--cov=api", "--cov-report=term-missing"])
    except ImportError:
        pass
    
    print(f"Running: {' '.join(cmd)}\n")
    
    # Run tests
    result = subprocess.run(cmd)
    
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run AI Accountant API tests")
    parser.add_argument("--skip-ai", action="store_true", help="Skip AI tests (no OpenAI calls)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--no-db-check", action="store_true", help="Skip database check")
    
    args = parser.parse_args()
    
    # Check test database
    if not args.no_db_check:
        if not check_test_database():
            sys.exit(1)
    
    # Run tests
    exit_code = run_tests(skip_ai=args.skip_ai, verbose=args.verbose)
    
    print("\n" + "="*60)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. See output above.")
    print("="*60)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
