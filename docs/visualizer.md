# How to Use the Simple MICT Visualizer Example

This example demonstrates how to connect the state transitions of a basic MICT (Mobius Inspired Cyclical Transformation) cycle to a simple visual output using HTML5 Canvas and JavaScript. It provides a tangible way to see the framework in action.

## Purpose

*   Show a practical implementation of the `updateUI` callback within the MICT configuration.
*   Visualize how the system's `state` changes through the `Sense`, `Process`, `Respond`, and `Adapt` stages.
*   Provide a basic template for creating more complex visualizations driven by MICT cycles.

## Prerequisites

*   A modern web browser that supports ES6 Modules (Chrome, Firefox, Edge, Safari).
*   Access to the example files.
*   A simple local web server (due to browser security restrictions on ES6 modules loaded via `file://`).

## Files Included

*   `index.html`: The main HTML file that structures the page, includes the canvas, buttons, and state display area, and loads the JavaScript module.
*   `visualizer.js`: Contains the core logic:
    *   Imports the `createMICTEngine` function from the core framework.
    *   Defines the MICT configuration (`stages`, `initialState`, `stageFunctions`, `updateUI`).
    *   Creates the MICT engine instance.
    *   Includes the `render` function to draw on the HTML5 canvas based on the current MICT state.
    *   Sets up event listeners for the Start/Stop buttons.
    *   Initializes the visualization.
*   `style.css`: Basic CSS for layout and appearance.
*   `../../mict-framework.js` (or similar path): **This example assumes the core MICT framework JavaScript file (`mict-framework.js`) is located two directories above the example directory.** You may need to adjust the import path in `visualizer.js` based on your project structure.

    ```javascript
    // Inside visualizer.js - Adjust this path if needed:
    import { createMICTEngine } from '../../mict-framework.js';
    ```

## Setup

1.  **Get the Files:** Clone the repository containing this example or download the necessary files (`index.html`, `visualizer.js`, `style.css`, and ensure you have `mict-framework.js` accessible).
2.  **Ensure File Structure:** Place the files in a directory structure where the import path in `visualizer.js` correctly points to `mict-framework.js`. The default assumes:
    ```
    your-project-root/
    ├── mict-framework.js
    └── examples/
        └── simple_visualization/
            ├── index.html
            ├── visualizer.js
            └── style.css
    ```
3.  **Prepare a Local Server:** Because `visualizer.js` uses ES6 `import`, you cannot simply open `index.html` directly from your file system in most browsers (due to CORS security policies). You need to serve the files using a simple local web server. Here are a few easy ways:
    *   **Using Python:** If you have Python 3 installed, navigate to the directory containing `index.html` (e.g., `simple_visualization`) in your terminal and run:
        ```bash
        python -m http.server
        ```
        Then open your browser to `http://localhost:8000`.
    *   **Using Node.js `http-server`:** If you have Node.js installed, you can install `http-server` globally (`npm install -g http-server`) and then run it in the directory containing `index.html`:
        ```bash
        http-server .
        ```
        Then open the URL provided (usually `http://localhost:8080`).
    *   **Using VS Code Live Server:** If you use Visual Studio Code, install the "Live Server" extension. Right-click on `index.html` in the VS Code explorer and choose "Open with Live Server".

## Running the Example

1.  Start your local web server in the directory containing `index.html` (as described in Setup step 3).
2.  Open your web browser and navigate to the local URL provided by your server (e.g., `http://localhost:8000` or `http://localhost:8080`).
3.  You should see the title, the Start/Stop buttons, a canvas with an initial light blue circle, and a state display area below it.

## Interaction

*   **Start Cycle:** Click the "Start Cycle" button. The MICT engine will begin cycling through its stages (`Sense` -> `Process` -> `Respond` -> `Adapt` -> `Sense`...).
*   **Observe:**
    *   The circle on the canvas will change color (lightblue or orangered) and size based on the random `value` generated in the `Sense` stage and the `sensitivity` threshold used in the `Process` stage.
    *   The "State Display" text area below the canvas will update after each stage, showing the current stage name and the complete state object (including `value`, `color`, `sensitivity`, and `responseMessage`).
    *   The `sensitivity` value should slowly change over time based on the logic in the `Adapt` stage.
    *   Check your browser's developer console (usually F12) to see log messages printed by each stage function.
*   **Stop Cycle:** Click the "Stop Cycle" button to pause the MICT engine.

## Understanding the Code (`visualizer.js`)

*   **MICT Configuration (`config`):** This object defines how the MICT cycle behaves. Pay attention to:
    *   `initialState`: The starting point of the system.
    *   `stageFunctions`: Defines the logic executed during each stage. Each function receives the current state and must return the *new* state for the next stage.
    *   `updateUI`: This callback is the key link between the MICT engine and the visualization. It's called automatically by the engine whenever the stage changes, providing the latest state.
*   **`render(state)` Function:** This function takes the current MICT state object and draws the visualization on the canvas accordingly (adjusting circle size and color).
*   **`engine.startCycle(interval)`:** Starts the automatic cycling with the specified time (in milliseconds) between stage transitions.
*   **`engine.stopCycle()`:** Stops the automatic cycling.

## Customization

This is a basic example. You can modify it to explore MICT further:

*   Change the `stageFunctions` logic to simulate different behaviors.
*   Modify the `initialState`.
*   Add more complex properties to the state object.
*   Enhance the `render` function to create more sophisticated visualizations.
*   Adjust the cycle interval in `engine.startCycle()`.
*   Experiment with different MICT configurations (different stages, etc.).

This example provides a foundation for visualizing systems modeled with the MICT framework.
