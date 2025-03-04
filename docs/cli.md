# KeyCtl CLI Documentation

## SSH Config Management

### List SSH Config
```bash
keyctl config list
```
Lists all hosts configured in your SSH config file.

### Add/Edit Host
```bash
keyctl config host <host-pattern> [--key KEY] [--user USER] [--port PORT]
```
Adds or updates a host configuration in your SSH config file.

Options:
- `--key`: Path to the identity file
- `--user`: Username for the host
- `--port`: Port number for the host

### Remove Host
```bash
keyctl config remove <host>
```
Removes a host configuration from your SSH config file.

## Key Expiration Management

### Set Key Expiration
```bash
keyctl expire set <key-name> <days>
```
Sets an expiration date for a key.

### Remove Key Expiration
```bash
keyctl expire remove <key-name>
```
Removes the expiration date for a key.

### Check Key Expirations
```bash
keyctl expire check
```
Lists all keys that are expiring soon (within 30 days).

## Repository Management

### Clone Repository
```bash
keyctl repo clone <url> [--key KEY] [--provider PROVIDER] [--path PATH] [--git-email EMAIL] [--git-name NAME]
```
Clones a repository using a specific SSH key and configures Git user settings.

Options:
- `--key`: SSH key to use
- `--provider`: Git provider (github.com, gitlab.com, bitbucket.org)
- `--path`: Local path to clone to
- `--git-email`: Configure user.email for the repository
- `--git-name`: Configure user.name for the repository

### Link Repository
```bash
keyctl repo link <repo-path> <key-name>
```
Links an SSH key to a local repository.

### List Repository Links
```bash
keyctl repo list-links [--repo REPO] [--key KEY]
```
Lists all repository-key associations.

Options:
- `--repo`: Filter by repository path
- `--key`: Filter by key name

## Error Handling

KeyCtl provides clear error messages for common issues:

1. Configuration Errors:
   - Invalid SSH config file
   - Missing or invalid key files
   - Permission issues

2. Security Errors:
   - Invalid key formats
   - Weak key types
   - Expired keys

3. Validation Errors:
   - Invalid repository URLs
   - Invalid host patterns
   - Invalid expiration dates

4. Operation Errors:
   - Failed Git operations
   - Failed SSH operations
   - Failed file operations

## Logging

KeyCtl logs operations to help with troubleshooting:

1. Log File Location:
   - Default: `~/.keyctl.log`
   - Configurable via environment variable: `KEYCTL_LOG_FILE`

2. Log Levels:
   - INFO: Normal operations
   - WARNING: Potential issues
   - ERROR: Operation failures
   - DEBUG: Detailed information

3. Log Format:
   ```
   TIMESTAMP - NAME - LEVEL - MESSAGE
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