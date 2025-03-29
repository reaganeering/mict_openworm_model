# examples/two_neuron_interaction.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mict.mict_framework import MICT
from mict.cell_cycle import CellMICT # Import CellMICT

# --- Neuron Parameters (Same as before) ---
V_REST = -70.0; V_THRESHOLD = -55.0; V_RESET = -75.0; TAU_M = 10.0; R_M = 10.0; DT = 0.1

# --- Modified Neuron Stage Functions (to handle synaptic input) ---
# We'll create instances of these functions for each neuron

def create_neuron_stage_functions(neuron_id, synapse_weights):
    """Creates MICT stage functions for a specific neuron."""

    def neuron_mapping(state):
        # Receive input current from connected neurons
        input_current = state.get('base_current', 1.0) # Base external input
        received_signals = state.get('received_signals', {})

        for pre_synaptic_id, weight in synapse_weights.get(neuron_id, {}).items():
            # Get output signal from the pre-synaptic neuron's *previous* state
            # In a full simulation manager, you'd get this from the shared state
            # For this simple example, we'll assume a global state dict (not ideal!)
            if pre_synaptic_id in global_neuron_states:
                 # Get the output from the previous Transformation stage
                input_current += global_neuron_states[pre_synaptic_id].get('output_signal', 0) * weight

        state['input_current'] = input_current
        state['received_signals'] = {} # Clear received signals for next step
        # print(f"Neuron {state['cell_id']} Map: Input Current = {state['input_current']:.2f}")
        return state

    def neuron_iteration(state):
        # LIF model update (same as before)
        v = state['membrane_potential']
        i_input = state['input_current']
        r_m = state['params']['R_M']
        tau_m = state['params']['TAU_M']
        dt = state['params']['DT']
        dv = (-(v - V_REST) + r_m * i_input) / tau_m * dt
        v_new = v + dv
        state['membrane_potential'] = v_new
        state['fired_this_step'] = False
        # print(f"Neuron {state['cell_id']} Iterate: V = {v_new:.2f}")
        return state

    def neuron_checking(state):
        # Check firing threshold (same as before)
        if state['membrane_potential'] >= V_THRESHOLD:
            state['fired_this_step'] = True
            print(f"***** Neuron {state['cell_id']} FIRED! *****")
        # print(f"Neuron {state['cell_id']} Check: Fired = {state['fired_this_step']}")
        return state

    def neuron_transformation(state):
        # Reset potential and prepare output signal (same as before)
        if state.get('fired_this_step', False):
            state['membrane_potential'] = V_RESET
            state['output_signal'] = 1
            state['fired_this_step'] = False
        else:
            state['output_signal'] = 0
        # print(f"Neuron {state['cell_id']} Transform: Output = {state['output_signal']}")
        return state

    return {
        "Mapping": neuron_mapping,
        "Iteration": neuron_iteration,
        "Checking": neuron_checking,
        "Transformation": neuron_transformation
    }


# --- Simulation Setup ---
if __name__ == "__main__":
    # Define synaptic connections and weights
    # N1 sends excitatory input to N2
    synapses = {
        "N2": {"N1": 1.5} # Target Neuron: {Source Neuron: Weight}
    }

    # Shared state dictionary (Simplified approach for this example)
    global_neuron_states = {}

    # --- Create Neurons ---
    neuron1_initial_state = {
        'membrane_potential': V_REST, 'output_signal': 0, 'fired_this_step': False,
        'base_current': 1.6, # Constant input to make N1 fire periodically
        'params': {'R_M': R_M, 'TAU_M': TAU_M, 'DT': DT}
    }
    neuron1_funcs = create_neuron_stage_functions("N1", synapses)
    neuron1 = CellMICT("N1", "neuron", neuron1_initial_state, stageFunctions=neuron1_funcs)
    global_neuron_states["N1"] = neuron1.currentState # Add to shared state

    neuron2_initial_state = {
        'membrane_potential': V_REST, 'output_signal': 0, 'fired_this_step': False,
        'base_current': 0.0, # No base input for N2
        'params': {'R_M': R_M, 'TAU_M': TAU_M, 'DT': DT}
    }
    neuron2_funcs = create_neuron_stage_functions("N2", synapses)
    neuron2 = CellMICT("N2", "neuron", neuron2_initial_state, stageFunctions=neuron2_funcs)
    global_neuron_states["N2"] = neuron2.currentState # Add to shared state


    print("--- Running Two Neuron Interaction Simulation ---")
    # Simple synchronous update loop
    for i in range(1000):
        print(f"\n--- Step {i} ---")

        # Store previous outputs before stepping
        prev_outputs = {
            "N1": global_neuron_states["N1"].get('output_signal', 0),
            "N2": global_neuron_states["N2"].get('output_signal', 0)
        }

        # Pass previous output to the *next* mapping step (simplified communication)
        # In a real manager, this would be handled more robustly
        neuron1.currentState['received_signals'] = {} # Clear first
        neuron2.currentState['received_signals'] = {"N1": prev_outputs["N1"]} # N2 receives from N1

        # Step both neurons through their MICT cycles
        neuron1.step()
        neuron2.step()

        # Update the global state (for the next iteration's input calculation)
        global_neuron_states["N1"] = neuron1.currentState
        global_neuron_states["N2"] = neuron2.currentState

        # Optional: time.sleep(0.01)

    print("--- Simulation Complete ---")
