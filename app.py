import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog
from tkinter import messagebox
from dateutil.parser import parse as parse_datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import json
import csv
import pandas as pd
import numpy as np

class Application(ttk.Notebook):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill = "both", expand = "true")
        self.create_widgets()
        self.outputdict = {}
        self.friendly_names = []

    def create_widgets(self):
        # Process Data tab
        self.process_data_tab = ttk.Frame(self)
        self.add(self.process_data_tab, text='Process Data')

        self.open_directory_button = ttk.Button(self.process_data_tab, text="Select Project Directory", command=self.load_directory)
        self.open_directory_button.grid(row=0, column=1, pady=10, padx = 10, sticky = "nsew")
    
        self.select_files_button = ttk.Button(self.process_data_tab, text="Select CSV Files", command=self.load_files)
        self.select_files_button.grid(row=0, column=0, pady=10, padx = 10, sticky = "nsew")
        
        self.file_listbox = tk.Listbox(self.process_data_tab)
        self.file_listbox.grid(row=1, column=0, pady=10, padx = 10, sticky = "nsew")

        self.directory_listbox = tk.Listbox(self.process_data_tab)
        self.directory_listbox.grid(row=1, column=1, pady=10, padx = 10, sticky = "nsew")

        self.process_button = ttk.Button(self.process_data_tab, text="Process", command=self.process_files)
        self.process_button.grid(row=2, column=0, pady=10, padx = 10, sticky = "nsew")

        self.export_button = ttk.Button(self.process_data_tab, text="Export", command=self.export_data)
        self.export_button.grid(row=2, column=1, pady=10, padx = 10, sticky = "nsew")

        #Configure Rows and Columns for Dynamic App Resizing
        self.process_data_tab.grid_columnconfigure(0, weight=1)
        self.process_data_tab.grid_columnconfigure(1, weight=1)

        # Analyze Data tab
        self.analyze_data_tab = ttk.Frame(self)
        self.add(self.analyze_data_tab, text='Analyze Data')
        
        self.open_json_button = ttk.Button(self.analyze_data_tab, text="Open JSON", command=self.load_json)
        self.open_json_button.pack(padx=10, pady=10)

    def load_json(self):
        self.json_filename = filedialog.askopenfilename(filetypes=[('JSON Files', '*.json')])
        # Here you could implement the loading and processing of the selected JSON file
        messagebox.showinfo(title="Info", message=f"JSON file {self.json_filename} selected. Implement your loading and processing logic here.")

    def load_directory(self):
        self.project_directory = filedialog.askdirectory()
        for folder in ["graphs", "data"]:
            if not os.path.exists(f'{self.project_directory}/{folder}'):
                os.makedirs(f'{self.project_directory}/{folder}')
                print(f"Created {folder} folder")
            else: 
                print(f"{folder} already exists")
        self.directory_listbox.insert(tk.END, self.project_directory)


    def load_files(self):
        self.filenames = filedialog.askopenfilenames(filetypes=[('CSV Files', '*.csv')])
        self.file_listbox.delete(0, tk.END)
        for file in self.filenames:
            self.file_listbox.insert(tk.END, file)
        
    def process_files(self):
        self.output_dict = {}

        for file in self.filenames:
            self.friendly_name = simpledialog.askstring("Input", f"Enter a friendly name for {file}:")
            self.wattage = simpledialog.askfloat("Input", f"Enter the wattage for {file}:")

            # store the data in the dictionary
            self.output_dict[file] = {'friendly_name': self.friendly_name, 'wattage': self.wattage}

        # print the output_dict to the console for verification
        print(self.output_dict)

    def export_data(self):
        for file, file_data in self.output_dict.items():
            # Read the csv file
            df = pd.read_csv(file, usecols=[0, 1, 2, 3])

            # Change column names to standardized names
            df.columns = ['Index', 'Timestamp', 'Light', 'Occupancy']

            # Drop the index column
            df = df.drop(columns=['Index'])

            # Convert Date Time to datetime and sort by it
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            df.sort_values('Timestamp', inplace=True)

            # Set Timestamp as index
            df.set_index('Timestamp', inplace=True)

            # Resample the dataframe to every second, forward fill missing data
            df = df.resample('S').ffill()
            df['Light'].fillna(method='ffill', inplace=True)
            df['Occupancy'].fillna(method='ffill', inplace=True)

            # Find the rows where Light is on (1.00) and Occupancy is off (0.00)
            df_light_on_no_occupancy = df[(df['Light'] == 1.00) & 
                                        (df['Occupancy'] == 0.00)]

            # Calculate the time difference between consecutive timestamps
            df_light_on_no_occupancy.loc[:, 'Time Difference'] = df_light_on_no_occupancy.index.to_series().diff().dt.total_seconds()


            # Sum up the total time
            total_time = df_light_on_no_occupancy['Time Difference'].sum()

            # Store total time in output_dict
            file_data['total_time_light_on_no_occupancy'] = total_time

            # Save pd to csv
            df.to_csv(f"{self.project_directory}/data/{file_data['friendly_name']}.csv", index=True)
        
            # Make Plot
            plt.figure(figsize=(12, 6))
            plt.plot(df.index, df['Light'], label='Light')
            plt.plot(df.index, df['Occupancy'], label='Occupancy')
            plt.xlabel('Timestamp')
            plt.ylabel('Value')
            plt.title(f"Light and Occupancy over time for {file_data['friendly_name']}")
            plt.legend()
            
            # Save the figure
            plt.savefig(f"{self.project_directory}/graphs/{file_data['friendly_name']}.png")

            # Add figure filepath to dir
            file_data['graph filepath'] = f"graphs/{file_data['friendly_name']}.png"
        
        
        # Dump output_dict to JSON
        self.site_number = simpledialog.askinteger("Input", f"Enter the site number:")
        with open(f'{self.project_directory}/{self.site_number}.json', 'w') as json_file:
            json.dump(self.output_dict, json_file, indent=4)
        print("Successful Export")


root = tk.Tk()
root.geometry('1000x600')
root.title('Data Processing and Analysis')
app = Application(master=root)
app.mainloop()
