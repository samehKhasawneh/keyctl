# Command Line Interface

## Repository Management

### Clone Repository
```bash
ssh-key-manager repo clone <url> [options]
```

Clone a Git repository using a specific SSH key and configure Git user settings.

Options:
- `--key KEY`: SSH key to use for cloning
- `--provider PROVIDER`: Git provider (default: github.com)
- `--path PATH`: Local path to clone to
- `--git-email EMAIL`: Configure user.email for the repository
- `--git-name NAME`: Configure user.name for the repository

The command supports:
- Full SSH URLs (e.g., git@github.com:username/repo.git)
- Shorthand notation (e.g., username/repo)
- Automatic Git user configuration
- Repository-specific settings

Examples:
```bash
# Clone with full URL and Git configuration
ssh-key-manager repo clone git@github.com:username/repo.git \
  --key id_ed25519_github \
  --git-email "user@example.com" \
  --git-name "Your Name"

# Clone with shorthand and Git configuration
ssh-key-manager repo clone username/repo \
  --key id_ed25519_github \
  --git-email "user@example.com" \
  --git-name "Your Name"

# Clone to specific path
ssh-key-manager repo clone username/repo \
  --key id_ed25519_github \
  --path ~/projects/repo \
  --git-email "user@example.com" \
  --git-name "Your Name"
```

### Link Repository
```bash
ssh-key-manager repo link <repo-path> <key-name>
```

Link an SSH key to a local repository for automatic key selection.

Examples:
```bash
# Link from repository directory
cd ~/projects/repo
ssh-key-manager repo link . id_ed25519_github

# Link by specifying path
ssh-key-manager repo link ~/projects/repo id_ed25519_github
```

### List Repository Links
```bash
ssh-key-manager repo list-links [options]
```

List repository-key associations.

Options:
- `--repo REPO`: Filter by repository path
- `--key KEY`: Filter by key name

Examples:
```bash
# List all links
ssh-key-manager repo list-links

# Filter by key
ssh-key-manager repo list-links --key id_ed25519_github

# Filter by repository
ssh-key-manager repo list-links --repo ~/projects/repo
```

## Best Practices

1. **Git Configuration**
   - Use `--git-email` and `--git-name` when cloning to ensure correct commit attribution
   - Set different Git configurations for different contexts (personal/work)
   - Use repository-specific settings for team projects

2. **Key Management**
   - Link keys to repositories for automatic selection
   - Use descriptive key names and comments
   - Rotate keys regularly
   - Set appropriate expiration times

3. **Security**
   - Use different keys for different providers/organizations
   - Remove keys from agent when not in use
   - Regularly check key strength and expiration
   - Maintain secure backups 