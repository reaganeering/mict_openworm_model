# mict/system_cycle.py
from .mict_framework import MICT
from .component_cycle import ComponentMICT # Assuming ComponentMICT is defined
from typing import Dict, Any, Optional, List

class SystemMICT:
    """
    Represents a MICT cycle for a larger system (e.g., nervous system, muscular system).
    Manages a collection of component-level MICT cycles.

    Args:
        system_id (str): A unique identifier for the system.
        system_type (str): The type of system (e.g., 'nervous_system', 'muscular_system').
        initial_state (Dict[str, Any]): Initial state specific to the system level.
        component_cycles (List[ComponentMICT]): List of component MICT cycles managed by this system.
    """
    def __init__(self, system_id: str, system_type: str, initial_state: Dict[str, Any], component_cycles: List[ComponentMICT]):
        self.system_id = system_id
        self.system_type = system_type
        self.component_cycles = component_cycles

        # --- Define MICT Stage Functions for a System ---
        def mapping(state: Dict) -> Dict:
            """Aggregates state from components, receives inputs from other systems."""
            print(f"System {self.system_id} - Mapping: Aggregating component states...")
            # TODO: Aggregate relevant state information from self.component_cycles.
            # TODO: Receive inputs from other system-level cycles or the organism level.
            # state['aggregated_component_state'] = ...
            # state['inputs'] = get_inputs_from_other_systems(...)
            return state

        def iteration(state: Dict) -> Dict:
            """Simulates the interactions *between* components within the system."""
            print(f"System {self.system_id} - Iteration: Simulating system-level interactions...")
            # TODO: Implement logic for interactions between components.
            # Example (Nervous System): Route signals between different neural circuits.
            # Example (Muscular System): Coordinate actions of different muscle groups.

            # --- Trigger steps in component cycles ---
            for comp_cycle in self.component_cycles:
                comp_cycle.step() # Step each component cycle

            return state

        def checking(state: Dict) -> Dict:
            """Evaluates the overall function/output of the system."""
            print(f"System {self.system_id} - Checking: Evaluating system performance...")
            # TODO: Implement checks on the system's overall state or output.
            # Example: Is the nervous system effectively processing sensory information?
            # Example: Is the muscular system generating coordinated movement?
            # state['system_performance'] = ...
            return state

        def transformation(state: Dict) -> Dict:
            """Adapts system properties or sends output to organism level."""
            print(f"System {self.system_id} - Transformation: Adapting system...")
            # TODO: Implement adaptation logic (e.g., large-scale neural plasticity).
            # TODO: Prepare and send output signals to the organism level.
            return state

        # --- MICT Configuration ---
        config = {
            "stages": ["Mapping", "Iteration", "Checking", "Transformation"],
            "initialState": {**initial_state, "system_id": self.system_id},
            "updateUI": self._update_state,
            "stageFunctions": {
                "Mapping": mapping,
                "Iteration": iteration,
                "Checking": checking,
                "Transformation": transformation
            },
            "errorHandler": self._handle_error
        }

        self.engine = MICT(config)
        self.currentState = self.engine.currentState

    def _update_state(self, new_state: Dict, stage: str):
        self.currentState = new_state
        # print(f"System {self.system_id} - Update ({stage})")

    def _handle_error(self, error: Exception, stage: str, state: Dict):
        print(f"ERROR in System {self.system_id} ({stage}): {error}")
        # TODO: Implement error handling

    def step(self):
        """Advances the system's MICT cycle by one step."""
        self.engine.next_stage()

    def get_state(self) -> Dict:
        """Returns the current state of the system."""
        return self.currentState
