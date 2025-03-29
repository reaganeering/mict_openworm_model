# mict/simulation_manager.py
import time
from .organism_cycle import OrganismMICT
from .system_cycle import SystemMICT
from .component_cycle import ComponentMICT
from .cell_cycle import CellMICT
# Import visualization libraries if needed (e.g., Pygame, Matplotlib animation)

class SimulationManager:
    """
    Manages the overall C. elegans simulation using hierarchical MICT cycles.
    """
    def __init__(self):
        self.organism_cycle: Optional[OrganismMICT] = None
        self.is_running = False
        self.simulation_time = 0.0
        self.steps_per_second = 100 # Example simulation speed

    def initialize_simulation(self):
        """Initializes the organism and its sub-cycles."""
        print("Initializing Simulation...")
        # --- 1. Create Cell Cycles ---
        # TODO: Load cell data (connectome, types, initial states) from OpenWorm data
        #       and create CellMICT instances for each cell.
        neurons = []
        muscle_cells = []
        # Example:
        # neuron_data = load_neuron_data()
        # for data in neuron_data:
        #     neurons.append(CellMICT(data['id'], 'neuron', data['initial_state'], data['neighbors']))
        # muscle_data = load_muscle_data()
        # for data in muscle_data:
        #     muscle_cells.append(CellMICT(data['id'], 'muscle', data['initial_state'], data['neighbors']))

        # --- 2. Create Component Cycles ---
        # TODO: Group cells into components (neural circuits, muscle groups) and create ComponentMICT instances.
        neural_circuit_1 = ComponentMICT('circuit1', 'neural_circuit', {}, neurons[0:10]) # Example
        muscle_group_a = ComponentMICT('muscle_group_a', 'muscle_group', {}, muscle_cells[0:5]) # Example
        # ... create other components ...
        component_cycles = [neural_circuit_1, muscle_group_a] # Example list

        # --- 3. Create System Cycles ---
        # TODO: Group components into systems (nervous system, muscular system) and create SystemMICT instances.
        nervous_system = SystemMICT('nervous_sys', 'nervous_system', {}, [neural_circuit_1]) # Example
        muscular_system = SystemMICT('muscular_sys', 'muscular_system', {}, [muscle_group_a]) # Example
        system_cycles = [nervous_system, muscular_system] # Example list

        # --- 4. Create Organism Cycle ---
        # TODO: Define the organism's initial state (position, goals, etc.)
        organism_initial_state = {'position': (0, 0), 'velocity': (0, 0), 'hunger': 0.5} # Example
        self.organism_cycle = OrganismMICT('worm1', organism_initial_state, system_cycles)

        self.simulation_time = 0.0
        print("Simulation Initialized.")

    def run_simulation(self):
        """Runs the main simulation loop."""
        if not self.organism_cycle:
            print("Simulation not initialized.")
            return

        self.is_running = True
        print("Starting Simulation Loop...")
        while self.is_running:
            start_time = time.time()

            # --- Run one step of the top-level organism cycle ---
            # This will recursively step through all sub-cycles (system, component, cell)
            self.organism_cycle.run_simulation_step()

            # --- Update simulation time ---
            # Note: The actual time represented by a step depends on the 'dt' used
            #       within the iteration stages of the sub-cycles.
            #       This is simplified for the template.
            self.simulation_time += 1.0 / self.steps_per_second

            # --- Visualization (Optional) ---
            # Update any visualization based on self.organism_cycle.get_state()
            # and potentially states from lower levels.
            # e.g., update_visualization(self.organism_cycle.get_state())

            # --- Control simulation speed ---
            elapsed_time = time.time() - start_time
            sleep_time = (1.0 / self.steps_per_second) - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)

            # --- Add stopping conditions if needed ---
            # if some_condition:
            #     self.stop_simulation()

        print("Simulation Stopped.")

    def stop_simulation(self):
        """Stops the simulation loop."""
        self.is_running = False

# --- Example Usage (in a main script) ---
if __name__ == "__main__":
    manager = SimulationManager()
    manager.initialize_simulation()
    # manager.run_simulation() # Run indefinitely until stopped or condition met

    # Or run for a fixed number of steps:
    if manager.organism_cycle:
        for _ in range(200): # Example: Run 200 steps
            manager.run_simulation_step()
            print(f"Time: {manager.simulation_time:.2f} | Organism State: {manager.organism_cycle.get_state()}")
            time.sleep(0.05) # Small delay for visualization
