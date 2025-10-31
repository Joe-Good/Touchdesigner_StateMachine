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