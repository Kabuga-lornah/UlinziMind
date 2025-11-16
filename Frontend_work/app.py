import dash
from dash import dcc, html, clientside_callback, ClientsideFunction
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import json
import requests
import pandas as pd
import sys

# Import the layouts from the new files
from auth_layout import auth_layout
from dashboard import dashboard_layout, ALERTS_URL 

# --- Configuration ---
REFRESH_INTERVAL_MS = 5000 
EXTERNAL_STYLESHEETS = [dbc.themes.SLATE] 

# --- NEW: Firebase Configuration (PLACEHOLDERS) ---
# *** IMPORTANT: Replace these values with your actual Firebase project config ***
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDU_xPuE1EkpGGvFae2nH9_khctiV5dUJY",
    "authDomain": "ulinzimind.firebaseapp.com",
    "projectId": "ulinzimind",
    "storageBucket": "ulinzimind.firebasestorage.app",
    "messagingSenderId": "716679595914",
    "appId": "1:716679595914:web:e02b5c137e514246156a73",
    "measurementId": "G-BTZH80JN16"
}


# --- Dash App Setup ---
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, title='UlinziMind AI Sentinel')

# --- Inject Firebase SDK via Custom Index HTML ---
# This includes all client-side Firebase logic (login, register, sign-out, token refresh)
app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body>
        <div id="react-entry-point">
            {{%app_entry%}}
        </div>
        <footer>
            {{%config%}}

            <!-- Load Firebase SDKs -->
            <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-app-compat.js"></script>
            <script src="https://www.gstatic.com/firebasejs/9.6.1/firebase-auth-compat.js"></script>
            
            <script>
                // Initialize Firebase App globally
                const firebaseConfig = {json.dumps(FIREBASE_CONFIG)};
                const app = firebase.initializeApp(firebaseConfig);
                const auth = firebase.auth();

                // Helper to update the JS-side error message
                function updateJsStatus(id, message, isError = true) {{
                    const el = document.getElementById(id);
                    if (el) {{
                        el.innerText = message;
                        el.style.color = isError ? 'red' : 'green';
                    }}
                }}

                // Expose client-side functions to be called by Dash
                window.dash_clientside = Object.assign({{}}, window.dash_clientside, {{
                    firebaseAuth: {{
                        // --- 1. Login Function ---
                        login: function(data) {{
                            if (!data || !data.email || !data.password) return null;
                            updateJsStatus('login-status-js', ''); // Clear errors
                            
                            return new Promise((resolve) => {{
                                auth.signInWithEmailAndPassword(data.email, data.password)
                                    .then((userCredential) => {{
                                        updateJsStatus('login-status-js', 'Success! Redirecting...', false);
                                        userCredential.user.getIdToken(true).then(resolve).catch(() => resolve(null));
                                    }})
                                    .catch((error) => {{
                                        console.error("Firebase Login Error:", error);
                                        const errorMessage = error.message.replace('Firebase: ', '');
                                        updateJsStatus('login-status-js', `Login Failed: ${{errorMessage}}`);
                                        resolve(null);
                                    }});
                            }});
                        }},

                        // --- 2. Register Function ---
                        register: function(data) {{
                            if (!data || !data.email || !data.password) return null;
                            updateJsStatus('register-status-js', ''); // Clear errors

                            return new Promise((resolve) => {{
                                auth.createUserWithEmailAndPassword(data.email, data.password)
                                    .then(() => {{
                                        updateJsStatus('register-status-js', 'Registration successful! Redirecting to Login...', false);
                                        // Return a flag to tell the Python side to redirect to login
                                        resolve('REGISTERED'); 
                                    }})
                                    .catch((error) => {{
                                        console.error("Firebase Register Error:", error);
                                        const errorMessage = error.message.replace('Firebase: ', '');
                                        updateJsStatus('register-status-js', `Registration Failed: ${{errorMessage}}`);
                                        resolve(null);
                                    }});
                            }});
                        }},

                        // --- 3. Sign Out Function ---
                        signOut: function() {{
                            auth.signOut().then(() => {{
                                console.log("User signed out.");
                            }});
                            // Always return null to clear the token store
                            return null;
                        }}
                    }}
                }});
            </script>

            {{%scripts%}}
        </footer>
    </body>
</html>
"""

# --- Main Layout Definition (Global Stores and Router) ---
app.layout = html.Div(style={'backgroundColor': '#1C1C1C', 'minHeight': '100vh', 'padding': '10px'}, children=[
    # Global State Stores
    dcc.Store(id='raw-data-store'), # Data fetched from the protected API
    dcc.Store(id='jwt-token-store', data=None), # The core authentication state (Firebase ID Token)
    dcc.Store(id='navigation-store', data={'page': 'login'}), # State for routing between Login/Register
    
    dcc.Interval(
        id='interval-component',
        interval=REFRESH_INTERVAL_MS, 
        n_intervals=0,
        disabled=True 
    ),

    # Main content area (Router Output)
    html.Div(id='page-content')
])


# =================================================================
# === PYTHON CALLBACKS (ROUTING, TOKEN MANAGEMENT, DATA FETCH) ======
# =================================================================

# --- 1. Clientside Callbacks to Run Firebase Auth JS ---

# Bridge 1: Triggers client-side Firebase Login
clientside_callback(
    ClientsideFunction(
        namespace='dash_clientside',
        function_name='firebaseAuth.login'
    ),
    Output('jwt-token-store', 'data', allow_duplicate=True), # Output the token (or null)
    Input('login-data-store', 'data'), # Input from auth_layout.py when user clicks Login
    prevent_initial_call=True
)

# Bridge 2: Triggers client-side Firebase Registration
clientside_callback(
    ClientsideFunction(
        namespace='dash_clientside',
        function_name='firebaseAuth.register'
    ),
    Output('navigation-store', 'data', allow_duplicate=True), # Output a success state to redirect
    Input('register-data-store', 'data'), # Input from auth_layout.py when user clicks Register
    prevent_initial_call=True
)

# Bridge 3: Triggers client-side Firebase Sign Out
clientside_callback(
    ClientsideFunction(
        namespace='dash_clientside',
        function_name='firebaseAuth.signOut'
    ),
    Output('jwt-token-store', 'data', allow_duplicate=True),
    Input('sign-out-button', 'n_clicks'), # Input from dashboard.py Sign Out button
    prevent_initial_call=True
)

# --- 2. Main Router Logic (Conditional Page Rendering) ---
@app.callback(
    Output('page-content', 'children'),
    Output('interval-component', 'disabled'),
    Input('jwt-token-store', 'data'), # Primary trigger: Token state change
    Input('navigation-store', 'data'), # Secondary trigger: Manual navigation (e.g., after registration)
)
def render_page_content(token, nav_state):
    """Renders the appropriate layout (Auth or Dashboard) based on token state."""
    
    # Priority 1: If a valid token exists, go to the Dashboard
    if token:
        return dashboard_layout, False # Enable refresh
    
    # Priority 2: If no token, show the Auth screen
    # Check if registration was successful and redirect to login form
    if nav_state and nav_state.get('page') == 'REGISTERED':
        return auth_layout, True # Display auth_layout (defaults to Login), Disable refresh
    
    # Default: Show Auth (Login/Register) screen
    return auth_layout, True # Disable refresh


# --- 3. Data Fetching (Uses Token to Call Protected API) ---
@app.callback(
    Output('raw-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('jwt-token-store', 'data'), # Retrieve the token
)
def fetch_data(n, token):
    """Fetches data from the protected FastAPI endpoint using the Firebase ID Token."""
    # Prevent initial run and runs when not authenticated
    if not token:
        # Returning [] here is important to signal to the dashboard.py viz callbacks to show empty state
        return [] 

    # Prepare the Authorization header using the Firebase ID Token
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(ALERTS_URL, params={'count': 20}, headers=headers) 
        response.raise_for_status() 
        data = response.json()
        df = pd.DataFrame(data)
        return df.to_dict('records')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
             print("ERROR: Authentication failed (401). Token is expired or invalid. Clearing token.")
             # Dash cannot directly update the jwt-token-store here, but this
             # error will cause the next router callback check to fail, showing the login screen.
             return None 
        else:
            print(f"ERROR: API fetch failed with status {e.response.status_code}: {e}", file=sys.stderr)
            return dash.no_update
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to FastAPI server. Ensure it is running.", file=sys.stderr)
        return dash.no_update
    except Exception as e:
        print(f"An unexpected error occurred during fetch: {e}", file=sys.stderr)
        return dash.no_update


# --- Run the Dash App ---
if __name__ == '__main__':
    # You run this file now, not dashboard.py
    app.run_server(debug=True, host='127.0.0.1', port=8050)