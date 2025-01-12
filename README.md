
# Interactive Map Tool

This tool is a simple yet useful interactive map for visualizing and comparing hydropower plant data. It provides an intuitive interface for exploring hydropower plant details and comparing various operational indices.

## Features

- Visualize hydropower plant locations on an interactive map.
- Select specific hydropower plants to view their detailed parameters and operational data.
- Compare indices such as:
  - Usable Storage Index (USI)
  - Elevation Range Index (ERI)
  - Flexibility Index (FI)
  - Head Efficiency Index (HEI)
  - Flow Management Index (FMI)
  - Energy Storage Index (ESI)
- Toggle between different data views and indices using an interactive interface.

## Requirements

To run this tool, the following dependencies must be installed:

- `pandas`
- `numpy`
- `dash`
- `dash-split-pane`
- `folium`
- `openpyxl`
- `plotly`
- `gunicorn`

### Install dependencies

You can install these libraries using the following command:

```bash
pip install -r requirements.txt
```

Ensure the `requirements.txt` file in your repository includes:

```
pandas==1.5.3
numpy==1.24.3
dash==2.12.1
dash-split-pane==1.0.0
gunicorn==20.1.0
folium==0.14.0
openpyxl==3.1.2
plotly==5.15.0
```

## How to Use

### 1. Running the Tool

1. Clone the repository and navigate to the directory:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```
2. Install the required dependencies using the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   python app.py
   ```
4. Open a web browser and go to `http://127.0.0.1:8050` to access the tool.

### 2. Exploring the Map

- Use the map interface to view the locations of hydropower plants.
- Click on a plant marker to view detailed parameters and operational indices.
- Toggle between detailed views of parameters and indices.

### 3. Comparing Plants

- Use the dropdown menu to select specific hydropower plants for comparison.
- View bar charts comparing the operational indices for the selected plants.

## Deployment

This tool can be deployed using a platform like Heroku. Ensure the following files are included in the repository for deployment:

- `Procfile`: Specifies the web server command (e.g., `web: gunicorn app:server`).
- `runtime.txt`: Specifies the Python runtime version (e.g., `python-3.9.12`).

To deploy to Heroku:

1. Install the Heroku CLI.
2. Log in to your Heroku account:
   ```bash
   heroku login
   ```
3. Create a new Heroku app:
   ```bash
   heroku create app-name
   ```
4. Deploy the app:
   ```bash
   git push heroku main
   ```

## Limitations

- The tool currently supports only the parameters included in the uploaded Excel file.
- Ensure the data file (`data/New improved table.xlsx`) is structured correctly for seamless integration.

## Contributing

If you encounter any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
