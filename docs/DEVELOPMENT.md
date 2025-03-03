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

## Project Structure

```
ssh-key-manager/
├── docs/                    # Documentation
├── tests/                   # Test files
├── ssh_key_manager/        # Main package
│   ├── core/               # Core functionality
│   ├── security/           # Security features
│   ├── ui/                 # User interface
│   └── utils/              # Utilities
├── README.md               # Project overview
├── requirements.txt        # Production dependencies
└── requirements-dev.txt    # Development dependencies
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
from ssh_key_manager.core import KeyManager
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
pytest --cov=ssh_key_manager
```

### Writing Tests
```python
import pytest
from ssh_key_manager.core import KeyManager

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
pdoc --html ssh_key_manager

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