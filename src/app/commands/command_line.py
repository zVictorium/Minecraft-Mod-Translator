"""
Main command-line interface for Mod Translator.
"""

import sys
import json
from argparse import ArgumentParser, Namespace, _SubParsersAction

from ..commands.translate import add_translate_arguments, handle_translate_command

def print_json(data: dict) -> None:
    """
    Print data as JSON.
    
    Args:
        data: Data to print
    """
    formatted = json.dumps(data, indent=2)
    if sys.stdout.isatty():
        print(formatted)
    else:
        sys.stdout.write(formatted)


def build_argument_parser() -> ArgumentParser:
    """
    Build the argument parser for the command-line interface.
    
    Returns:
        ArgumentParser object
    """
    parser = ArgumentParser(prog="mod-translator")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Create the CLI command (default)
    cli_parser = subparsers.add_parser("cli", help="Use traditional command-line arguments")
    add_translate_arguments(cli_parser)
    
    # Create the app command
    app_parser = subparsers.add_parser("app", help="Launch interactive form interface")
    # No arguments needed for the app interface
    
    # For backward compatibility, also add translate arguments to the main parser
    add_translate_arguments(parser)
    
    return parser


def main() -> None:
    """Main entry point for the command-line interface."""
    try:
        parser = build_argument_parser()
        
        # If no arguments provided, show help
        if len(sys.argv) == 1:
            parser.print_help()
            return
            
        args = parser.parse_args()
        
        # Handle different commands
        if getattr(args, "command", None) == "app":
            # Import app module here to avoid circular imports
            from ..commands.app import main as app_main
            app_main()
        else:
            # Default to translate command for backward compatibility
            handle_translate_command(args)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
