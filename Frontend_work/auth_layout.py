import dash
from dash import dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc 
import dash.exceptions # Import exceptions for clarity

# --- Layout Components ---

# Form for User Registration (Sign Up)
register_form = dbc.Card([
    dbc.CardHeader(html.H4("New User Registration", className="text-primary")),
    dbc.CardBody([
        html.P("Create an account to access the UlinziMind AI Sentinel.", className="card-text text-muted"),
        dcc.Input(id="reg-email-input", placeholder="Email", type="email", className="mb-3 form-control"),
        dcc.Input(id="reg-password-input", placeholder="Password (min 6 characters)", type="password", className="mb-3 form-control"),
        dbc.Button("Register", id="register-button", color="info", className="w-100 mb-3"),
        html.Div(id="register-status-js", className="mt-2 text-danger"), # JS updates for Firebase errors
        html.Div(id="register-status-py", className="mt-2 text-light"), # Python updates (e.g., success message)
    ]),
])

# Form for User Login (Sign In)
login_form = dbc.Card([
    dbc.CardHeader(html.H4("User Sign In", className="text-primary")),
    dbc.CardBody([
        html.P("Already registered? Enter your credentials below.", className="card-text text-muted"),
        dcc.Input(id="login-email-input", placeholder="Email", type="email", className="mb-3 form-control"),
        dcc.Input(id="login-password-input", placeholder="Password", type="password", className="mb-3 form-control"),
        dbc.Button("Log In", id="login-button", color="primary", className="w-100 mb-3"),
        html.Div(id="login-status-js", className="mt-2 text-danger"), # JS updates for Firebase errors
        html.Div(id="login-status-py", className="mt-2 text-light"), # Python updates (e.g., loading message)
        dbc.Button("Go to Register", id="to-register-button", color="link", className="mt-3 w-100"),
    ]),
])

# Main Authentication Layout
auth_layout = dbc.Container([
    # Hidden Dcc.Store to hold credentials and trigger JS callbacks
    dcc.Store(id='login-data-store'), 
    dcc.Store(id='register-data-store'),
    # Note: jwt-token-store is defined in app.py

    dbc.Row(dbc.Col(html.H2("UlinziMind Sentinel Access", className="text-center text-primary my-5"))),
    
    # Toggle between Login and Register Forms
    dbc.Row(justify="center", children=[
        dbc.Col(md=6, children=[
            html.Div(id='auth-form-content')
        ])
    ])
], fluid=False, className="h-100 align-items-center")


# --- Callbacks for Navigation and Preparation (ALL AUTHENTICATION LOGIC REMOVED) ---

# All three callbacks below rely on IDs that are not present when the dashboard is visible.
# Commenting them out resolves the "ID not found in layout" errors.

# @callback(
#     Output('auth-form-content', 'children'),
#     Input('to-register-button', 'n_clicks'),
#     Input('to-login-button', 'n_clicks'),
#     State('jwt-token-store', 'data')
# )
# def render_auth_form(to_reg_clicks, to_login_clicks, token):
#     """Controls which form (Login or Register) is visible."""
#     # This callback relies on 'to-register-button', 'to-login-button', and 'auth-form-content'.
#     raise dash.exceptions.PreventUpdate


# @callback(
#     Output('login-data-store', 'data'),
#     Output('login-status-py', 'children'),
#     Input('login-button', 'n_clicks'),
#     State('login-email-input', 'value'),
#     State('login-password-input', 'value'),
#     prevent_initial_call=True
# )
# def prepare_login_data(n_clicks, email, password):
#     """Captures login inputs and stores them to trigger the JS callback."""
#     # This callback relies on 'login-button'.
#     raise dash.exceptions.PreventUpdate


# @callback(
#     Output('register-data-store', 'data'),
#     Output('register-status-py', 'children'),
#     Input('register-button', 'n_clicks'),
#     State('reg-email-input', 'value'),
#     State('reg-password-input', 'value'),
#     prevent_initial_call=True
# )
# def prepare_register_data(n_clicks, email, password):
#     """Captures registration inputs and stores them to trigger the JS callback."""
#     # This callback relies on 'register-button'.
#     raise dash.exceptions.PreventUpdate