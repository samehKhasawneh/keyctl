# SSH Key Manager

A comprehensive SSH key management tool that helps you create, manage, and maintain your SSH keys securely.

## Features

- **Key Management**
  - Create new SSH keys with secure defaults
  - List existing SSH keys with detailed information
  - Rotate SSH keys while preserving metadata
  - Add and remove keys from SSH agent
  - Secure key deletion with overwrite protection

- **Security**
  - Automatic permission management for keys and directories
  - Key strength analysis and recommendations
  - Secure storage of configuration and usage data
  - Path traversal protection
  - Validation of key names and formats

- **Provider Integration**
  - Validate keys with common Git providers:
    - GitHub
    - GitLab
    - Bitbucket
  - Custom provider support

- **Configuration Management**
  - Persistent configuration storage
  - Key usage statistics tracking
  - Key expiration management
  - Provider-specific settings

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ssh-key-manager.git
   cd ssh-key-manager
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

For development installation with additional tools:
```bash
pip install -r requirements-dev.txt
```

## Usage

### Command Line Interface

The SSH Key Manager provides a command-line interface with the following commands:

```bash
# Create a new SSH key
ssh-key-manager create <key-name> [--type TYPE] [--comment COMMENT]

# List all SSH keys
ssh-key-manager list [--show-details]

# Add a key to the SSH agent
ssh-key-manager add <key-name>

# Remove a key from the SSH agent
ssh-key-manager remove [key-name]

# Validate a key with a provider
ssh-key-manager validate <provider>

# Rotate an existing key
ssh-key-manager rotate <key-name>
```

### Examples

1. Create a new Ed25519 key:
   ```bash
   ssh-key-manager create id_ed25519_github --comment "GitHub key"
   ```

2. List all keys with details:
   ```bash
   ssh-key-manager list --show-details
   ```

3. Validate a key with GitHub:
   ```bash
   ssh-key-manager validate github.com
   ```

## Project Structure

```
ssh_key_manager/
├── core/               # Core functionality
│   ├── __init__.py
│   └── key_manager.py
├── security/          # Security operations
│   ├── __init__.py
│   └── key_security.py
├── ui/                # User interface
│   ├── __init__.py
│   └── cli.py
├── utils/            # Utility functions
│   ├── __init__.py
│   ├── config.py
│   └── logger.py
└── __init__.py
```

## Configuration

The SSH Key Manager stores its configuration in `~/.ssh/.keyctl/`:
- `config.json`: General configuration and provider settings
- `usage.json`: Key usage statistics and metadata

## Development

### Requirements

- Python 3.6 or higher
- Development dependencies listed in `requirements-dev.txt`

### Setting Up Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

### Running Tests

```bash
pytest
```

### Code Style

The project follows PEP 8 guidelines. To check and format code:

```bash
# Check code style
pylint ssh_key_manager

# Format code
black ssh_key_manager
```

## Security Considerations

- Private keys are stored with 600 permissions (user read/write only)
- Public keys are stored with 644 permissions (user read/write, others read)
- SSH directory is maintained with 700 permissions (user access only)
- Configuration files are stored with 600 permissions
- Secure key deletion with data overwriting
- Protection against path traversal attacks
- Regular key rotation recommendations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code style compliance
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

SSH Key Manager Contributors

## Acknowledgments

- OpenSSH project
- Python cryptography community
- Git hosting providers for their SSH implementations