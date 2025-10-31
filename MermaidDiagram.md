```mermaid
stateDiagram-v2
    direction LR

    %% Define States
    state Attract
    state PowerOff
    state WarmUpCycle
    state ExtensionMode
    state RotationCheck
    state LinearCheck
    state TouchDesignerInteractiveChecks
    state FaultMode
    state Attract_Intervention
    state GameMode

    %% Initial State
    [*] --> Attract

    %% 1. POWER ON SELF TEST (POST) SEQUENCE
    Attract --> WarmUpCycle : power_on
    WarmUpCycle --> ExtensionMode : warmup_complete
    ExtensionMode --> RotationCheck : extension_check_complete
    RotationCheck --> LinearCheck : rotation_check_complete

    %% 2. LINEAR CHECK PATHS (Success vs. Failure)
    LinearCheck --> TouchDesignerInteractiveChecks : linear_check_complete (Success)
    LinearCheck --> FaultMode : linear_check_failure (Min Variance >3%)

    %% 3. FAULT MODE RESOLUTION
    FaultMode --> Attract : resume_from_fault
    note right of FaultMode
        Curator action: set_box_locked_at_max(LA)
        Returns to Attract, honoring locked motor status.
    end note

    %% 4. FINAL POST STAGE
    TouchDesignerInteractiveChecks --> Attract : post_interactive_complete
    note right of TouchDesignerInteractiveChecks
        Requires Joystick/Kinect sequence completion
        (LEDs: SlowPulseBlue -> SlowPulseOrange -> SlowPulseGreen)
    end note

    %% 5. GAME MODE (APP FLOW)
    Attract --> GameMode : start_interaction
    GameMode --> GameMode : start_interaction (Reflexive)

    %% 6. CONDITIONAL EXIT FROM GAME MODE (Simplified for GitHub rendering compatibility)
    GameMode --> Attract : return_to_attract (Aligned Check Passed)
    note right of Attract
        Successful exit. Motors set to autonomous motion.
    end note

    GameMode --> Attract_Intervention : return_to_attract (Misalignment Detected)
    note right of Attract_Intervention
        Misalignment detected on exit.
        Autonomous motion SUSPENDED.
    end note