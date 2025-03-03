"""Command-line interface for SSH key management."""
import argparse
import sys
from pathlib import Path
from typing import List, Optional

from ..core.key_manager import KeyManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class CLI:
    """Command-line interface for the SSH key manager."""

    def __init__(self):
        self.key_manager = KeyManager()

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
                
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            print(f"Error: {str(e)}")
            return 1
            
        return 0

def main():
    """Entry point for the CLI."""
    cli = CLI()
    sys.exit(cli.run()) 