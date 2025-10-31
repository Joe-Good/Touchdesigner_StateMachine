# StateExtension.py
from transitions import Machine
import sys


# Note: TouchDesigner built-in objects like 'op', 'absTime', and 'debug' are
# automatically available without explicit import in DAT scripts.

class StateExtension:
    """
    Maestro FSM (TestStateModel) controlling high-level application flow for
    the Equilateral Expedition kinetic sculpture.

    CRITICAL FIX: FSM Machine instantiation is deferred to onInitTD to 
    prevent the silent initialization failure during Extension bootstrapping.
    """

    def __init__(self, ownerComp):
        """
        Initializes essential attributes only, minimizing logic that might 
        fail during the tight TD component creation window.
        """
        self.ownerComp = ownerComp

        # Initialize attributes that will eventually hold state data
        self.animation_frame_offset = 0
        self.td_system_frame_start = 0

        # Initialize machine object to None
        self.machine = None

        debug(f"StateExtension: Basic attributes initialized in __init__.")

    def onInitTD(self):
        """
        TouchDesigner Initialization Hook.
        This runs automatically at the end of the frame the extension initialized.
        This is the safe place to execute complex external library setups like 
        pytransitions which dynamically decorate the model with attributes like '.state'.
        """

        # --- 1. TD-Dependent Setup (Now Safe) ---
        # Accessing TD time objects like absTime.frame is now safe.
        self.td_system_frame_start = absTime.frame
        debug(f"StateExtension: Deferred TD Initialization (onInitTD) started on Frame: {self.td_system_frame_start}")

        # --- 2. PyTransitions Machine Setup ---

        # Define application states (Hierarchy/POST sequence checks)
        states = [
            'Attract', 'PowerOff', 'WarmUpCycle', 'ExtensionMode',
            'RotationCheck', 'LinearCheck', 'TouchDesignerInteractiveChecks',
            'FaultMode', 'Attract_Intervention', 'GameMode'
        ]

        # Define transitions (Mandatory Power On Self Test (POST) flow and Fault handling)
        transitions = [
            {'trigger': 'power_on', 'source': 'Attract', 'dest': 'WarmUpCycle'},
            {'trigger': 'warmup_complete', 'source': 'WarmUpCycle', 'dest': 'ExtensionMode'},
            {'trigger': 'extension_check_complete', 'source': 'ExtensionMode', 'dest': 'RotationCheck'},
            {'trigger': 'rotation_check_complete', 'source': 'RotationCheck', 'dest': 'LinearCheck'},

            # Linear Check Success/Failure Paths
            {'trigger': 'linear_check_complete', 'source': 'LinearCheck', 'dest': 'TouchDesignerInteractiveChecks'},
            {'trigger': 'linear_check_failure', 'source': 'LinearCheck', 'dest': 'FaultMode'},

            # Curator Intervention for Fault Mode
            {'trigger': 'resume_from_fault', 'source': 'FaultMode', 'dest': 'Attract',
             'before': 'set_box_locked_at_max'},

            # Final POST stage complete
            {'trigger': 'post_interactive_complete', 'source': 'TouchDesignerInteractiveChecks', 'dest': 'Attract'},

            # Game Mode Interaction
            {'trigger': 'start_interaction', 'source': 'Attract', 'dest': 'GameMode'},
            {'trigger': 'start_interaction', 'source': 'GameMode', 'dest': 'GameMode', 'before': 'debug_reflexive'},
        ]

        # Initialize the Hierarchical State Machine (HSM), binding dynamic methods/attributes to 'self'.
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='Attract')

        debug(f"StateExtension: FSM Machine object created successfully in onInitTD. Initial state: {self.state}")

        return

    # --- Example Callback and Utility Methods ---

    def set_box_locked_at_max(self):
        """Action required to resume from FaultMode: locking the linear actuator."""
        debug("CALLBACK: Curator action detected. Locking Linear Actuator at Max.")

    def on_enter_GameMode(self):
        """Callback that fires when entering the GameMode state."""
        debug("CALLBACK: Entering GameMode. Prepare for interactive alignment.")

    def debug_reflexive(self):
        """For reflexive transition debugging (GameMode -> GameMode)."""
        debug("CALLBACK: Reflexive interaction trigger received in GameMode.")

    # Utility method required for state checking (dynamically added by pytransitions)
    def is_GameMode(self):
        return self.state == 'GameMode'


# runbook
# 1. Ensure the pytransitions library is installed in your V-Env and the path is added to sys.path (as confirmed in your trace from the Execute DAT onStart).
# 2. In your TouchDesigner network, ensure the Base COMP named 'State' contains a Text DAT named 'StateExtension'.
# 3. Paste the entire content of this file into the 'StateExtension' DAT.
# 4. On the 'State' COMP's Extension Parameters page, set the following clean values:
#    a. Extension Object: StateExtension(me) 
#    b. Extension Name: (Leave Blank, access via .ext.StateExtension)
#    c. Promote Extension: Check On
# 5. Pulse the Re-Init Extensions parameter on the component.
# 6. Monitor the TouchDesigner Textport. You should see successful execution of __init__ followed by onInitTD, where the FSM is finally created.
# 7. Test the manual query again: python >>> op.State.ext.StateExtension.state

'''

Actual Outcome:
TouchDesigner  Build 2023.12480 compile on Mon Sep 22 20:10:42 2025
Python 3.11.1 (heads/3.11-Derivative-dirty:82b0389147, Jan 25 2023, 22:34:27) [MSC v.1929 64 bit (AMD64)]

--- TD Startup Sequence: Executing external path setup (onStart) --- 
  (Debug - DAT:/project1/start_state_machine fn:onStart line:20)
SUCCESS: Virtual Env path added to sys.path. Path: D:\FileReciever\TouchDesigner\BlenderIntegration\.venv\Lib\site-packages 
  (Debug - DAT:/project1/start_state_machine fn:onStart line:30)
--- TD Startup Sequence: Path setup complete --- 
  (Debug - DAT:/project1/start_state_machine fn:onStart line:38)
python >>> op.State.initializeExtensions()
[</project1/State/StateExtension.StateExtension object at 0x000002C4D4FE7150>]
python >>> op.State.ext.StateExtension.ownerComp.path
'/project1/State'
python >>> op.State.ext.StateExtension.state
Traceback (most recent call last):
  File "<Textport>", line 1
AttributeError: 'StateExtension' object has no attribute 'state'
python >>> 

'''