import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
from utils import load_session, get_driver_lap_telemetry

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("My Telemetry Dashboard"),
    html.H3("By Nathan Sizer - Details can be found in the GitHub repo for this project."),

    #year dropdown menu, default to 2024 since it's most recent
    html.Label("Season"),
    dcc.Dropdown(id = "year", options=[{'label': str(yr), 'value':yr} for yr in range(2021, 2024)], value = "2024"),

    #race weekend selection, default to Monza since it's a track everyone knows
    html.Label("Grand Prix"),
    dcc.Input(id = "gp", type = "text", value = "Monza"),

    #session selection, default to Quali since it's the quickest
    html.Label("Session"),
    dcc.Dropdown(id = "session", options=[{"label": ss, "value": ss} for ss in ["FP1", "FP2", "FP3", "Q", "R"]], value = "Q"),

    #driver comparison dropdown, default to the best of friends
    html.Label("Drivers to Compare"),
    dcc.Dropdown(
        id = "drivers",
        options = [
            {"label": "Max Verstappen", "value": "VER"},
            {'label': 'Lewis Hamilton', 'value': 'HAM'},
            {'label': 'Charles Leclerc', 'value': 'LEC'}
        ],
        multi = True,
        value = ["VER", "HAM"],
    ),

    #a speed trace graph
    dcc.Graph(id = "speed_trace")
])

#callbacks to update the graph when the user changes things
@app.callback(
    Output('speed-trace', 'figure'),
    Input('year', 'value'),
    Input('gp', 'value'),
    Input('session', 'value'),
    Input('drivers', 'value')
)
def update_graph(year, gp, session, drivers):
    #try to update the graph, otherwise throw an error
    try:
        #load session data
        ses = load_session(year, gp, session)
        traces = []
        #get data for each driver selected
        for drivercode in drivers:
            telemetry = get_driver_lap_telemetry(ses, drivercode)
            traces.append(go.Scatter(x=telemetry['Distance'], y=telemetry['Speed'], mode = "lines", name = drivercode))

        #update the graph using the new date
        fig = go.Figure(data = traces)
        fig.update_layout(
            title = f"Speed Trace for {gp} {session} {year}",
            xaxis_title = "Distance (m)",
            yaxis_title = "Speed (km/h)"
        )
        return fig
    except Exception as e:
        return go.Figure(layout = {"title": f"Error: {str(e)}"})

#run the app
if __name__ == '__main__':
    app.run_server(debug=True)