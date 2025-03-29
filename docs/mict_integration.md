# Integrating the Core MICT Framework

This document explains how the core **MICT Framework** (available at [Link to mict_framework repository]) is intended to be used within the hierarchical simulation model proposed in this `mict-openworm-model` repository.

## Core Concept: MICT as the Engine

The `MICT` class (available in both Python and JavaScript) serves as the fundamental "engine" driving the dynamics at *each level* of the hierarchical model (Cellular, Component, System, Organism). Each level is represented by its own instance of the `MICT` class, configured with stage functions specific to that level's biological function.

## Instantiating MICT Cycles

Instances of `MICT` are created within the Python classes representing each level (e.g., `CellMICT`, `ComponentMICT`, `SystemMICT`, `OrganismMICT`).

```python
# Example within ComponentMICT __init__ method:
from mict_framework import MICT # Assuming import

# ... (inside __init__)

config = {
    "stages": ["Mapping", "Iteration", "Checking", "Transformation"],
    "initialState": {**initial_state, "component_id": self.component_id},
    "updateUI": self._update_state, # Internal method for state handling
    "stageFunctions": {
        "Mapping": mapping_function_for_component,
        "Iteration": iteration_function_for_component,
        "Checking": checking_function_for_component,
        "Transformation": transformation_function_for_component
    },
    "errorHandler": self._handle_error # Internal error handler
}

self.engine = MICT(config)
self.currentState = self.engine.currentState
```

## State Management
**currentState:** Each MICT instance maintains its own currentState object (a Python dictionary or JavaScript object). This object encapsulates all the relevant information for that specific cycle at that point in time.

**Immutability/Copying:** It is crucial that stage functions avoid modifying the input state object directly. Instead, they should return a new state object (e.g., using { ...state, new_property: value } in JS or state.copy() and modifying the copy in Python). This prevents unintended side effects, especially in a hierarchical system where states might be shared or passed between levels. The core MICT class facilitates this.

**Serialization:** The currentState object can be serialized (e.g., to JSON) for saving the simulation state, debugging, or passing information between processes. Utility functions for serialization/deserialization might be helpful.

## Defining stageFunctions
The core biological and computational logic of the simulation resides within the stageFunctions (Mapping, Iteration, Checking, Transformation) passed to each MICT constructor.

**Inputs:** Each stage function receives the currentState of its own MICT cycle as input.

**Outputs:** Each stage function should return the new currentState after performing its logic.

**Accessing Other Cycles:** Stage functions may need to access the state of other MICT cycles (e.g., a Component cycle needing data from its Cell sub-cycles, or a Cell cycle needing input signals). This communication needs to be managed by the SimulationManager or through a shared state mechanism (with appropriate safeguards for concurrency if applicable).

## Handling Hierarchy: Stepping Sub-Cycles
A key aspect of the HCTS model is the interaction between levels. Typically, the Iteration stage of a higher-level cycle is responsible for advancing the simulation of its sub-cycles.

# Example within ComponentMICT's Iteration function:
```python
def iteration(state: Dict) -> Dict:
    # ... (Simulate interactions between cells) ...

    # Trigger steps in sub-cycles
    for cell_cycle in self.sub_cycles: # self.sub_cycles holds CellMICT instances
        cell_cycle.step() # Advance each cell's MICT cycle

    # ... (Potentially update component state based on sub-cycle results) ...
    return state
```
## Python
Synchronization: The exact timing and synchronization (e.g., should all sub-cycles complete their step before the parent cycle proceeds?) depend on the specific biological model and simulation requirements.

## Error Handling
The errorHandler function provided in the MICT configuration allows for centralized handling of errors that occur within any stage function.

# Example error handler (passed in config)
def handle_simulation_error(error, stage, state):
    print(f"ERROR occurred in stage '{stage}' with state {state}: {error}")
    # Log the error, potentially pause the simulation, or trigger recovery mechanisms

## Python
**updateUI Callback**
The updateUI function in the MICT configuration is the primary mechanism for observing the simulation's progress.

**Purpose:** In the context of this simulation, updateUI would typically be used to:

Log the current state and stage to the console or a file.

Send state updates to a visualization tool (e.g., via WebSockets).

Update data structures used by other parts of the simulation.

**Implementation:** Each MICT class (CellMICT, ComponentMICT, etc.) has an internal _update_state method passed as the updateUI callback, which updates its internal currentState attribute. The SimulationManager would likely be responsible for collecting these state updates for logging or visualization.

## Conclusion
The core MICT class provides the engine for the cyclical dynamics at each level of the proposed C. elegans model. The specific biological logic is implemented within the stageFunctions. The SimulationManager orchestrates the initialization and execution of the hierarchical system, managing the interactions between different MICT cycles. This modular approach allows for building and testing the simulation incrementally.
