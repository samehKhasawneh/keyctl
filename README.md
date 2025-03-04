# KeyCtl

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

### Install as a Python Package

```bash
# Clone the repository
git clone https://github.com/samehKhasawneh/keyctl.git
cd keyctl

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
```

After installation, you can use the `keyctl` command from anywhere:
```bash
# List all available commands
keyctl --help

# Create a new key
keyctl create my-key

# List all keys
keyctl list
```

## Usage

### Command Line Interface

KeyCtl provides a comprehensive command-line interface with the following commands:

```bash
# Key Management
keyctl create <key-name> [--type TYPE] [--comment COMMENT] [--expiry DAYS]
keyctl list [--show-details]
keyctl add <key-name> [--timeout MINUTES]
keyctl remove [key-name]
keyctl rotate <key-name>

# Key Validation
keyctl validate <provider>

# Security Analysis
keyctl analyze [key-name]

# Backup and Restore
keyctl backup [--dir BACKUP_DIR]
keyctl restore <backup-path>

# SSH Config Management
keyctl config list
keyctl config host <host-pattern> [--key KEY] [--user USER] [--port PORT]
keyctl config remove <host>

# Statistics and Monitoring
keyctl stats [key-name]

# Expiration Management
keyctl expire set <key-name> <days>
keyctl expire remove <key-name>
keyctl expire check

# Repository Management
keyctl repo clone <url> [--key KEY] [--provider PROVIDER] [--path PATH] [--git-email EMAIL] [--git-name NAME]
keyctl repo link <repo-path> <key-name>
keyctl repo list-links [--repo REPO] [--key KEY]
```

### Examples

1. Create a new Ed25519 key with expiration:
   ```bash
   keyctl create id_ed25519_github --comment "GitHub key" --expiry 90
   ```

2. List all keys with details:
   ```bash
   keyctl list --show-details
   ```

3. Add a key with timeout:
   ```bash
   keyctl add id_ed25519_github --timeout 60
   ```

4. Validate a key with GitHub:
   ```bash
   keyctl validate github.com
   ```

5. Analyze key strength:
   ```bash
   keyctl analyze id_ed25519_github
   ```

6. Backup all keys:
   ```bash
   keyctl backup --dir ~/ssh_keys_backup
   ```

7. Configure SSH for GitHub:
   ```bash
   keyctl config host "github.com" --key ~/.ssh/id_ed25519_github --user git
   ```

8. View key statistics:
   ```bash
   keyctl stats
   ```

9. Clone a repository with a specific key and Git configuration:
   ```bash
   # Using full URL with Git configuration
   keyctl repo clone git@github.com:username/repo.git \
     --key id_ed25519_github \
     --git-email "user@example.com" \
     --git-name "Your Name"

   # Using shorthand with Git configuration
   keyctl repo clone username/repo \
     --key id_ed25519_github \
     --git-email "user@example.com" \
     --git-name "Your Name"
   ```

10. Link a key to a repository:
    ```bash
    # Link from within the repository
    cd ~/projects/my-repo
    keyctl repo link . id_ed25519_github

    # Link by specifying path
    keyctl repo link ~/projects/my-repo id_ed25519_github
    ```

## Common Use Cases

### Managing Multiple GitHub Accounts

A common scenario is managing multiple GitHub accounts (e.g., personal and work accounts) from the same machine. Here's how to set it up:

1. Create separate keys for each account:
   ```bash
   # Personal account key
   keyctl create id_ed25519_github_personal --comment "GitHub Personal"

   # Work account key
   keyctl create id_ed25519_github_work --comment "GitHub Work"
   ```

2. Configure SSH to use different hostnames:
   ```bash
   # Configure for personal account (default)
   keyctl config host "github.com" --key ~/.ssh/id_ed25519_github_personal --user git

   # Configure for work account
   keyctl config host "github.com-work" --key ~/.ssh/id_ed25519_github_work --user git
   ```

3. Add the public keys to respective GitHub accounts:
   ```bash
   # List keys to get the public key content
   keyctl list --show-details
   ```
   Then add each public key to the corresponding GitHub account (Settings → SSH and GPG keys).

4. Clone repositories and configure Git user:
   ```bash
   # Personal project with Git configuration
   keyctl repo clone git@github.com:personal-username/project.git \
     --key id_ed25519_github_personal \
     --git-email "personal@example.com" \
     --git-name "Personal Name"

   # Work project with Git configuration
   keyctl repo clone git@github.com-work:work-username/project.git \
     --key id_ed25519_github_work \
     --git-email "work@company.com" \
     --git-name "Work Name"
   ```

   Note: The tool automatically configures repository-specific Git user settings, eliminating the need for manual `git config` commands.

5. Manage active keys:
   ```bash
   # Add work key with timeout
   keyctl add id_ed25519_github_work --timeout 60  # Active for 60 minutes

   # Or switch between keys
   keyctl add id_ed25519_github_personal
   ```

This setup ensures:
- Complete separation between accounts
- Automatic key selection based on repository URL
- Secure key management with optional timeouts
- Easy key rotation and expiration management

### Managing Repository-Specific Keys

Another common scenario is managing different SSH keys for different repositories or organizations:

1. Create keys for different contexts:
   ```bash
   # Create keys for different organizations
   keyctl create id_ed25519_org1 --comment "Organization 1"
   keyctl create id_ed25519_org2 --comment "Organization 2"
   ```

2. Clone repositories with specific keys and configurations:
   ```bash
   # Clone and configure for org1
   keyctl repo clone org1/project \
     --key id_ed25519_org1 \
     --git-email "user@org1.com" \
     --git-name "Your Name at Org1"

   # Clone and configure for org2
   keyctl repo clone org2/project \
     --key id_ed25519_org2 \
     --git-email "user@org2.com" \
     --git-name "Your Name at Org2"
   ```

3. Link existing repositories to keys:
   ```bash
   # Link repositories to their respective keys
   keyctl repo link ~/projects/org1-project id_ed25519_org1
   keyctl repo link ~/projects/org2-project id_ed25519_org2
   ```

4. View repository-key associations:
   ```bash
   # List all links
   keyctl repo list-links

   # Filter by key
   keyctl repo list-links --key id_ed25519_org1
   ```

This setup provides:
- Automatic key selection when cloning repositories
- Clear mapping between repositories and keys
- Easy key rotation for specific repositories
- Improved security through key isolation

### Key Rotation and Expiration

Managing key rotation and expiration is crucial for security:

1. Set up keys with expiration:
   ```bash
   # Create a key that expires in 90 days
   keyctl create id_ed25519_project --comment "Project Key" --expiry 90

   # Check expiration status
   keyctl expire check
   ```

2. Rotate keys before expiration:
   ```bash
   # Rotate the key (automatically updates configs and backups old key)
   keyctl rotate id_ed25519_project

   # Verify the new key
   keyctl validate github.com
   ```

3. Manage temporary access:
   ```bash
   # Add key with 1-hour timeout
   keyctl add id_ed25519_project --timeout 60

   # Remove key after use
   keyctl remove id_ed25519_project
   ```

### Security Monitoring and Maintenance

Regular security checks and maintenance:

1. Analyze key strength:
   ```bash
   # Check all keys
   keyctl analyze

   # Check specific key
   keyctl analyze id_ed25519_project
   ```

2. Track key usage:
   ```bash
   # View usage statistics
   keyctl stats

   # Check specific key stats
   keyctl stats id_ed25519_project
   ```

3. Regular backups:
   ```bash
   # Create dated backup
   keyctl backup --dir ~/ssh_backups/$(date +%Y%m%d)

   # Restore from backup if needed
   keyctl restore ~/ssh_backups/20240101
   ```

### SSH Config Management

Efficiently manage SSH configurations:

1. Set up host configurations:
   ```bash
   # Configure for specific host
   keyctl config host "dev.example.com" --key ~/.ssh/id_ed25519_dev --user admin --port 2222

   # Configure for wildcard domain
   keyctl config host "*.staging.example.com" --key ~/.ssh/id_ed25519_staging --user deploy
   ```

2. View and manage configurations:
   ```bash
   # List all configurations
   keyctl config list

   # Remove outdated config
   keyctl config remove "old.example.com"
   ```

### Provider Integration

Working with different Git providers:

1. Set up provider-specific keys:
   ```bash
   # Create keys for different providers
   keyctl create id_ed25519_github --comment "GitHub"
   keyctl create id_ed25519_gitlab --comment "GitLab"
   keyctl create id_ed25519_bitbucket --comment "Bitbucket"
   ```

2. Validate keys with providers:
   ```bash
   # Validate with each provider
   keyctl validate github.com
   keyctl validate gitlab.com
   keyctl validate bitbucket.org
   ```

3. Clone repositories:
   ```bash
   # Clone using provider shorthand
   keyctl repo clone username/repo --key id_ed25519_github --provider github.com

   # Clone GitLab project
   keyctl repo clone username/repo --key id_ed25519_gitlab --provider gitlab.com
   ```

### Team Collaboration

Managing keys in a team environment:

1. Set up project-specific keys:
   ```bash
   # Create key for team project
   keyctl create id_ed25519_team_project --comment "Team Project" --expiry 180

   # Link to project repositories
   keyctl repo link ~/projects/team-repo id_ed25519_team_project
   ```

2. Clone and configure team repositories:
   ```bash
   # Clone team repository with configuration
   keyctl repo clone team/project \
     --key id_ed25519_team_project \
     --git-email "your.name@team.com" \
     --git-name "Your Full Name"
   ```

3. Share public keys:
   ```bash
   # List key details for sharing
   keyctl list --show-details
   ```

4. Track team key usage:
   ```bash
   # Monitor key usage
   keyctl stats id_ed25519_team_project

   # Check key expiration status
   keyctl expire check
   ```

5. Maintain security:
   ```bash
   # Regular strength analysis
   keyctl analyze id_ed25519_team_project

   # Rotate team keys
   keyctl rotate id_ed25519_team_project
   ```

These use cases demonstrate:
- Complete key lifecycle management
- Security best practices
- Team collaboration workflows
- Integration with various providers
- Efficient repository management with automatic Git configuration
- Regular maintenance procedures

## Project Structure

```
keyctl/
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

KeyCtl stores its configuration in `~/.ssh/.keyctl/`:
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
pylint keyctl

# Format code
black keyctl
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

KeyCtl Contributors

## Acknowledgments

- OpenSSH project
- Python cryptography community
- Git hosting providers for their SSH implementations