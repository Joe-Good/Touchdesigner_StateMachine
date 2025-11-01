# start_state_machine.py
# DAT: /project1/start_state_machine (Execute DAT set to fire onStart)
# ==============================================================================
# DAT: /project1/start_state_machine (Execute DAT set to fire onStart)
# PURPOSE: Dynamically calculate and prepend the Virtual Environment path to sys.path
# to allow TouchDesigner to find external packages (e.g., 'pytransitions').
# ==============================================================================
# me - this DAT
#
# frame - the current frame
# state - True if the timeline is paused
#
# Make sure the corresponding toggle is enabled in the Execute DAT.

def onStart():
    # We rely on sys and os modules, which are part of the standard Python environment
    # available in TouchDesigner [6, 7].
    import sys
    import os

    # Debug statements are crucial for confirming execution during TD startup [8].
    debug("--- TD Startup Sequence: Executing external path setup (onStart) ---")

    # 1. Determine the project root directory.
    # 'project.folder' returns the absolute path of the directory containing the saved .toe file.
    # We assume the .venv folder is located here [4, 5].
    try:
        project_root_dir = project.folder

        # Define the relative path to site-packages within the standard venv structure.
        # Use os.path.join for cross-platform compatibility.
        relative_venv_path = os.path.join(".venv", "Lib", "site-packages")

        # Construct the full, soft-coded path
        mypath = os.path.join(project_root_dir, relative_venv_path)

        # 2. Check if the path exists and add it if necessary
        # Prepending ensures your custom packages have priority over TouchDesigner's built-in ones [9, 10].
        if mypath not in sys.path:
            sys.path = [mypath] + sys.path
            debug(f"SUCCESS: Virtual Env path added to sys.path. Path: {mypath}")
        else:
            debug(f"INFO: Virtual Env path already exists in sys.path. Path: {mypath}")

    except Exception as e:
        debug(f"ERROR calculating V-Env path: {e}")

    debug("--- TD Startup Sequence: Path setup complete ---")

    # NOTE: TouchDesigner's extension loader will proceed automatically with loading
    # extensions (like StateExtension) now that the path is correctly set [11].

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