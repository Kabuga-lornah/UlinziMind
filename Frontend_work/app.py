import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import sys

# Import the layouts from the new files
from auth_layout import auth_layout
from dashboard import dashboard_layout, ALERTS_URL 

# --- Configuration ---
REFRESH_INTERVAL_MS = 5000 
EXTERNAL_STYLESHEETS = [dbc.themes.SLATE] 

# --- Dash App Setup ---
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, title='UlinziMind AI Sentinel')
app.config.suppress_callback_exceptions = True # <<< ADDED THIS LINE

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
    dcc.Store(id='raw-data-store'),
    dcc.Store(id='jwt-token-store', data=None), 
    dcc.Store(id='navigation-store', data={'page': 'login'}),
    
    dcc.Interval(
        id='interval-component',
        interval=REFRESH_INTERVAL_MS, 
        n_intervals=0,
        disabled=True 
    ),

    # Main content area (Router Output)
    html.Div(id='page-content', children=[auth_layout]) 
])


# --- 1. Router Logic: Switch between Auth and Dashboard ---
@app.callback(
    Output('page-content', 'children'),
    Output('interval-component', 'disabled', allow_duplicate=True),
    Input('jwt-token-store', 'data'),
    prevent_initial_call='initial_duplicate' 
)
def route_to_page(token):
    if token is None:
        return auth_layout, True
    else:
        return dashboard_layout, False

# --- 2. Data Fetching: Use Token in Header ---
@app.callback(
    Output('raw-data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('jwt-token-store', 'data'), 
    prevent_initial_call=True
)
def fetch_data(n, token): 
    """Fetches data from the protected FastAPI endpoint with authentication."""
    
    if token is None:
        return dash.no_update
        
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(ALERTS_URL, params={'count': 20}, headers=headers) 
        response.raise_for_status() 
        data = response.json()
        df = pd.DataFrame(data)
        return df.to_dict('records')
    except requests.exceptions.HTTPError as e:
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
    app.run(debug=True, host='127.0.0.1', port=8050)