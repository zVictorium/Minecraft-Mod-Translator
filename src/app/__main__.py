import sys
import os
import traceback

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(os.path.dirname(current_dir))  # .../src
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from app.commands.command_line import main
    main()
except Exception as e:
    print(f"Error in Mod Translator: {e}")
    traceback.print_exc()
    sys.exit(1)
