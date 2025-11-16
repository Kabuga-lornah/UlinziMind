import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc 
import requests 

# --- Configuration (Kept for environment setup) ---
ALERTS_URL = "http://127.0.0.1:8000/api/v1/alerts" 
REFRESH_INTERVAL_MS = 5000 
EXTERNAL_STYLESHEETS = [dbc.themes.SLATE] 

# --- Helper function for creating KPI Cards ---
def make_kpi_card(title, value, color='primary', icon='info-circle'):
    """Creates a standardized card for Key Performance Indicators."""
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title text-muted"),
            html.H2(value, className=f"card-text text-{color}"),
            html.I(className=f"fa-solid fa-{icon}", style={"fontSize": "24px", "position": "absolute", "top": "10px", "right": "10px"}),
        ]),
        className="shadow-sm border-0",
        style={"backgroundColor": "#2e2e2e"} # Slightly lighter than slate background
    )

# --- Main Dashboard Layout Component (The only thing exported) ---
dashboard_layout = dbc.Container(fluid=True, children=[
    # Sign out button and Title
    dbc.Row([
        dbc.Col(html.H1("🇰🇪 UlinziMind AI Sentinel: Real-Time Intelligence", 
            className="text-center my-4 text-primary"), width=10),
        dbc.Col(dbc.Button("Sign Out", id="sign-out-button", color="secondary", className="mt-4"), width=2, className="d-flex justify-content-end")
    ], className="mb-4"),
    
    # 1. KPI Row
    dbc.Row([
        dbc.Col(html.Div(id='kpi-total-alerts')),
        dbc.Col(html.Div(id='kpi-max-risk')),
        dbc.Col(html.Div(id='kpi-peace-active')),
    ], className="mb-4"),

    # 2. Controls and Map Row
    dbc.Row([
        # Left Sidebar for Filters/Controls
        dbc.Col(md=3, children=[
            dbc.Card(dbc.CardBody([
                html.H4("Threat Filters", className="card-title text-light"),
                
                html.Label("Minimum Risk Score:", className="mt-3"),
                dcc.Slider(
                    id='risk-slider',
                    min=0.0, max=1.0, step=0.1, value=0.5,
                    marks={i/10: str(i/10) for i in range(11)},
                    className="mb-4"
                ),
                
                html.Label("Threat Type:", className="mt-2"),
                dcc.Dropdown(
                    id='threat-dropdown',
                    options=[
                        {'label': 'All Threats', 'value': 'ALL'},
                        {'label': 'CRITICAL: Coordinated Threat', 'value': 'CRITICAL'},
                        {'label': 'HIGH: Escalating Unrest/Infiltration', 'value': 'HIGH'},
                        {'label': 'Peaceful Civic Protest', 'value': 'Peaceful'},
                    ],
                    value='ALL',
                    clearable=False,
                    className="mb-4"
                ),
                
            ]), style={"backgroundColor": "#2e2e2e", "border": "none"}),
        ]),

        # Main Area for Map Visualization
        dbc.Col(md=9, children=[
            dcc.Graph(id='live-map', style={'height': '80vh'}),
        ]),
    ], className="mb-4"),

    # 3. Live Alert Table Row
    dbc.Row([
        dbc.Col(html.H4("Detailed Real-Time Alerts", className="text-light mb-3")),
        dbc.Col(md=12, children=[
            html.Div(id='live-alerts-table'),
        ]),
    ], className="mt-4"),
])

# --- Core Visualization Logic (Keep this, just ensure it uses dcc.Store for input) ---
@dash.callback(
    [Output('kpi-total-alerts', 'children'),
     Output('kpi-max-risk', 'children'),
     Output('kpi-peace-active', 'children'),
     Output('live-map', 'figure'),
     Output('live-alerts-table', 'children')],
    [Input('raw-data-store', 'data'),
     Input('risk-slider', 'value'),
     Input('threat-dropdown', 'value')]
)
def update_dashboard_content(data, min_risk, threat_filter):
    # Handle the case where authentication failed or no data is available
    if not data or data is None:
        empty_fig = px.scatter_mapbox(zoom=5, center={"lat": 0, "lon": 37}, mapbox_style="carto-darkmatter")
        empty_fig.update_layout(mapbox_style="carto-darkmatter", paper_bgcolor="#222222", font_color="white")
        
        return (
            make_kpi_card("Total Alerts", "N/A", "danger", "triangle-exclamation"),
            make_kpi_card("Max Risk Score", "0.00", "success", "fire-extinguisher"),
            make_kpi_card("Peace Protocols Active", "0", "success", "hand-holding-heart"),
            empty_fig, 
            html.Div("No data available or authentication required.", className="text-center text-muted p-5")
        )

    df = pd.DataFrame(data)
    
    # --- Apply Filtering ---
    # 1. Risk Score Filter
    df_filtered = df[df['risk_score'] >= min_risk]
    
    # 2. Threat Type Filter
    if threat_filter != 'ALL':
        if threat_filter == 'Peaceful':
             df_filtered = df_filtered[df_filtered['peace_module_flag'] == True]
        else:
             df_filtered = df_filtered[df_filtered['threat_type'].str.contains(threat_filter, case=False)]

    
    # --- KPI Calculation ---
    total_alerts = len(df_filtered)
    max_risk = df_filtered['risk_score'].max() if not df_filtered.empty else 0.0
    peace_active = df_filtered['peace_module_flag'].sum() if not df_filtered.empty else 0

    kpi_alerts = make_kpi_card("Active Alerts (Filtered)", total_alerts, "light", "bell")
    
    max_color = 'danger' if max_risk > 0.8 else 'warning' if max_risk > 0.6 else 'success'
    kpi_risk = make_kpi_card("Max Risk Score", f"{max_risk:.2f}", max_color, "fire-extinguisher")
    
    kpi_peace = make_kpi_card("Peace Protocols Active", peace_active, "success", "hand-holding-heart")

    
    # --- Map Update ---
    fig = px.scatter_mapbox(df_filtered, 
                            lat="latitude", lon="longitude", 
                            color="risk_score", size="risk_score",
                            color_continuous_scale=px.colors.sequential.Reds,
                            hover_data=["threat_type", "recommended_action", "source_type"],
                            zoom=5, center={"lat": 0.0, "lon": 37.0}, 
                            title="Live Predictive Threat Map"
                            )
    
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor="#222222",
        plot_bgcolor="#222222",
        font_color="white",
        coloraxis_colorbar=dict(title="Risk")
    )

    # --- Table Update ---
    table_data = df_filtered[['timestamp', 'threat_type', 'risk_score', 'recommended_action', 'source_type', 'peace_module_flag']]
    
    table = dash_table.DataTable(
        id='datatable-alerts',
        columns=[{"name": i, "id": i} for i in table_data.columns],
        data=table_data.to_dict('records'),
        style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold'},
        style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_data_conditional=[
            {'if': {'filter_query': '{risk_score} > 0.8', 'column_id': 'risk_score'},
             'backgroundColor': '#6A0000', 'color': 'white'},
            {'if': {'filter_query': '{risk_score} > 0.6', 'column_id': 'risk_score'},
             'backgroundColor': '#8B4513', 'color': 'white'},
        ],
        sort_action="native",
        filter_action="native",
        page_action="native",
        page_current=0,
        page_size=10,
    )


    return kpi_alerts, kpi_risk, kpi_peace, fig, table

# We remove the main app.run() block and main layout definition from this file.