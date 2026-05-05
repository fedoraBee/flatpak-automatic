# 🧪 Testing Procedures & Quality Standards

Flatpak Automatic follows a shift-left testing strategy to ensure reliability
and maintainability. This document outlines the testing architecture,
procedures, and enforcement policies.

## 🏗 Testing Architecture

The test suite is powered by **Pytest** and is structured to provide exhaustive
coverage while maintaining strict isolation from the host OS.

- **Unit Tests (`tests/test_*.py`)**: Focused on individual components (config,
  notifiers, logic). These use extensive mocking to avoid side effects.
- **Integration Tests (`tests/integration_test_*.py`)**: Verify that components
  work together (e.g., D-Bus communication, CLI routing).
- **Coverage Enforcement**: Enforced via `pytest-cov`. A minimum threshold of
  **85%** is mandatory for all PRs.

## 🛠 Quality Enforcement

We use `pytest.ini` to define our quality gates. Every PR must pass all tests
and meet the coverage threshold.

### Coverage Enforcement

A minimum threshold of **85%** is mandatory. This is enforced via `pytest-cov`
and configured in `pytest.ini`:

```ini
[pytest]
addopts =
    --cov=flatpak_automatic
    --cov-fail-under=85
```

If coverage falls below 85%, the test suite will exit with a non-zero code,
failing CI.

## 📋 Testing Procedures

To maintain high quality, follow these procedures when developing new features
or fixing bugs:

### 1. Test-Driven Development (TDD) Recommended

- For bugs: Write a reproduction test case first.
- For features: Define the expected behavior in a unit test before
  implementation.

### 2. Unit Testing (Target: >90% of logic)

- Store in `tests/test_*.py`.
- Mock all external dependencies (D-Bus, Filesystem, Network).
- Focus on small, isolated pieces of logic (e.g., `logging_utils.py`,
  `config.py`).

### 3. Integration Testing

- Store in `tests/integration_test_*.py`.
- Test interactions between components.
- Mock only at the system boundaries (e.g., mocking the `flatpak` binary
  response).

### 4. Running the Suite

The most efficient way to run tests locally is using the following command:

```bash
pytest
```

This will automatically:

1. Use `src/` as the python path.
2. Run all tests in `tests/`.
3. Generate a terminal coverage report.
4. Generate an HTML report in `htmlcov/`.

### 5. Analyzing Coverage

If coverage is below the threshold:

1. Open `htmlcov/index.html` in your browser.
2. Click on the file with low coverage.
3. Untested lines are highlighted in red.
4. Add tests targeting those specific branches.

## 🔍 Mocking Strategy (System Isolation)

To ensure tests run fast and safely on any environment, we strictly mock all
system-level calls:

### 1. Subprocess Mocking

We use `unittest.mock.patch` to intercept `subprocess.run` and
`subprocess.Popen`.

```python
@patch("subprocess.run")
def test_command_execution(mock_run):
    mock_run.return_value = MagicMock(stdout="Output", returncode=0)
    # ... test logic ...
```

### 2. D-Bus Mocking

D-Bus is mocked globally in `tests/conftest.py` to prevent tests from attempting
to connect to the actual system bus.

### 3. Filesystem Mocking

We prefer using `pathlib.Path` and `unittest.mock.mock_open` or temporary
directories (`tmp_path` fixture) for file operations.

## 🚀 Running Tests

### Standard Execution

```bash
PYTHONPATH=src pytest
```

### Low Memory Environments

If running tests consumes too much RAM or freezes your system, try disabling
coverage:

```bash
PYTHONPATH=src pytest --no-cov
```

By default, tests run sequentially. If you have `pytest-xdist` installed and
want to run them in parallel, you can use `-n auto`.

### With Coverage Report (HTML)

```bash
PYTHONPATH=src pytest --cov-report=html
```

The report will be available at `htmlcov/index.html`.

## 🛡 Type Checking (Mypy)

To prevent resource exhaustion, the `tests/` directory is excluded from the
default Mypy check in `.mypy.ini`. To run type checks on the source code:

```bash
mypy src/
```

If you must check the tests and have enough RAM:

```bash
mypy tests/
```

## 📈 Improving Coverage

If you add new features, you **must** add corresponding tests. Check the
"Missing" column in the coverage output to identify untested lines of code.

---

_This documentation is maintained by the QA team. Ensure it remains in sync with
the project's evolving standards._
