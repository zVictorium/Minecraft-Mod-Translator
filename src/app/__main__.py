import sys
import traceback

try:
    from .commands.command_line import main
    main()
except Exception as e:
    print(f"Error in Mod Translator: {e}")
    traceback.print_exc()
    sys.exit(1)