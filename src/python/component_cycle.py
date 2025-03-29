# mict/component_cycle.py
from .mict_framework import MICT
from .cell_cycle import CellMICT # Assuming CellMICT is in the same directory
from typing import Dict, Any, Optional, List

class ComponentMICT:
    """
    Represents a MICT cycle for a component (e.g., neural circuit, muscle group).
    Manages a collection of lower-level (e.g., cellular) MICT cycles.

    Args:
        component_id (str): A unique identifier for the component.
        component_type (str): The type of component (e.g., 'neural_circuit', 'muscle_group').
        initial_state (Dict[str, Any]): Initial state specific to the component level.
        sub_cycles (List[CellMICT]): A list of the cell-level MICT cycles managed by this component.
    """
    def __init__(self, component_id: str, component_type: str, initial_state: Dict[str, Any], sub_cycles: List[CellMICT]):
        self.component_id = component_id
        self.component_type = component_type
        self.sub_cycles = sub_cycles # Store references to the cell cycles

        # --- Define MICT Stage Functions for a Component ---
        def mapping(state: Dict) -> Dict:
            """Aggregates state from sub-cycles, receives inputs from other components."""
            print(f"Component {self.component_id} - Mapping: Aggregating states...")
            # TODO: Aggregate relevant state information from self.sub_cycles.
            # Example: aggregated_activity = [cell.get_state().get('activity') for cell in self.sub_cycles]
            # TODO: Receive inputs from connected components or higher levels.
            # state['aggregated_state'] = calculate_aggregated_state(self.sub_cycles)
            # state['inputs'] = get_inputs_from_other_components(...)
            return state

        def iteration(state: Dict) -> Dict:
            """Simulates the interactions *between* sub-cycles within the component."""
            print(f"Component {self.component_id} - Iteration: Simulating interactions...")
            # TODO: Implement logic for interactions between cells/units in the component.
            # Example (Neural Circuit): Simulate synaptic transmission based on aggregated activity.
            # Example (Muscle Group): Coordinate contraction patterns based on aggregated state.

            # --- Trigger steps in sub-cycles ---
            # This is a key part of hierarchical control. How sub-cycles are stepped
            # depends on the specific model (e.g., all at once, sequentially, based on events).
            for cell_cycle in self.sub_cycles:
                 cell_cycle.step() # Example: Step each sub-cycle once per component iteration

            return state

        def checking(state: Dict) -> Dict:
            """Evaluates the overall function/output of the component."""
            print(f"Component {self.component_id} - Checking: Evaluating function...")
            # TODO: Implement checks on the component's aggregated state or output.
            # Example: Does the neural circuit output match the expected pattern?
            # Example: Is the muscle group generating the correct force?
            # state['performance_metric'] = calculate_component_performance(state)
            return state

        def transformation(state: Dict) -> Dict:
            """Adapts component properties (e.g., connections) or sends output."""
            print(f"Component {self.component_id} - Transformation: Adapting component...")
            # TODO: Implement adaptation logic (e.g., Hebbian learning for synapses).
            # TODO: Prepare and send output signals to other components or higher levels.
            # state['connections'] = adapt_connections(state)
            # send_output_to_neighbors(state['output'])
            return state

        # --- MICT Configuration ---
        config = {
            "stages": ["Mapping", "Iteration", "Checking", "Transformation"],
            "initialState": {**initial_state, "component_id": self.component_id},
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
        # print(f"Component {self.component_id} - Update ({stage}): {new_state}")

    def _handle_error(self, error: Exception, stage: str, state: Dict):
        print(f"ERROR in Component {self.component_id} ({stage}): {error}")
        # TODO: Implement error handling

    def step(self):
        """Advances the component's MICT cycle by one step."""
        self.engine.next_stage()

    def get_state(self) -> Dict:
        """Returns the current state of the component."""
        return self.currentState

    def get_sub_cycle_states(self) -> List[Dict]:
        """Returns the current states of all sub-cycles."""
        return [cell.get_state() for cell in self.sub_cycles]
