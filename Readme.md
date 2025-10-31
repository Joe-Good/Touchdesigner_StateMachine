# Python Virtual Environment Setup and Debugging

1. Synch Project to local > Make note of file location.

2. Install Python **3.11.1** if you haven't already > Find the path to the actual installation.

3. Open Project with **pycharm-2025.2.4**.

4. PyCharm > Settings > Python > Interpreter > Add Interpreter > Add Local Interpreter

5. Generate New > **Virtualenv**

    - Base Python: (Paste the link to the Actual Installation path to Python on your machine)
    - Location: (Paste the File Location for the Github Project synched on local machine)
    - Un-check boxes at bottom for Inherit/make available to all

6. OK to confirm > Should take a moment to complete > Update pip/setup tools if possible > OK to exit.

7. venv directory should now exist and be populated in parent folder. At this point it should NOT yet contain the "**transitions**" folder.

8. In PyCharm > Open Terminal > Enter command: **pip install transitions** > Allow to complete.
    - Also update pip to latest (currently **25.3**).

9. Confirm "**transitions**" folder exists now in: `\.venv\Lib\site-packages`

10. In PyCharm Terminal, change directories to execute the following test script:

```bash
\Touchdesigner_StateMachine\Python\Scripts\Debugging> python .\test_fsm_post_automation.py
```

11. Key indicator of success is the console displays:

```text
DEBUG 5: FSM successfully bound. Current state: Attract
Next,
Open Touchdesigner project from within the directory.
```

Actual result:
Console displays what appears to be a working virtual environment, returning:

```text
TouchDesigner Build 2023.12480 compile on Mon Sep 22 20:10:42 2025
Python 3.11.1 (heads/3.11-Derivative-dirty:82b0389147, Jan 25 2023, 22:34:27) [MSC v.1929 64 bit (AMD64)]
--- TD Startup Sequence: Executing external path setup (onStart) ---
(Debug - DAT:/project1/start_state_machine fn:onStart line:20)
SUCCESS: Virtual Env path added to sys.path. Path: D:\FileReciever\TouchDesigner\BlenderIntegration\.venv\Lib\site-packages
(Debug - DAT:/project1/start_state_machine fn:onStart line:30)
--- TD Startup Sequence: Path setup complete ---
(Debug - DAT:/project1/start_state_machine fn:onStart line:38)
python >>>
```

However, StateExtensions.py clearly has some error, as none of the Debug Outputs are ever displayed in console. To fully test it, you can execute the same commands in the TouchDesigner Textport, and (hopefully) see the same results:

```python
AttributeError: 'StateExtension' object has no attribute 'is_GameMode'

python >>> op.State.initializeExtensions()

[]

python >>> op.State.ext.StateExtension.ownerComp.path
'/project1/State'

python >>> op.State.ext.StateExtension.state

Traceback (most recent call last):
File "", line 1
AttributeError: 'StateExtension' object has no attribute 'state'

python >>> op.State.ext.StateExtension.ownerComp.path
```

# runbook
# 1. Ensure Python 3.11.1 is installed and a Virtualenv is created in PyCharm.
# 2. In PyCharm terminal, run: pip install transitions
# 3. Execute the test FSM script via the command line (adjust path as necessary): python \Touchdesigner_StateMachine\Python\Scripts\Debugging\test_fsm_post_automation.py
# 4. Open the TouchDesigner project and check the Textport for startup messages (SUCCESS: Virtual Env path added...).
# 5. In the TouchDesigner Textport, execute the extension validation commands, expecting the listed AttributeErrors or correct paths:
# op.State.initializeExtensions()
# op.State.ext.StateExtension.ownerComp.path
# op.State.ext.StateExtension.state
```