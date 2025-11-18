// This file runs immediately when loaded, guaranteeing the namespace is ready.
// It combines initialization and function definition into one step.

window.dash_clientside = window.dash_clientside || {};

// The Firebase configuration needs to be passed dynamically from Python's app.py.
// We'll rely on app.py to set a global variable for this config before this script loads, 
// OR we will revert to placing the dynamic config definition back in the index_string 
// and making the function definition here immediate.

// Since the config is dynamic, we must use the index_string to handle the JSON config, 
// and use a reliable mechanism to define the clientside function immediately. 

// **CRITICAL CHANGE:** We will go back to placing the logic in the index_string, 
// but we will use the `window.onload` event which is the last-resort guarantee 
// that all resources (including the Dash clientside registration) are ready before 
// defining the custom object.