# ==============================================================================
# Pure Python Finite State Machine Model (test_fsm_init.py)
# PURPOSE: PoC Test to confirm core FSM logic is sound and expose hidden TD crash errors.
# FIX: Added the create_fsm_instance() wrapper function for interactive access.
# ==============================================================================

from transitions import Machine


class TestStateModel(object):
    """
    The Maestro FSM Model. Controls the high-level application flow.
    """

    # --- 1. STATE DEFINITIONS ---
    states = [
        'Attract',
        'GameMode',
        'Calibration',
        'WarmUpCycle',
        'ExtensionMode',
        'RotationCheck',
        'LinearCheck',
        'TouchDesignerInteractiveChecks',
        'FaultMode',
        'Attract_Intervention'
    ]

    # --- 2. INITIALIZATION ---
    def __init__(self):
        print("DEBUG 1: Initializing custom attributes.")
        # Non-TD dependent custom attributes
        self.animation_frame_offset = 0  # Initialized safely to 0 [3]
        self.boxes = []

        # --- CRITICAL POINT OF FAILURE TEST ---
        # If this crashes, the traceback will appear immediately in the console.
        print("DEBUG 2: Attempting to instantiate pytransitions Machine.")
        self.machine = Machine(
            model=self,
            states=TestStateModel.states,
            initial='Attract',
            auto_transitions=True,
            name='Maestro_FSM'
        )
        print("DEBUG 3: Machine instantiation SUCCESS.")

        self._add_application_transitions()
        print("DEBUG 4: Transitions added successfully.")

        # This confirms pytransitions bound the state attribute to the model
        print(f"DEBUG 5: FSM successfully bound. Current state: {self.state}")

    # --- 3. TRANSITION DEFINITIONS ---
    def _add_application_transitions(self):
        # Power On Self Test (POST) Sequence
        self.machine.add_transition(trigger='power_on', source='Attract', dest='WarmUpCycle')
        self.machine.add_transition('warmup_complete', 'WarmUpCycle', 'ExtensionMode')
        self.machine.add_transition('extension_check_complete', 'ExtensionMode', 'RotationCheck')
        self.machine.add_transition('rotation_check_complete', 'RotationCheck', 'LinearCheck')

        # Linear Check Paths
        self.machine.add_transition(
            trigger='linear_check_complete',
            source='LinearCheck',
            dest='TouchDesignerInteractiveChecks',
            conditions=['_check_motor_variance']
        )
        self.machine.add_transition(
            trigger='linear_check_failure',
            source='LinearCheck',
            dest='FaultMode',
            unless=['_check_motor_variance']
        )

        self.machine.add_transition('post_interactive_complete', 'TouchDesignerInteractiveChecks', 'Attract')
        self.machine.add_transition('resume_from_fault', 'FaultMode', 'Attract')

        # Game Mode Entry
        self.machine.add_transition(
            trigger='start_interaction',
            source=['Attract', 'GameMode'],
            dest='GameMode',
            before='_log_interaction_start'
        )

        # Conditional Exit from Game Mode
        self.machine.add_transition(
            trigger='return_to_attract',
            source='GameMode',
            dest='Attract',
            conditions=['check_all_aligned']
        )
        self.machine.add_transition(
            trigger='return_to_attract',
            source='GameMode',
            dest='Attract_Intervention',
            unless=['check_all_aligned']
        )
        self.machine.add_transition('force_system_ready', 'Attract_Intervention', 'Attract',
                                    conditions=['check_all_aligned'])

    # --- 4. CALLBACKS AND CONDITIONS (Placeholders) ---
    def check_all_aligned(self):
        return True

    def _check_motor_variance(self):
        return True

    def _log_interaction_start(self):
        pass  # Placeholder for actual action

    # State Entry Callbacks (Now empty/passive, deferring TD-dependent logic)
    def on_enter_Attract(self):
        pass

    def on_enter_GameMode(self):
        pass

    # --- 5. REQUIRED WRAPPER FUNCTION ---


def create_fsm_instance():
    """Instantiates the TestStateModel and returns the instance."""
    return TestStateModel()


# ==============================================================================
# EXECUTION
# ==============================================================================
if __name__ == '__main__':
    print("-" * 40)
    print("Starting External FSM Initialization Test (via direct execution)")
    # When running the file directly, we create the instance, triggering __init__
    create_fsm_instance()
    print("-" * 40)