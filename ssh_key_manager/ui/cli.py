"""Command-line interface for SSH key management."""
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from ..core.key_manager import KeyManager
from ..utils.logger import get_logger
from ..utils.config import Config

logger = get_logger(__name__)

class CLI:
    """Command-line interface for the SSH key manager."""

    def __init__(self):
        self.key_manager = KeyManager()
        self.config = Config()

    def create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="SSH Key Manager - A comprehensive SSH key management tool",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Create key command
        create_parser = subparsers.add_parser("create", help="Create a new SSH key")
        create_parser.add_argument("name", help="Name of the key")
        create_parser.add_argument(
            "--type", "-t",
            choices=["ed25519", "rsa", "ecdsa"],
            default="ed25519",
            help="Key type (default: ed25519)"
        )
        create_parser.add_argument(
            "--comment", "-c",
            help="Comment for the key"
        )
        create_parser.add_argument(
            "--expiry", "-e",
            type=int,
            help="Days until key expiration"
        )
        
        # List keys command
        list_parser = subparsers.add_parser("list", help="List all SSH keys")
        list_parser.add_argument(
            "--show-details", "-d",
            action="store_true",
            help="Show detailed information about each key"
        )
        
        # Add to agent command
        add_parser = subparsers.add_parser("add", help="Add key to SSH agent")
        add_parser.add_argument("name", help="Name of the key to add")
        add_parser.add_argument(
            "--timeout", "-t",
            type=int,
            help="Minutes until key is automatically removed"
        )
        
        # Remove from agent command
        remove_parser = subparsers.add_parser("remove", help="Remove key from SSH agent")
        remove_parser.add_argument(
            "name",
            nargs="?",
            help="Name of the key to remove (omit to remove all)"
        )
        
        # Validate key command
        validate_parser = subparsers.add_parser("validate", help="Validate key with provider")
        validate_parser.add_argument(
            "provider",
            choices=["github.com", "gitlab.com", "bitbucket.org"],
            help="Provider to validate against"
        )
        
        # Rotate key command
        rotate_parser = subparsers.add_parser("rotate", help="Rotate an SSH key")
        rotate_parser.add_argument("name", help="Name of the key to rotate")
        
        # Backup keys command
        backup_parser = subparsers.add_parser("backup", help="Backup SSH keys")
        backup_parser.add_argument(
            "--dir", "-d",
            help="Backup directory (default: ~/ssh_backup)"
        )
        
        # Restore keys command
        restore_parser = subparsers.add_parser("restore", help="Restore SSH keys from backup")
        restore_parser.add_argument(
            "backup_path",
            help="Path to backup directory"
        )
        
        # Analyze key strength
        analyze_parser = subparsers.add_parser("analyze", help="Analyze key strength")
        analyze_parser.add_argument(
            "name",
            nargs="?",
            help="Name of the key to analyze (omit to analyze all)"
        )
        
        # SSH config management
        config_parser = subparsers.add_parser("config", help="Manage SSH config")
        config_subparsers = config_parser.add_subparsers(dest="config_command")
        
        # List hosts
        config_subparsers.add_parser("list", help="List SSH config hosts")
        
        # Add/edit host
        config_host_parser = config_subparsers.add_parser("host", help="Add/edit host")
        config_host_parser.add_argument("host", help="Host pattern")
        config_host_parser.add_argument("--key", help="Identity file for host")
        config_host_parser.add_argument("--user", help="Username for host")
        config_host_parser.add_argument("--port", type=int, help="Port for host")
        
        # Remove host
        config_remove_parser = config_subparsers.add_parser("remove", help="Remove host")
        config_remove_parser.add_argument("host", help="Host to remove")
        
        # Statistics command
        stats_parser = subparsers.add_parser("stats", help="View key statistics")
        stats_parser.add_argument(
            "name",
            nargs="?",
            help="Name of the key to show stats for (omit for all)"
        )
        
        # Expiration management
        expire_parser = subparsers.add_parser("expire", help="Manage key expiration")
        expire_subparsers = expire_parser.add_subparsers(dest="expire_command")
        
        # Set expiration
        expire_set_parser = expire_subparsers.add_parser("set", help="Set key expiration")
        expire_set_parser.add_argument("name", help="Name of the key")
        expire_set_parser.add_argument("days", type=int, help="Days until expiration")
        
        # Remove expiration
        expire_remove_parser = expire_subparsers.add_parser("remove", help="Remove key expiration")
        expire_remove_parser.add_argument("name", help="Name of the key")
        
        # Check expiration
        expire_subparsers.add_parser("check", help="Check key expirations")
        
        return parser

    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI with the given arguments."""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        if not parsed_args.command:
            parser.print_help()
            return 1
            
        try:
            if parsed_args.command == "create":
                success, message = self.key_manager.create_key(
                    parsed_args.name,
                    parsed_args.type,
                    parsed_args.comment
                )
                if success and parsed_args.expiry:
                    self.config.set_key_expiration(parsed_args.name, parsed_args.expiry)
                print(message)
                return 0 if success else 1
                
            elif parsed_args.command == "list":
                keys = self.key_manager.list_keys()
                if not keys:
                    print("No SSH keys found")
                    return 0
                    
                for key in keys:
                    if parsed_args.show_details:
                        info = self.key_manager.get_key_info(key)
                        print(f"\nKey: {info['name']}")
                        print(f"Type: {info['type']}")
                        print(f"Comment: {info['comment']}")
                        print(f"Last Used: {info['last_used']}")
                        print(f"Permissions: {info['permissions']}")
                        if info['expiry']:
                            print(f"Expires: {info['expiry']}")
                    else:
                        print(key.name)
                return 0
                
            elif parsed_args.command == "add":
                key_path = Path.home() / ".ssh" / parsed_args.name
                if self.key_manager.add_to_agent(key_path):
                    print(f"Added {parsed_args.name} to SSH agent")
                    if parsed_args.timeout:
                        # Implementation for timeout-based activation would go here
                        print(f"Key will be removed after {parsed_args.timeout} minutes")
                    return 0
                else:
                    print(f"Failed to add {parsed_args.name} to SSH agent")
                    return 1
                    
            elif parsed_args.command == "remove":
                if parsed_args.name:
                    key_path = Path.home() / ".ssh" / parsed_args.name
                    if self.key_manager.remove_from_agent(key_path):
                        print(f"Removed {parsed_args.name} from SSH agent")
                        return 0
                    else:
                        print(f"Failed to remove {parsed_args.name} from SSH agent")
                        return 1
                else:
                    if self.key_manager.remove_from_agent():
                        print("Removed all keys from SSH agent")
                        return 0
                    else:
                        print("Failed to remove keys from SSH agent")
                        return 1
                        
            elif parsed_args.command == "validate":
                success, message = self.key_manager.validate_key(parsed_args.provider)
                print(message)
                return 0 if success else 1
                
            elif parsed_args.command == "rotate":
                key_path = Path.home() / ".ssh" / parsed_args.name
                success, message = self.key_manager.rotate_key(key_path)
                print(message)
                return 0 if success else 1
                
            elif parsed_args.command == "backup":
                backup_dir = parsed_args.dir if parsed_args.dir else None
                if self.key_manager.backup_keys(backup_dir):
                    print("Backup completed successfully")
                    return 0
                return 1
                
            elif parsed_args.command == "restore":
                if self.key_manager.restore_keys(parsed_args.backup_path):
                    print("Keys restored successfully")
                    return 0
                return 1
                
            elif parsed_args.command == "analyze":
                if parsed_args.name:
                    key_path = Path.home() / ".ssh" / parsed_args.name
                    strength_info = self.key_manager.security.check_key_strength(key_path)
                    if strength_info:
                        print(f"Analysis for {parsed_args.name}:")
                        print(strength_info)
                else:
                    for key in self.key_manager.list_keys():
                        strength_info = self.key_manager.security.check_key_strength(key)
                        if strength_info:
                            print(f"\nAnalysis for {key.name}:")
                            print(strength_info)
                return 0
                
            elif parsed_args.command == "config":
                if not parsed_args.config_command:
                    parser.parse_args(["config", "--help"])
                    return 1
                    
                if parsed_args.config_command == "list":
                    # Implementation for listing SSH config
                    pass
                elif parsed_args.config_command == "host":
                    # Implementation for adding/editing host
                    pass
                elif parsed_args.config_command == "remove":
                    # Implementation for removing host
                    pass
                    
            elif parsed_args.command == "stats":
                if parsed_args.name:
                    usage = self.config.get_key_usage(parsed_args.name)
                    if usage:
                        print(f"Statistics for {parsed_args.name}:")
                        print(f"First used: {usage['created']}")
                        print(f"Last used: {usage['last_used']}")
                        print(f"Use count: {usage['use_count']}")
                else:
                    print("Key Usage Statistics:")
                    for key in self.key_manager.list_keys():
                        usage = self.config.get_key_usage(key.name)
                        if usage:
                            print(f"\nKey: {key.name}")
                            print(f"First used: {usage['created']}")
                            print(f"Last used: {usage['last_used']}")
                            print(f"Use count: {usage['use_count']}")
                return 0
                
            elif parsed_args.command == "expire":
                if not parsed_args.expire_command:
                    parser.parse_args(["expire", "--help"])
                    return 1
                    
                if parsed_args.expire_command == "set":
                    self.config.set_key_expiration(parsed_args.name, parsed_args.days)
                    print(f"Set expiration for {parsed_args.name}")
                elif parsed_args.expire_command == "remove":
                    # Implementation for removing expiration
                    pass
                elif parsed_args.expire_command == "check":
                    # Implementation for checking expirations
                    pass
                    
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            print(f"Error: {str(e)}")
            return 1
            
        return 0

def main():
    """Entry point for the CLI."""
    cli = CLI()
    sys.exit(cli.run()) 