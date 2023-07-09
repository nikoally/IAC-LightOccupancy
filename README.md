# Data Processing and Analysis Tool for Light On/Off and Occupancy Sensor Data

## Overview
This is a simple GUI tool that enables users to load, process, and analyze CSV data files and export the results in JSON and CSV format along with graphs. It is implemented using Python with tkinter for the GUI and other libraries for data manipulation and plotting.

The application contains two tabs: "Process Data" and "Analyze Data". 

- The "Process Data" tab allows users to select a project directory, CSV files to process, and then process and export these files after entering additional information. 
- The "Analyze Data" tab allows users to select and load a JSON file. More functions will be implemented over time. 

## Features
- Select a directory for project data and automatically create necessary subfolders.
- Select multiple CSV files for processing.
- Process selected CSV files by entering custom names and associated wattage for each file.
- Export processed data to the project directory as CSV and JSON files.
- Generate and export a graph for each CSV file processed, which shows light and occupancy over time.
- Load JSON files for analysis.

## Usage

```python
# To start the application, simply run the script using Python
python3 script_name.py
```

The application will open a new window. Start by selecting a project directory and then CSV files to process. You can then process and export the data.

When selecting a directory, you will be prompted to enter a site number. For each file selected, you will be asked to enter a friendly name and wattage for the file. These are used in the processing and export of the data.

The export functionality also asks for a start date/time in the format 'YYYY-MM-DD HH:MM:SS'. It then processes each file, generating a graph and saving it to a 'graphs' folder in the project directory. It also saves processed data as a CSV file in a 'data' folder, and as a JSON file named with the site number in the main project directory.

You can also use the "Analyze Data" tab to select a JSON file for analysis. As of now, it only displays a message box showing the selected file.

## Dependencies
- Python 3
- tkinter
- pandas
- matplotlib
- numpy
- python-dateutil
- json
- csv

## Future Work
While the application already has useful functionality, there is room for improvement and further development. Some potential future features could include:

- Implementing actual analysis of loaded JSON files.
- Automatic generation of reports
- Adding more advanced data processing and analysis capabilities.
- Refining the interface and user experience.


## License
This project is open-source, feel free to use, distribute or contribute to this project.
