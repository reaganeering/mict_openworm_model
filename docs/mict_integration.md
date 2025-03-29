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
