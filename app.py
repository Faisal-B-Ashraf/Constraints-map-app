import pandas as pd
import folium
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_split_pane  # For draggable layout

# File path
FILE_PATH = "data/New improved table.xlsx"



# Read the Excel data
data = pd.read_excel(FILE_PATH)

# Helper functions
def validate_coordinates(data, dam_columns):
    valid_coords, invalid_coords = {}, {}
    coordinate_row_index = 2
    coordinates = data.loc[coordinate_row_index, dam_columns]
    for dam, coord in coordinates.items():
        try:
            lat, lon = map(float, str(coord).split(","))
            valid_coords[dam] = (lat, lon)
        except Exception:
            invalid_coords[dam] = coord
    return valid_coords, invalid_coords

def preprocess_value(value):
    try:
        if "-" in str(value):
            low, _ = map(lambda x: float(x.replace(",", "").strip()), value.split("-"))
            return low
        return float(str(value).replace(",", "").strip())
    except:
        return None

def calculate_indices(row):
    try:
        row = row.apply(preprocess_value)
        usi = (
            round(row['Usable Storage Capacity (acre-feet)'] / row['Storage Volume (acre-feet)'], 2)
            if row['Storage Volume (acre-feet)'] and row['Usable Storage Capacity (acre-feet)']
            else "N/A"
        )
        eri = (
            round(row['Maximum Pool Elevation (feet)'] - row['Minimum Pool Elevation (feet)'], 2)
            if row['Maximum Pool Elevation (feet)'] and row['Minimum Pool Elevation (feet)']
            else "N/A"
        )
        fi = (
            round(row['Maximum Daily Fluctuation (feet)'] / row['Ramping Rate (feet/hour)'], 2)
            if row['Ramping Rate (feet/hour)'] and row['Maximum Daily Fluctuation (feet)']
            else "N/A"
        )
        avg_head = row['Power Head (feet)'] if row['Power Head (feet)'] else "N/A"
        hei = (
            round(avg_head / row['Maximum Pool Elevation (feet)'], 2)
            if avg_head and row['Maximum Pool Elevation (feet)']
            else "N/A"
        )
        fmi = (
            round(row['Minimum Flow (cfs)'] / row['Annual Flow Mean (m³/s)'], 2)
            if row['Minimum Flow (cfs)'] and row['Annual Flow Mean (m³/s)']
            else "N/A"
        )
        esi = (
            round(row['Energy Output (MWh)'] / row['Storage Volume (acre-feet)'], 2)
            if row['Energy Output (MWh)'] and row['Storage Volume (acre-feet)']
            else "N/A"
        )
        return {
            'Usable Storage Index': usi,
            'Elevation Range Index': eri,
            'Flexibility Index': fi,
            'Head Efficiency Index': hei,
            'Flow Management Index': fmi,
            'Energy Storage Index': esi
        }
    except Exception as e:
        print(f"Error calculating indices: {e}")
        return {
            'Usable Storage Index': "Error",
            'Elevation Range Index': "Error",
            'Flexibility Index': "Error",
            'Head Efficiency Index': "Error",
            'Flow Management Index': "Error",
            'Energy Storage Index': "Error"
        }

def create_map_with_parameters(data, valid_coords, selected_plants):
    m = folium.Map(location=[46.5, -120.5], zoom_start=6)
    for dam, coord in valid_coords.items():
        try:
            marker_color = "red" if dam in selected_plants else "blue"
            dam_data = data.loc[:, [dam, dam.replace("(Representative Value)", "(Notes)")]]
            dam_row = data.set_index("Parameter")[dam]
            indices = calculate_indices(dam_row)

            # Tab 1: Dam Details
            dam_popup_content = f"""
            <b>{dam.split(" (Representative Value)")[0]}</b><br>
            <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
                <thead>
                    <tr>
                        <th>Parameter (Units)</th>
                        <th>Value</th>
                        <th>Notes</th>
                    </tr>
                </thead>
                <tbody>
            """
            for param, value, notes in zip(data['Parameter'], dam_data[dam], dam_data[dam.replace("(Representative Value)", "(Notes)")]):
                dam_popup_content += f"""
                    <tr>
                        <td>{param}</td>
                        <td>{value}</td>
                        <td>{notes}</td>
                    </tr>
                """
            dam_popup_content += """
                </tbody>
            </table>
            """

            # Tab 2: Indices Details
            indices_popup_content = f"""
            <b>{dam.split(" (Representative Value)")[0]} - Indices</b><br>
            <table border="1" style="border-collapse: collapse; width: 100%; text-align: left;">
                <thead>
                    <tr>
                        <th>Index</th>
                        <th>Value</th>
                        <th>Explanation</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Usable Storage Index</td><td>{indices['Usable Storage Index']}</td><td>USI = Usable Storage Capacity / Storage Volume</td></tr>
                    <tr><td>Elevation Range Index</td><td>{indices['Elevation Range Index']}</td><td>ERI = Maximum Pool Elevation - Minimum Pool Elevation</td></tr>
                    <tr><td>Flexibility Index</td><td>{indices['Flexibility Index']}</td><td>FI = Maximum Daily Fluctuation / Ramping Rate</td></tr>
                    <tr><td>Head Efficiency Index</td><td>{indices['Head Efficiency Index']}</td><td>HEI = Avg Power Head / Max Pool Elevation</td></tr>
                    <tr><td>Flow Management Index</td><td>{indices['Flow Management Index']}</td><td>FMI = Min Flow / Annual Flow Mean</td></tr>
                    <tr><td>Energy Storage Index</td><td>{indices['Energy Storage Index']}</td><td>ESI = Energy Output / Storage Volume</td></tr>
                </tbody>
            </table>
            """

            # Toggleable Tabs in Popup
            combined_popup_content = f"""
            <div id="popup-content">
                <div id="dam-details" style="display: block;">
                    {dam_popup_content}
                    <button onclick="document.getElementById('dam-details').style.display='none'; 
                                     document.getElementById('indices-details').style.display='block';">
                        View Indices
                    </button>
                </div>
                <div id="indices-details" style="display: none;">
                    {indices_popup_content}
                    <button onclick="document.getElementById('indices-details').style.display='none'; 
                                     document.getElementById('dam-details').style.display='block';">
                        View Dam Details
                    </button>
                </div>
            </div>
            """

            folium.Marker(
                location=coord,
                popup=folium.Popup(combined_popup_content, max_width=600),
                icon=folium.Icon(color=marker_color, icon="info-sign")
            ).add_to(m)
        except Exception as e:
            print(f"Error processing dam {dam}: {e}")

    # Add a legend (hard-coded as Folium doesn't have built-in legend support)
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 90px; 
                background-color: white; z-index:9999; font-size:14px;
                border:1px solid grey; padding: 10px;">
        <b>Legend</b><br>
        <i class="fa fa-map-marker" style="color:red"></i> Selected Plant<br>
        <i class="fa fa-map-marker" style="color:blue"></i> Other Plant
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m

# Extract dam columns
dam_columns = [col for col in data.columns if "(Representative Value)" in col]
valid_coords, invalid_coords = validate_coordinates(data, dam_columns)

# Dash App
app = Dash(__name__)

app.layout = dash_split_pane.DashSplitPane(
    children=[
        html.Div([
            html.H1("Hydropower Plant Analysis Tool"),
            dcc.Dropdown(
                id='plant-selector',
                options=[{'label': dam, 'value': dam} for dam in valid_coords.keys()],
                multi=True,
                placeholder="Select plants to compare"
            ),
            dcc.Graph(id='comparison-graph')
        ]),
        html.Div([
            html.Iframe(id='map-view', width='100%', height='100%')
        ], style={'height': '100%', 'padding': '10px'})
    ],
    id="split-pane",
    split="horizontal",
    size="50%"
)

@app.callback(
    Output('comparison-graph', 'figure'),
    [Input('plant-selector', 'value')]
)
def update_comparison_graph(selected_dams):
    if not selected_dams:
        return px.bar(title="Select plants to compare")

    comparison_data = []
    for dam in selected_dams:
        row = data.set_index("Parameter")[dam]
        indices = calculate_indices(row)
        comparison_data.append({'Plant': dam, **indices})

    df = pd.DataFrame(comparison_data)

    fig = px.bar(
        df, x='Plant', y=list(comparison_data[0].keys())[1:], title="Comparison of Indices", barmode='group'
    )
    return fig

@app.callback(
    Output('map-view', 'srcDoc'),
    [Input('plant-selector', 'value')]
)
def update_map(selected_dams):
    m = create_map_with_parameters(data, valid_coords, selected_dams or [])
    return m._repr_html_()  # Render map HTML directly

if __name__ == '__main__':
    app.run_server(debug=True)
# Add this line:
server = app.server  # Expose the Flask server for deployment