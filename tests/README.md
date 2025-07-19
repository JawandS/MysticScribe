# MysticScribe Tests

This directory contains tests for the MysticScribe AI-powered chapter writing system.

## Test Structure

### Core Test Files

- **`test_main.py`** - Comprehensive standalone test runner that works without external dependencies
- **`conftest.py`** - Pytest configuration and shared fixtures (optional)
- **`test_chapter_manager.py`** - Tests for chapter management functionality
- **`test_knowledge_manager.py`** - Tests for knowledge base management
- **`test_workflows.py`** - Tests for workflow execution
- **`test_validation.py`** - Tests for content validation
- **`setup_check.py`** - System setup verification script

## Running Tests

### Option 1: Using the Test Runner (Recommended)
```bash
python run_tests.py
```
This automatically detects whether pytest is available and runs the appropriate test suite.

### Option 2: Standalone Tests
```bash
python tests/test_main.py
```
Runs comprehensive tests without requiring pytest or other dependencies.

### Option 3: With Pytest (if installed)
```bash
pytest tests/ -v
```

### Option 4: Setup Check
```bash
python tests/setup_check.py
```
Verifies system configuration and dependencies.

## Test Features

- **Dependency-Free**: Main tests work without pytest or external libraries
- **Automatic Cleanup**: Tests use temporary directories and clean up after themselves
- **Comprehensive Coverage**: Tests all core functionality including:
  - Chapter management (save/load/info)
  - Knowledge base operations
  - Content validation
  - Workflow execution
  - Style analysis tools (if available)
  - Utility functions

## Test Environment

Tests automatically create temporary project directories with:
- `/chapters/` - Sample chapter files
- `/knowledge/` - Sample knowledge base files
- `/outlines/` - Chapter outline directory
- `/styles/` - Style guide directory

## CI/CD Integration

The test suite is designed to work in continuous integration environments:
- No external dependencies required for basic functionality
- Exit codes: 0 = success, 1 = failure
- Detailed output for debugging

## Development

When adding new tests:

1. Add pytest-based tests to appropriate `test_*.py` files
2. Add fallback standalone tests to `test_main.py`
3. Use the fixtures in `conftest.py` for pytest tests
4. Ensure tests clean up temporary resources

## Markers

When using pytest, tests support these markers:
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow-running tests

Run specific test types:
```bash
pytest -m "not slow"  # Skip slow tests
pytest -m integration  # Run only integration tests
```
