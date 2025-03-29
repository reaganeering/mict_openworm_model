// examples/simple_visualization/visualizer.js
// Assumes mict-framework.js is in the parent directory or accessible path
import { createMICTEngine } from '../../mict-framework.js';

// --- DOM Elements ---
const canvas = document.getElementById('visualization-canvas');
const ctx = canvas.getContext('2d');
const stateDisplay = document.getElementById('state-display');
const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');

// --- Constants ---
const MIN_RADIUS = 10;
const MAX_RADIUS = 50;
const SENSITIVITY_INCREMENT = 0.1; // How much sensitivity adapts per cycle
const SENSITIVITY_BOUNDS = { min: 1, max: 9 }; // Keep sensitivity reasonable

// --- MICT Cycle Configuration ---
const config = {
    stages: ["Sense", "Process", "Respond", "Adapt"], // Example stages relevant to a simple biological interaction
    initialState: {
        value: 0,           // Represents a sensed environmental value (e.g., chemical concentration)
        color: 'lightblue', // Represents the internal state/response
        sensitivity: 5.0,   // A threshold used in processing
        responseMessage: 'Initializing...' // Status message
    },
    updateUI: (currentState, currentStage) => {
        // This function is called after each stage transition
        // Update the simple visualization and text display
        stateDisplay.textContent = `Stage: ${currentStage} | State: ${JSON.stringify(currentState, (key, value) =>
            typeof value === 'number' ? parseFloat(value.toFixed(2)) : value // Format numbers
        )}`;
        render(currentState); // Redraw the canvas
    },
    stageFunctions: {
        Sense: (state) => {
            // Simulate sensing the environment
            console.log("MICT: Sensing...");
            const newValue = Math.random() * 10; // Get a new random value (0-10)
            // Return the *new* state for the next stage
            return { ...state, value: newValue, responseMessage: 'Sensing...' };
        },
        Process: (state) => {
            // Process the sensed value based on internal sensitivity
            console.log("MICT: Processing...");
            const triggered = state.value > state.sensitivity;
            const newColor = triggered ? 'orangered' : 'lightblue';
            const message = triggered ? `Processed: Value ${state.value.toFixed(2)} > Sensitivity ${state.sensitivity.toFixed(2)}` : `Processed: Value ${state.value.toFixed(2)} <= Sensitivity ${state.sensitivity.toFixed(2)}`;
            return { ...state, color: newColor, responseMessage: message };
        },
        Respond: (state) => {
            // Determine an observable response based on the processed state
            console.log("MICT: Responding...");
            const response = state.color === 'orangered' ? 'Response: Action Triggered!' : 'Response: Resting.';
            // Example: Log the response or trigger another external action here
            console.log(response);
            return { ...state, responseMessage: response };
        },
        Adapt: (state) => {
            // Adapt internal parameters based on the cycle's outcome (e.g., adjust sensitivity)
            // Simple adaptation: decrease sensitivity if often triggered, increase if rarely triggered
            console.log("MICT: Adapting...");
            let newSensitivity = state.sensitivity;
            if (state.color === 'orangered') { // If triggered
                newSensitivity -= SENSITIVITY_INCREMENT;
            } else { // If not triggered
                newSensitivity += SENSITIVITY_INCREMENT;
            }
            // Clamp sensitivity within bounds
            newSensitivity = Math.max(SENSITIVITY_BOUNDS.min, Math.min(SENSITIVITY_BOUNDS.max, newSensitivity));
            const message = `Adapting: Sensitivity changed to ${newSensitivity.toFixed(2)}`;
            console.log(message);
            return { ...state, sensitivity: newSensitivity, responseMessage: message };
        },
    },
    onError: (error, stage, state) => {
        console.error(`MICT Error during stage ${stage}:`, error, "State:", state);
        // Potentially stop the cycle or implement recovery logic
        engine.stopCycle();
        startButton.disabled = false;
        stopButton.disabled = true;
        stateDisplay.textContent = `Error during ${stage}. Cycle stopped. Check console.`;
    }
};

// --- MICT Engine Instance ---
const engine = createMICTEngine(config);

// --- Rendering Function ---
function render(state) {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Calculate radius based on the 'value' state (maps 0-10 to MIN_RADIUS-MAX_RADIUS)
    const radius = MIN_RADIUS + ((state.value / 10) * (MAX_RADIUS - MIN_RADIUS));

    // Draw the representative "cell" or entity
    ctx.fillStyle = state.color;
    ctx.beginPath();
    ctx.arc(canvas.width / 2, canvas.height / 2, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 1;
    ctx.stroke();


    // Draw text labels
    ctx.fillStyle = 'black';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`Value: ${state.value.toFixed(2)}`, canvas.width / 2, canvas.height / 2 + radius + 15);
    ctx.fillText(`Sensitivity: ${state.sensitivity.toFixed(2)}`, canvas.width / 2, canvas.height / 2 + radius + 30);
    ctx.fillText(`(${state.responseMessage})`, canvas.width / 2, canvas.height / 2 + radius + 45);

}

// --- Event Listeners ---
startButton.addEventListener('click', () => {
    console.log("Starting MICT Cycle...");
    engine.startCycle(1000); // Run cycle every 1000 ms (1 second)
    startButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener('click', () => {
    console.log("Stopping MICT Cycle...");
    engine.stopCycle();
    startButton.disabled = false;
    stopButton.disabled = true;
    stateDisplay.textContent = `Cycle stopped by user. ${stateDisplay.textContent}`; // Append previous state info
});

// --- Initialization ---
function init() {
    console.log("Initializing visualizer...");
    // Initial render based on initialState
    render(engine.getCurrentState());
    // Initial state display update
    config.updateUI(engine.getCurrentState(), engine.getCurrentStage());
    stopButton.disabled = true; // Stop button initially disabled
    startButton.disabled = false; // Start button initially enabled
    console.log("Visualizer ready.");
}

// Run initialization when the script loads
init();
