import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests
# --- NEW: Dash Bootstrap Components for professional layout ---
import dash_bootstrap_components as dbc 

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/api/v1/alerts" 
REFRESH_INTERVAL_MS = 5000 
EXTERNAL_STYLESHEETS = [dbc.themes.SLATE] # Dark, modern theme for security dashboard

# --- Dash App Setup ---
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, title='UlinziMind AI Sentinel')

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

# --- Layout Definition ---
app.layout = dbc.Container(fluid=True, children=[
    html.H1("🇰🇪 UlinziMind AI Sentinel: Real-Time Intelligence", 
            className="text-center my-4 text-primary"),
    
    # 1. KPI Row (Total Alerts, Max Risk, Peace Protocol Active)
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
    
    # Hidden component to trigger the refresh interval and store raw data
    dcc.Interval(
        id='interval-component',
        interval=REFRESH_INTERVAL_MS, 
        n_intervals=0
    ),
    dcc.Store(id='raw-data-store'),
])

# --- Callback: Fetch Data from FastAPI and Store ---
@app.callback(
    Output('raw-data-store', 'data'),
    [Input('interval-component', 'n_intervals')]
)
def fetch_data(n):
    try:
        response = requests.get(API_URL, params={'count': 20}) # Fetch more data points
        response.raise_for_status() 
        data = response.json()
        df = pd.DataFrame(data)
        return df.to_dict('records') # Store data as a list of dicts
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to FastAPI server.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during fetch: {e}")
        return []

# --- Callback: Update KPIs and Map/Table based on Filters ---
@app.callback(
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
    if not data:
        return (make_kpi_card("Total Alerts", "N/A", "danger", "triangle-exclamation"),) * 3 + (px.scatter_mapbox(zoom=5, center={"lat": 0, "lon": 37}, mapbox_style="carto-darkmatter"), html.Div("No data available from API."))

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

# --- Run the Dash App ---
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)