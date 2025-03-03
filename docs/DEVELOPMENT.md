# Development Guide

## Setting Up Development Environment

### Prerequisites
- Python 3.6+
- Git
- Virtual environment (recommended)

### Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ssh-key-manager.git
cd ssh-key-manager
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

## Project Structure

```
project/
├── docs/              # Documentation
├── tests/            # Test files
├── keyctl/        # Main package
│   ├── core/         # Core functionality
│   ├── security/     # Security operations
│   ├── ui/          # User interface
│   └── utils/       # Utility functions
└── setup.py         # Package configuration
```

## Coding Standards

### Style Guide
- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use docstrings for all public functions/classes

### Example
```python
from typing import List, Optional

def process_key(key_path: str, options: Optional[dict] = None) -> bool:
    """
    Process an SSH key with given options.

    Args:
        key_path: Path to the SSH key
        options: Optional processing options

    Returns:
        bool: True if processing successful, False otherwise

    Raises:
        KeyError: If key_path doesn't exist
    """
    pass
```

### Code Organization

1. **Imports**
```python
# Standard library
import os
import json
from pathlib import Path

# Third party imports
import pytest

# Local imports
from keyctl.core import KeyManager
```

2. **Class Structure**
```python
class KeyManager:
    """Manages SSH keys and their operations."""

    def __init__(self):
        self._initialize()

    def _initialize(self):
        """Internal initialization method."""
        pass

    @property
    def active_key(self):
        """Current active SSH key."""
        pass
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_key_manager.py

# Run with coverage
pytest --cov=keyctl
```

### Writing Tests
```python
import pytest
from keyctl.core import KeyManager

def test_key_creation():
    manager = KeyManager()
    result = manager.create_key("test_key")
    assert result.success
    assert result.key_path.exists()
```

### Test Categories

1. **Unit Tests**
- Test individual components
- Mock external dependencies
- Focus on edge cases

2. **Integration Tests**
- Test component interaction
- Use real file system
- Test provider integration

3. **Security Tests**
- Test permission handling
- Verify encryption
- Check key strength validation

## Documentation

### Writing Documentation

1. **Code Documentation**
- Clear docstrings
- Type hints
- Inline comments for complex logic

2. **Module Documentation**
- Module purpose
- Usage examples
- Dependencies

3. **API Documentation**
- Function signatures
- Parameter descriptions
- Return values
- Error conditions

### Building Documentation
```bash
# Generate API documentation
pdoc --html keyctl

# Build user guide
mkdocs build
```

## Git Workflow

### Branches
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `release/*`: Release preparation

### Commits
```bash
# Feature
feat: add key rotation functionality

# Bug fix
fix: correct permission checking logic

# Documentation
docs: update installation guide

# Refactoring
refactor: reorganize key management module
```

### Pull Requests
1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit PR
6. Address reviews
7. Merge to develop

## Release Process

1. **Preparation**
```bash
# Update version
bump2version minor

# Update changelog
changelog update

# Run full test suite
pytest
```

2. **Documentation**
- Update changelog
- Review documentation
- Update version numbers

3. **Release**
```bash
# Create release branch
git checkout -b release/v1.1.0

# Build distribution
python setup.py sdist bdist_wheel

# Upload to PyPI
twine upload dist/*
```

## Security Considerations

### Key Handling
- Never log sensitive data
- Secure memory handling
- Proper key cleanup

### Testing Security
- Permission tests
- Encryption validation
- Access control checks

### Code Review
- Security-focused review
- Dependency checking
- Vulnerability scanning

## Performance

### Optimization Tips
1. Use pathlib for file operations
2. Implement caching where appropriate
3. Lazy loading of resources
4. Efficient key operations

### Profiling
```bash
# Profile execution
python -m cProfile -o output.prof script.py

# Analyze results
snakeviz output.prof
```

## Troubleshooting

### Common Issues
1. Permission problems
2. Configuration errors
3. Provider integration issues

### Debugging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Detailed operation info")
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Update documentation
6. Submit pull request

## Support

- GitHub Issues
- Documentation
- Community discussions 

## Development Workflow

### 1. Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the coding standards
3. Write/update tests
4. Update documentation
5. Run the test suite
6. Submit a pull request

### 2. Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=keyctl

# Run specific test file
pytest tests/test_key_manager.py
```

### 3. Code Style

Follow PEP 8 guidelines and use provided tools:
```bash
# Check style
pylint keyctl

# Format code
black keyctl

# Check types
mypy keyctl
```

## Adding New Features

### 1. Core Functionality

When adding new core features:
1. Add the feature to appropriate module
2. Write unit tests
3. Update type hints
4. Document the API

Example:
```python
def create_key(self, name: str, key_type: str, comment: Optional[str] = None) -> Tuple[bool, str]:
    """Create a new SSH key.

    Args:
        name: Name of the key
        key_type: Type of key (ed25519, rsa, ecdsa)
        comment: Optional comment

    Returns:
        Tuple of (success, message)
    """
    # Implementation
```

### 2. Git Integration Features

When adding Git-related features:

1. **Configuration Management**
   ```python
   def configure_git_user(self, repo_path: str, email: str, name: str) -> bool:
       """Configure Git user for a repository.

       Args:
           repo_path: Path to repository
           email: User email
           name: User name

       Returns:
           Success status
       """
       # Implementation
   ```

2. **Repository Operations**
   ```python
   def clone_repository(
       self,
       url: str,
       key: str,
       path: Optional[str] = None,
       git_config: Optional[Dict[str, str]] = None
   ) -> bool:
       """Clone a repository with specific configuration.

       Args:
           url: Repository URL
           key: SSH key to use
           path: Target path
           git_config: Optional Git configuration

       Returns:
           Success status
       """
       # Implementation
   ```

### 3. Command Line Interface

When adding new commands:

1. Add argument parser:
   ```python
   def add_clone_parser(self, subparsers):
       """Add clone command parser.

       Args:
           subparsers: Subparser group
       """
       clone_parser = subparsers.add_parser("clone", help="Clone repository")
       clone_parser.add_argument("url", help="Repository URL")
       clone_parser.add_argument("--key", help="SSH key to use")
       clone_parser.add_argument("--git-email", help="Git user email")
       clone_parser.add_argument("--git-name", help="Git user name")
   ```

2. Implement command handler:
   ```python
   def handle_clone(self, args):
       """Handle clone command.

       Args:
           args: Parsed arguments
       """
       # Implementation
   ```

## Documentation

### 1. Code Documentation

- Use docstrings for all public functions
- Include type hints
- Document exceptions
- Provide usage examples

### 2. User Documentation

Update the following when adding features:
- README.md
- Command line help
- Usage examples
- Common use cases

### 3. Architecture Documentation

Document:
- Component interactions
- Data flow
- Security considerations
- Configuration details

## Testing Guidelines

### 1. Unit Tests

Write tests for:
- Core functionality
- Git operations
- Configuration management
- Error handling

Example:
```python
def test_git_config():
    """Test Git configuration management."""
    manager = KeyManager()
    result = manager.configure_git_user(
        repo_path="test_repo",
        email="test@example.com",
        name="Test User"
    )
    assert result is True
```

### 2. Integration Tests

Test:
- Git operations
- Key management
- Provider integration
- Command line interface

### 3. Security Tests

Verify:
- Permission handling
- Key isolation
- Secure storage
- Path validation

## Release Process

1. Update version:
   ```bash
   bump2version patch  # or minor/major
   ```

2. Update changelog
3. Run full test suite
4. Build distribution:
   ```bash
   python -m build
   ```

5. Create release PR
6. Tag and release

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Run tests
5. Submit pull request

See CONTRIBUTING.md for detailed guidelines. 