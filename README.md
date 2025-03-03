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

The SSH Key Manager provides a comprehensive command-line interface with the following commands:

```bash
# Key Management
ssh-key-manager create <key-name> [--type TYPE] [--comment COMMENT] [--expiry DAYS]
ssh-key-manager list [--show-details]
ssh-key-manager add <key-name> [--timeout MINUTES]
ssh-key-manager remove [key-name]
ssh-key-manager rotate <key-name>

# Key Validation
ssh-key-manager validate <provider>

# Security Analysis
ssh-key-manager analyze [key-name]

# Backup and Restore
ssh-key-manager backup [--dir BACKUP_DIR]
ssh-key-manager restore <backup-path>

# SSH Config Management
ssh-key-manager config list
ssh-key-manager config host <host-pattern> [--key KEY] [--user USER] [--port PORT]
ssh-key-manager config remove <host>

# Statistics and Monitoring
ssh-key-manager stats [key-name]

# Expiration Management
ssh-key-manager expire set <key-name> <days>
ssh-key-manager expire remove <key-name>
ssh-key-manager expire check

# Repository Management
ssh-key-manager repo clone <url> [--key KEY] [--provider PROVIDER] [--path PATH]
ssh-key-manager repo link <repo-path> <key-name>
ssh-key-manager repo list-links [--repo REPO] [--key KEY]
```

### Examples

1. Create a new Ed25519 key with expiration:
   ```bash
   ssh-key-manager create id_ed25519_github --comment "GitHub key" --expiry 90
   ```

2. List all keys with details:
   ```bash
   ssh-key-manager list --show-details
   ```

3. Add a key with timeout:
   ```bash
   ssh-key-manager add id_ed25519_github --timeout 60
   ```

4. Validate a key with GitHub:
   ```bash
   ssh-key-manager validate github.com
   ```

5. Analyze key strength:
   ```bash
   ssh-key-manager analyze id_ed25519_github
   ```

6. Backup all keys:
   ```bash
   ssh-key-manager backup --dir ~/ssh_keys_backup
   ```

7. Configure SSH for GitHub:
   ```bash
   ssh-key-manager config host "github.com" --key ~/.ssh/id_ed25519_github --user git
   ```

8. View key statistics:
   ```bash
   ssh-key-manager stats
   ```

9. Clone a repository with a specific key:
   ```bash
   # Using full URL
   ssh-key-manager repo clone git@github.com:username/repo.git --key id_ed25519_github

   # Using shorthand (automatically expands to github.com)
   ssh-key-manager repo clone username/repo --key id_ed25519_github
   ```

10. Link a key to a repository:
    ```bash
    # Link from within the repository
    cd ~/projects/my-repo
    ssh-key-manager repo link . id_ed25519_github

    # Link by specifying path
    ssh-key-manager repo link ~/projects/my-repo id_ed25519_github
    ```

## Common Use Cases

### Managing Multiple GitHub Accounts

A common scenario is managing multiple GitHub accounts (e.g., personal and work accounts) from the same machine. Here's how to set it up:

1. Create separate keys for each account:
   ```bash
   # Personal account key
   ssh-key-manager create id_ed25519_github_personal --comment "GitHub Personal"

   # Work account key
   ssh-key-manager create id_ed25519_github_work --comment "GitHub Work"
   ```

2. Configure SSH to use different hostnames:
   ```bash
   # Configure for personal account (default)
   ssh-key-manager config host "github.com" --key ~/.ssh/id_ed25519_github_personal --user git

   # Configure for work account
   ssh-key-manager config host "github.com-work" --key ~/.ssh/id_ed25519_github_work --user git
   ```

3. Add the public keys to respective GitHub accounts:
   ```bash
   # List keys to get the public key content
   ssh-key-manager list --show-details
   ```
   Then add each public key to the corresponding GitHub account (Settings → SSH and GPG keys).

4. Clone repositories using the appropriate hostname:
   ```bash
   # Personal project
   git clone git@github.com:personal-username/project.git

   # Work project
   git clone git@github.com-work:work-username/project.git
   ```

5. Manage active keys:
   ```bash
   # Add work key with timeout
   ssh-key-manager add id_ed25519_github_work --timeout 60  # Active for 60 minutes

   # Or switch between keys
   ssh-key-manager add id_ed25519_github_personal
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
   ssh-key-manager create id_ed25519_org1 --comment "Organization 1"
   ssh-key-manager create id_ed25519_org2 --comment "Organization 2"
   ```

2. Clone repositories with specific keys:
   ```bash
   # Clone using org1's key
   ssh-key-manager repo clone org1/project --key id_ed25519_org1

   # Clone using org2's key
   ssh-key-manager repo clone org2/project --key id_ed25519_org2
   ```

3. Link existing repositories to keys:
   ```bash
   # Link repositories to their respective keys
   ssh-key-manager repo link ~/projects/org1-project id_ed25519_org1
   ssh-key-manager repo link ~/projects/org2-project id_ed25519_org2
   ```

4. View repository-key associations:
   ```bash
   # List all links
   ssh-key-manager repo list-links

   # Filter by key
   ssh-key-manager repo list-links --key id_ed25519_org1
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
   ssh-key-manager create id_ed25519_project --comment "Project Key" --expiry 90

   # Check expiration status
   ssh-key-manager expire check
   ```

2. Rotate keys before expiration:
   ```bash
   # Rotate the key (automatically updates configs and backups old key)
   ssh-key-manager rotate id_ed25519_project

   # Verify the new key
   ssh-key-manager validate github.com
   ```

3. Manage temporary access:
   ```bash
   # Add key with 1-hour timeout
   ssh-key-manager add id_ed25519_project --timeout 60

   # Remove key after use
   ssh-key-manager remove id_ed25519_project
   ```

### Security Monitoring and Maintenance

Regular security checks and maintenance:

1. Analyze key strength:
   ```bash
   # Check all keys
   ssh-key-manager analyze

   # Check specific key
   ssh-key-manager analyze id_ed25519_project
   ```

2. Track key usage:
   ```bash
   # View usage statistics
   ssh-key-manager stats

   # Check specific key stats
   ssh-key-manager stats id_ed25519_project
   ```

3. Regular backups:
   ```bash
   # Create dated backup
   ssh-key-manager backup --dir ~/ssh_backups/$(date +%Y%m%d)

   # Restore from backup if needed
   ssh-key-manager restore ~/ssh_backups/20240101
   ```

### SSH Config Management

Efficiently manage SSH configurations:

1. Set up host configurations:
   ```bash
   # Configure for specific host
   ssh-key-manager config host "dev.example.com" --key ~/.ssh/id_ed25519_dev --user admin --port 2222

   # Configure for wildcard domain
   ssh-key-manager config host "*.staging.example.com" --key ~/.ssh/id_ed25519_staging --user deploy
   ```

2. View and manage configurations:
   ```bash
   # List all configurations
   ssh-key-manager config list

   # Remove outdated config
   ssh-key-manager config remove "old.example.com"
   ```

### Provider Integration

Working with different Git providers:

1. Set up provider-specific keys:
   ```bash
   # Create keys for different providers
   ssh-key-manager create id_ed25519_github --comment "GitHub"
   ssh-key-manager create id_ed25519_gitlab --comment "GitLab"
   ssh-key-manager create id_ed25519_bitbucket --comment "Bitbucket"
   ```

2. Validate keys with providers:
   ```bash
   # Validate with each provider
   ssh-key-manager validate github.com
   ssh-key-manager validate gitlab.com
   ssh-key-manager validate bitbucket.org
   ```

3. Clone repositories:
   ```bash
   # Clone using provider shorthand
   ssh-key-manager repo clone username/repo --key id_ed25519_github --provider github.com

   # Clone GitLab project
   ssh-key-manager repo clone username/repo --key id_ed25519_gitlab --provider gitlab.com
   ```

### Team Collaboration

Managing keys in a team environment:

1. Set up project-specific keys:
   ```bash
   # Create key for team project
   ssh-key-manager create id_ed25519_team_project --comment "Team Project" --expiry 180

   # Link to project repositories
   ssh-key-manager repo link ~/projects/team-repo id_ed25519_team_project
   ```

2. Share public keys:
   ```bash
   # List key details for sharing
   ssh-key-manager list --show-details
   ```

3. Track team key usage:
   ```bash
   # Monitor key usage
   ssh-key-manager stats id_ed25519_team_project

   # Check key expiration status
   ssh-key-manager expire check
   ```

4. Maintain security:
   ```bash
   # Regular strength analysis
   ssh-key-manager analyze id_ed25519_team_project

   # Rotate team keys
   ssh-key-manager rotate id_ed25519_team_project
   ```

These use cases demonstrate:
- Complete key lifecycle management
- Security best practices
- Team collaboration workflows
- Integration with various providers
- Efficient repository management
- Regular maintenance procedures

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