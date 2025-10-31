1. Synch Project to local > Make note of file location
2. Install Python 3.11.1 if you haven't already > Find the path to the actual installation
3. Open Project with pycharm-2025.2.4
4. PyCharm > Settings > Python > Interpreter > Add Interpreter > Add Local Interpreter
5. Generate New > Virtualenv
  - Base Python: (Paste the link to the Actual Installation path to Python on your machine)
  - Location: (Paste the File Location for the Github Project synched on local machine)
  - Un-check boxes at bottom for Inherit/make available to all
  - OK to confirm > Should take a moment to complete > Update pip/setup tools if possible > OK to exit
6. venv directory should now exist and be populated in parent folder. At this point it should NOT yet contiain "transitions" folder
7. In PyCharm > Open Terminal > Enter command: pip install transitions > Allow to complete
  - Also update pip to latest (currently 25.3)
7. Confirm "transitions" folder exists now in: \.venv\Lib\site-packages
8. In PyCharm Interpreter > Change directories to execute the following: 
\Touchdesigner_StateMachine\Python\Scripts\Debugging> python .\test_fsm_post_automation.py  
9. Key indicator of success is the console displays: 
DEBUG 5: FSM successfully bound. Current state: Attract

Next,
Open Touchdesigner project from within the directory.

Actual result:
Console displays what appears to be a working virtual environment, but StateExtensions.py clearly has some error, as none of 
the Debug Outputs are ever displayed in console. To fully test it, you can execute the same commands, and (hopefully) see
the same results:

AttributeError: 'StateExtension' object has no attribute 'is_GameMode'
python >>> op.State.initializeExtensions()
[</project1/State/StateExtension.StateExtension object at 0x0000022347894410>]
python >>> op.State.ext.StateExtension.ownerComp.path
'/project1/State'
python >>> op.State.ext.StateExtension.state
Traceback (most recent call last):
  File "<Textport>", line 1
AttributeError: 'StateExtension' object has no attribute 'state'
python >>> op.State.ext.StateExtension.ownerComp.path
'/project1/State'
python >>> 	
python >>> op.State.ext.StateExtension.start_game()
Traceback (most recent call last):
  File "<Textport>", line 1
AttributeError: 'StateExtension' object has no attribute 'start_game'
python >>> 

