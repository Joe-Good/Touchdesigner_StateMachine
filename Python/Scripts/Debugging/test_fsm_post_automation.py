# test_fsm_post_automation.py
# Automated test script based on [Power On Self Test - Equilateral Expedition] requirements.

import sys
import test_fsm_init
from transitions.core import MachineError  # Used to confirm expected FSM errors [2]

# Define new states the Maestro FSM must implement:
POST_STATES = [
    'WarmUpCycle', 'ExtensionMode', 'RotationCheck', 'LinearCheck',
    'FaultMode', 'TouchDesignerInteractiveChecks'
]


def run_post_tests():
    """
    Executes a sequence of automated tests on the Power On Self Test workflow,
    including successful hardware checks and critical fault intervention.
    """

    print("==========================================================")
    print("= Starting Automated POST Test Suite (TDD)               =")
    print("==========================================================")

    try:
        # FSM starts in 'Attract' state (simulating system running)
        fsm = test_fsm_init.create_fsm_instance()
        print(f"\nSETUP: Maestro initialized. Initial state: {fsm.state}")

    except Exception as e:
        print(f"\nCRITICAL FAILURE: FSM Initialization failed: {e}")
        return

    # --- TEST SCENARIO 1: FULL POST SUCCESS PATH (Hardware Ready) ---

    print("\n--- Test 1: Full POST Sequence (Success Path) ---")

    # Start POST sequence from Attract
    fsm.power_on()
    assert fsm.state == 'WarmUpCycle', f"1.1 FAILED: Expected WarmUpCycle, got {fsm.state}"
    print(f"SUCCESS: System entered WarmUpCycle (LEDs: SlowPulseRainbow).")

    # 1. WarmUp completion (Simulates 30 seconds passing)
    fsm.warmup_complete()
    assert fsm.state == 'ExtensionMode', f"1.2 FAILED: Expected ExtensionMode, got {fsm.state}"
    print(f"SUCCESS: Entered ExtensionMode (Linear Max Limit Switch Check).")

    # 2. Extension check completion (All 6 Linear Actuators hit Max Limit Switch)
    fsm.extension_check_complete()
    assert fsm.state == 'RotationCheck', f"1.3 FAILED: Expected RotationCheck, got {fsm.state}"
    print("SUCCESS: LAs Max Limit Check passed. Moving to RotationCheck (Zeroing).")

    # 3. Rotation check completion (Zeroing and 1/6th revolution check confirmed)
    fsm.rotation_check_complete()
    assert fsm.state == 'LinearCheck', f"1.4 FAILED: Expected LinearCheck, got {fsm.state}"
    print("SUCCESS: Rotation check passed. Moving to LinearCheck (Min Travel Check).")

    # 4. Linear check completion (All LAs pass Min travel/variance check)
    fsm.linear_check_complete()
    assert fsm.state == 'TouchDesignerInteractiveChecks', f"1.5 FAILED: Expected TouchDesignerInteractiveChecks, got {fsm.state}"
    print("SUCCESS: All LAs passed Min check. Starting TD Controller Checks.")

    # 5. TD Interactive Checks completion (Joystick/Kinect sequence complete)
    fsm.post_interactive_complete()
    assert fsm.state == 'Attract', f"1.6 FAILED: Expected Attract Mode on final success, got {fsm.state}"
    print("SUCCESS: Full POST passed. Entering Attract Mode (Autonomous Motion).")

    # --- TEST SCENARIO 2: CRITICAL LA FAULT HANDLING ---

    print("\n--- Test 2: Linear Actuator Fault and Curator Intervention ---")

    # Setup: Reset FSM back to LinearCheck state for fault injection
    fsm.power_on()
    fsm.warmup_complete()
    fsm.extension_check_complete()
    fsm.rotation_check_complete()
    print(f"SETUP: POST sequence reset to {fsm.state}.")

    # 1. SIMULATE FAILURE: LA 4 fails the Min check.
    fsm.linear_check_failure(box_id=4)
    assert fsm.state == 'FaultMode', f"2.1 FAILED: Expected FaultMode on failure, got {fsm.state}"
    print(f"SUCCESS: System entered FaultMode (LA 4 fault).")

    # 2. SIMULATE USER ACTION: Curator marks Box 4 LA as PowerOnMotorsLockedAtMax.
    fsm.set_box_locked_at_max(4)

    # 3. Resume (Should transition out of FaultMode to Attract)
    fsm.resume_from_fault()
    assert fsm.state == 'Attract', f"2.2 FAILED: Expected Attract Mode resume, got {fsm.state}"
    print("SUCCESS: System resumed to Attract Mode, marking LA 4 as permanently excluded from Linear movement.")

    # --- TEST SCENARIO 3: GameMode Exit Fault (Hierarchical Check) ---

    print("\n--- Test 3: GameMode Exit Fault Check ---")

    # FIX: Only attempt to align boxes that are currently NOT Aligned,
    # preventing the MachineError from triggering an invalid transition [2].
    for box_id, box in fsm.box_models.items():
        if box.box_state != 'Aligned':
            try:
                box.alignment_achieved()
            except MachineError:
                # This should not happen with the check above, but catches any latent issues
                print(f"WARNING: Box {box_id} failed alignment_achieved trigger but was not Aligned.")

    fsm.start_interaction()  # Go to GameMode

    # 1. Provoke misalignment on Box 6
    fsm.provoke_misalignment(6)

    # 2. Attempt to exit GameMode with fault active.
    fsm.return_to_attract()

    # Should land in the intervention state due to conditional transition (unless check_all_aligned)
    assert fsm.state == 'Attract_Intervention', f"3.1 FAILED: Expected Attract_Intervention, got {fsm.state}"
    print(f"SUCCESS: Maestro halted in intervention state: {fsm.state}")

    # 3. Resolve Fault manually
    fsm.box_models.get(6).alignment_achieved()

    # 4. Exit fault state using the dedicated trigger
    fsm.force_system_ready()
    assert fsm.state == 'Attract', f"3.2 FAILED: Expected Attract, got {fsm.state}"
    print("SUCCESS: Fault resolved and Maestro FSM returned to Attract mode.")

    print("\n==========================================================")
    print("= ALL AUTOMATED TESTS COMPLETED SUCCESSFULLY!            =")
    print("==========================================================")


if __name__ == "__main__":
    run_post_tests()