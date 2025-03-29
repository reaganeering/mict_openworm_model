# examples/simple_muscle_cycle.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mict.mict_framework import MICT
from mict.cell_cycle import CellMICT

# --- Muscle Parameters ---
MAX_CONTRACTION = 1.0
CONTRACTION_RATE = 0.1 # Rate of contraction per step with input
RELAXATION_RATE = 0.05 # Rate of relaxation per step without input
DT = 0.1 # Simulation time step (should match neuron if interacting)

# --- Muscle MICT Stage Functions ---
def muscle_mapping(state):
    # Receives input signal (e.g., from a connected neuron)
    # For this example, simulate alternating input
    step_count = state.get('step_count', 0)
    state['input_signal'] = 1 if (step_count // 50) % 2 == 0 else 0 # On for 50 steps, off for 50
    state['step_count'] = step_count + 1
    # print(f"Muscle {state['cell_id']} Map: Input Signal = {state['input_signal']}")
    return state

def muscle_iteration(state):
    # Simple muscle contraction/relaxation model
    contraction = state['contraction_level']
    input_signal = state['input_signal']

    if input_signal > 0:
        contraction += CONTRACTION_RATE * DT
    else:
        contraction -= RELAXATION_RATE * DT

    # Clamp contraction level between 0 and MAX_CONTRACTION
    contraction = max(0.0, min(MAX_CONTRACTION, contraction))

    state['contraction_level'] = contraction
    # print(f"Muscle {state['cell_id']} Iterate: Contraction = {contraction:.2f}")
    return state

def muscle_checking(state):
    # Check contraction level, perhaps against thresholds
    # print(f"Muscle {state['cell_id']} Check: Contraction = {state['contraction_level']:.2f}")
    return state

def muscle_transformation(state):
    # Prepare output (e.g., force generated, change in shape)
    # state['output_force'] = calculate_force(state['contraction_level'])
    # print(f"Muscle {state['cell_id']} Transform: State updated")
    return state

# --- Create and Run Muscle Cycle ---
if __name__ == "__main__":
    muscle_initial_state = {
        'contraction_level': 0.0,
        'step_count': 0, # For simulating input
        'params': {
            'DT': DT,
        }
        # 'output_force': 0.0
    }

    muscle1 = CellMICT(
        cell_id="M1",
        cell_type="muscle",
        initial_state=muscle_initial_state,
        stageFunctions={
            "Mapping": muscle_mapping,
            "Iteration": muscle_iteration,
            "Checking": muscle_checking,
            "Transformation": muscle_transformation
        }
    )

    print("--- Running Simple Muscle Simulation ---")
    for _ in range(1000): # Run for 1000 steps
        muscle1.step()
        print(f"Muscle Contraction: {muscle1.currentState['contraction_level']:.3f}") # Print contraction level
        # time.sleep(0.01)

    print("--- Simulation Complete ---")
