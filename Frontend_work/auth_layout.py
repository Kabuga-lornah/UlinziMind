import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc 
import dash.exceptions
from dashboard import dashboard_layout 

# --- Layout Components ---

# Form for User Registration (Sign Up)
register_form = dbc.Card([
    dbc.CardHeader(html.H4("New User Registration", className="text-primary")),
    dbc.CardBody([
        html.P("Create an account to access the UlinziMind AI Sentinel.", className="card-text text-muted"),
        dcc.Input(id="reg-email-input", placeholder="Email", type="email", className="mb-3 form-control"),
        dcc.Input(id="reg-password-input", placeholder="Password (min 6 characters)", type="password", className="mb-3 form-control"),
        dbc.Button("Register", id="register-button", color="info", className="w-100 mb-3"),
        html.Div(id="register-status-js", className="mt-2 text-danger"),
        html.Div(id="register-status-py", className="mt-2 text-light"),
        dbc.Button("Already registered? Go to Log In", id="to-login-button", color="link", className="mt-3 w-100"),
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
        html.Div(id="login-status-js", className="mt-2 text-danger"),
        html.Div(id="login-status-py", className="mt-2 text-light"),
        dbc.Button("Go to Register", id="to-register-button", color="link", className="mt-3 w-100"),
    ]),
])

# Main Authentication Layout
auth_layout = dbc.Container([
    # Hidden Dcc.Store
    dcc.Store(id='login-data-store'), 
    dcc.Store(id='register-data-store'),
    
    dbc.Row(dbc.Col(html.H2("UlinziMind Sentinel Access", className="text-center text-primary my-5"))),
    
    # FIX: Include both conditional buttons hidden in the initial layout
    # This guarantees the IDs exist for the 'handle_auth_logic' callback's Inputs.
    html.Div([
        dbc.Button("Go to Log In", id="to-login-button", color="link"),
        dbc.Button("Go to Register", id="to-register-button", color="link")
    ], style={'display': 'none'}),
    
    # Toggle between Login and Register Forms
    dbc.Row(justify="center", children=[
        dbc.Col(md=6, children=[
            html.Div(id='auth-form-content', children=login_form) # Initial children set to login form
        ])
    ])
], fluid=False, className="h-100 align-items-center")


# --- Callbacks for Authentication and Navigation ---

@callback(
    Output('auth-form-content', 'children', allow_duplicate=True),
    Output('jwt-token-store', 'data', allow_duplicate=True), 
    Output('login-status-py', 'children', allow_duplicate=True), 
    Input('to-register-button', 'n_clicks'),
    Input('to-login-button', 'n_clicks'),
    Input('login-button', 'n_clicks'),
    State('login-email-input', 'value'),
    State('login-password-input', 'value'),
    prevent_initial_call='initial_duplicate' 
)
def handle_auth_logic(to_reg_clicks, to_login_clicks, login_clicks, email, password):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'initial_load'

    # 1. Handle Form Switching
    if trigger_id == 'to-register-button':
        return register_form, dash.no_update, dash.no_update
    
    if trigger_id == 'to-login-button':
        return login_form, dash.no_update, dash.no_update
    
    if trigger_id == 'initial_load':
        # This handles the initial loading of the login form
        return login_form, dash.no_update, dash.no_update

    # 2. Handle Mock Login Attempt
    if trigger_id == 'login-button':
        if not email or not password:
             return login_form, dash.no_update, dbc.Alert("Please enter email and password.", color="warning")

        # Mock Authentication Logic (Credentials: user@example.com / password)
        if email == "user@example.com" and password == "password":
            mock_token = "MOCK_JWT_TOKEN_ULINZI_SENTINEL"
            return dash.no_update, mock_token, dbc.Alert("Login successful! Redirecting...", color="success")
        else:
            return login_form, None, dbc.Alert("Invalid email or password. Please try again.", color="danger")
            
    # Fallback
    raise dash.exceptions.PreventUpdate