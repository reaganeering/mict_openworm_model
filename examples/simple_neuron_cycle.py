# examples/simple_neuron_cycle.py
import sys
import os
# Adjust the path to import from the parent directory if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mict.mict_framework import MICT
from mict.cell_cycle import CellMICT # Import CellMICT template

# --- Neuron Parameters ---
V_REST = -70.0  # mV (Resting potential)
V_THRESHOLD = -55.0 # mV (Firing threshold)
V_RESET = -75.0   # mV (Reset potential after firing)
TAU_M = 10.0      # ms (Membrane time constant)
R_M = 10.0        # Mohm (Membrane resistance)
DT = 0.1          # ms (Simulation time step)

# --- Neuron MICT Stage Functions ---
def neuron_mapping(state):
    # Receives input current (e.g., from synapses or external stimulus)
    # For this example, we'll use a constant input current for simplicity
    state['input_current'] = state.get('input_current', 1.6) # Default constant input
    # print(f"Neuron {state['cell_id']} Map: Input Current = {state['input_current']:.2f}")
    return state

def neuron_iteration(state):
    # Leaky Integrate-and-Fire (LIF) model update
    v = state['membrane_potential']
    i_input = state['input_current']
    r_m = state['params']['R_M']
    tau_m = state['params']['TAU_M']
    dt = state['params']['DT']

    # Calculate change in voltage using Euler method (simplified)
    dv = (-(v - V_REST) + r_m * i_input) / tau_m * dt
    v_new = v + dv

    state['membrane_potential'] = v_new
    state['fired_this_step'] = False # Reset firing flag
    # print(f"Neuron {state['cell_id']} Iterate: V = {v_new:.2f}")
    return state

def neuron_checking(state):
    # Check if membrane potential reached threshold
    if state['membrane_potential'] >= V_THRESHOLD:
        state['fired_this_step'] = True
        print(f"***** Neuron {state['cell_id']} FIRED! *****")
    # print(f"Neuron {state['cell_id']} Check: Fired = {state['fired_this_step']}")
    return state

def neuron_transformation(state):
    # If neuron fired, reset potential and prepare output
    if state.get('fired_this_step', False):
        state['membrane_potential'] = V_RESET # Reset potential
        state['output_signal'] = 1 # Simple binary output signal
        state['fired_this_step'] = False # Reset flag after processing
    else:
        state['output_signal'] = 0
    # print(f"Neuron {state['cell_id']} Transform: Output = {state['output_signal']}")
    return state

# --- Create and Run Neuron Cycle ---
if __name__ == "__main__":
    neuron_initial_state = {
        'membrane_potential': V_REST,
        'output_signal': 0,
        'fired_this_step': False,
        'params': { # Store parameters within the state
            'R_M': R_M,
            'TAU_M': TAU_M,
            'DT': DT,
        }
    }

    # Use CellMICT template
    neuron1 = CellMICT(
        cell_id="N1",
        cell_type="neuron",
        initial_state=neuron_initial_state,
        stageFunctions={ # Override the default stage functions
            "Mapping": neuron_mapping,
            "Iteration": neuron_iteration,
            "Checking": neuron_checking,
            "Transformation": neuron_transformation
        }
    )

    print("--- Running Simple Neuron Simulation ---")
    for i in range(1000): # Run for 1000 steps (100ms simulation time)
        neuron1.step()
        # Optional: Add a small delay for visualization
        # time.sleep(0.001)

    print("--- Simulation Complete ---")
