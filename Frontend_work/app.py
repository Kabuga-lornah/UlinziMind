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

# --- Firebase Configuration (REMOVED) ---
# FIREBASE_CONFIG is no longer needed.


# --- Dash App Setup ---
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, title='UlinziMind AI Sentinel')

# --- Inject Firebase SDK via Custom Index HTML (REMOVED) ---
# Revert to the default index string to ensure no custom JS interferes.
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body>
        <div id="react-entry-point">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""


# --- Main Layout Definition (Global Stores and Router) ---
app.layout = html.Div(style={'backgroundColor': '#1C1C1C', 'minHeight': '100vh', 'padding': '10px'}, children=[
    # Global State Stores
    dcc.Store(id='raw-data-store'), # Data fetched from the protected API
    # dcc.Store(id='jwt-token-store', data=None), # REMOVED: No more token
    # dcc.Store(id='navigation-store', data={'page': 'login'}), # REMOVED: No more navigation state
    
    dcc.Interval(
        id='interval-component',
        interval=REFRESH_INTERVAL_MS, 
        n_intervals=0,
        disabled=False # Set to False for immediate data fetching
    ),

    # Main content area (Router Output)
    html.Div(id='page-content', children=[dashboard_layout]) # Directly render the dashboard
])


# --- 1. Clientside Callbacks to Run Firebase Auth JS (REMOVED) ---
# All clientside_callback blocks are removed as they are no longer functional.


# --- 2. Main Router Logic (REMOVED/SIMPLIFIED) ---
# Since we are always showing the dashboard, the routing callback is removed.
# The layout is directly set in app.layout.


# --- 3. Data Fetching (MODIFIED) ---
@app.callback(
    Output('raw-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    # State('jwt-token-store', 'data'), # REMOVED: No more token state
)
# Note: The function signature must be updated to remove the 'token' argument.
def fetch_data(n): 
    """Fetches data from the protected FastAPI endpoint without authentication."""
    
    # Prepare the Authorization header (REMOVED)
    headers = {}
    
    try:
        # The mock API in main.py does not require headers, so we call it directly.
        response = requests.get(ALERTS_URL, params={'count': 20}, headers=headers) 
        response.raise_for_status() 
        data = response.json()
        df = pd.DataFrame(data)
        return df.to_dict('records')
    except requests.exceptions.HTTPError as e:
        # 401 Unauthorized handling is no longer relevant here.
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
    app.run(debug=True, host='127.0.0.1', port=8050)