# mict/organism_cycle.py
from .mict_framework import MICT
from .system_cycle import SystemMICT # Assuming SystemMICT is defined
from typing import Dict, Any, Optional, List

class OrganismMICT:
    """
    Represents the top-level MICT cycle for the entire organism (C. elegans).
    Manages system-level MICT cycles.

    Args:
        organism_id (str): A unique identifier for the organism.
        initial_state (Dict[str, Any]): Initial state of the organism (position, goals, etc.).
        system_cycles (List[SystemMICT]): List of system MICT cycles (nervous, muscular, etc.).
    """
    def __init__(self, organism_id: str, initial_state: Dict[str, Any], system_cycles: List[SystemMICT]):
        self.organism_id = organism_id
        self.system_cycles = system_cycles

        # --- Define MICT Stage Functions for the Organism ---
        def mapping(state: Dict) -> Dict:
            """Gathers sensory input, assesses internal state and environment."""
            print(f"Organism {self.organism_id} - Mapping: Assessing state...")
            # TODO: Get sensory input from the simulated environment.
            # TODO: Aggregate state from self.system_cycles (e.g., hunger, energy).
            # state['sensory_input'] = get_sensory_input(state['position'])
            # state['internal_state'] = aggregate_system_states(self.system_cycles)
            # state['environment_map'] = update_environment_map(state)
            return state

        def iteration(state: Dict) -> Dict:
            """Selects and executes a behavior based on goals and current state."""
            print(f"Organism {self.organism_id} - Iteration: Executing behavior...")
            # TODO: Implement behavioral decision-making logic.
            # Example: Choose to move towards food if hungry, avoid danger if threatened.
            # TODO: Send commands to system-level cycles (e.g., nervous system for movement).
            # selected_behavior = choose_behavior(state)
            # execute_behavior(selected_behavior, self.system_cycles)

            # --- Trigger steps in system cycles ---
            for sys_cycle in self.system_cycles:
                sys_cycle.step() # Step each system cycle

            # TODO: Update organism's position based on movement simulation
            # state['position'] = update_position(state)
            return state

        def checking(state: Dict) -> Dict:
            """Evaluates the outcome of the behavior against goals."""
            print(f"Organism {self.organism_id} - Checking: Evaluating outcome...")
            # TODO: Compare the result of the behavior to internal goals.
            # Example: Did the worm get closer to food? Did it successfully avoid the obstacle?
            # state['goal_achieved'] = check_goal_achievement(state)
            return state

        def transformation(state: Dict) -> Dict:
            """Adapts behavioral strategies, updates internal goals or knowledge."""
            print(f"Organism {self.organism_id} - Transformation: Adapting strategy...")
            # TODO: Implement learning and adaptation logic based on Checking.
            # Example: If foraging was successful, reinforce that strategy.
            # Example: Update internal goals based on current needs (e.g., prioritize finding food if hungry).
            # state['behavioral_strategy'] = adapt_strategy(state)
            return state

        # --- MICT Configuration ---
        config = {
            "stages": ["Mapping", "Iteration", "Checking", "Transformation"],
            "initialState": {**initial_state, "organism_id": self.organism_id},
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
        # This could trigger updates in a visualization or log data
        # print(f"Organism {self.organism_id} - Update ({stage})")

    def _handle_error(self, error: Exception, stage: str, state: Dict):
        print(f"ERROR in Organism {self.organism_id} ({stage}): {error}")
        # TODO: Implement robust error handling for the entire simulation

    def run_simulation_step(self):
        """Runs one complete MICT cycle for the organism."""
        self.engine.next_stage() # Map
        self.engine.next_stage() # Iterate (includes stepping sub-cycles)
        self.engine.next_stage() # Check
        self.engine.next_stage() # Transform

    def get_state(self) -> Dict:
        """Returns the current state of the organism."""
        return self.currentState
