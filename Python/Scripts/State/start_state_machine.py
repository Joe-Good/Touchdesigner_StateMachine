# start_state_machine.py
# DAT: /project1/start_state_machine (Execute DAT set to fire onStart)

import sys


# The 'debug' function is automatically available in TD scripts [3, 4]

# ==============================================================================
# Execute DAT Callbacks
# ==============================================================================

def onStart():
    """
    Executes on TouchDesigner startup to ensure the external pytransitions library
    is accessible by modifying sys.path.
    """

    # Use the direct debug() function, which is globally available in TD scripts [3]
    debug("--- TD Startup Sequence: Executing external path setup (onStart) ---")

    try:
        # 1. Define the Virtual Environment's site-packages path using a raw string (r"...")
        # Path confirmed by user: D:\FileReciever\TouchDesigner\BlenderIntegration\.venv\Lib\site-packages
        mypath = r"D:\FileReciever\TouchDesigner\BlenderIntegration\.venv\Lib\site-packages"

        if mypath not in sys.path:
            # Prepending ensures your custom packages (like pytransitions) have priority [6, 7]
            sys.path = [mypath] + sys.path
            debug(f"SUCCESS: Virtual Env path added to sys.path. Path: {mypath}")
        else:
            debug(f"INFO: Virtual Env path already exists in sys.path. Path: {mypath}")

    except Exception as e:
        # Catch errors if path modification fails
        debug(f"CRITICAL ERROR: Failed to set sys.path for Virtual Environment. Error: {e}")

    debug("--- TD Startup Sequence: Path setup complete ---")

    # We rely on TouchDesigner's extension loader to automatically proceed with loading the StateExtension class now that the path is set [8].
    return


def onCreate():
    # If the Execute DAT is created dynamically, you may want to re-run setup here
    return

'''

Expect on TD Startup:

TouchDesigner  Build 2023.12480 compile on Mon Sep 22 20:10:42 2025
Python 3.11.1 (heads/3.11-Derivative-dirty:82b0389147, Jan 25 2023, 22:34:27) [MSC v.1929 64 bit (AMD64)]

--- TD Startup Sequence: Executing external path setup (onStart) --- 
  (Debug - DAT:/project1/start_state_machine fn:onStart line:20)
SUCCESS: Virtual Env path added to sys.path. Path: D:\FileReciever\TouchDesigner\BlenderIntegration\.venv\Lib\site-packages 
  (Debug - DAT:/project1/start_state_machine fn:onStart line:30)
--- TD Startup Sequence: Path setup complete --- 
  (Debug - DAT:/project1/start_state_machine fn:onStart line:38)
python >>> 

'''