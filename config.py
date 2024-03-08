import os 
import json
import tkinter as tk
from tkinter import messagebox


class ConfigDialog(tk.Toplevel):
    def __init__(self, parent, project_dir, project_name):
        super().__init__(parent)
        self.project_dir = project_dir
        self.project_name = project_name
        self.title("Configuration Details")

        # Create StringVars
        self.bids_dir_var = tk.StringVar()
        self.fmriprep_container_dir_var = tk.StringVar()
        self.fmriprep_job_file_out_dir_var = tk.StringVar()
        self.fmriprep_out_dir_var = tk.StringVar()
        self.fmriprep_error_out_dir_var = tk.StringVar()
        self.fmriprep_freesurfer_license_dir_var = tk.StringVar()
        self.xcpd_container_dir_var = tk.StringVar()
        self.xcpd_job_file_out_dir_var = tk.StringVar()
        self.xcpd_out_dir_var = tk.StringVar()
        self.xcpd_error_out_dir_var = tk.StringVar()

        # Create and place labels and entry fields in the dialog
        fields = [
            ("BIDS Directory", self.bids_dir_var),
            ("fmriprep Container Directory", self.fmriprep_container_dir_var),
            # Add the rest of your fields here
        ]

        for i, (label, var) in enumerate(fields):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="e")
            tk.Entry(self, textvariable=var).grid(row=i, column=1)

        # Submit button
        tk.Button(self, text="Save Configuration", command=self.save_config).grid(row=len(fields), column=0, columnspan=2)

    def save_config(self):
        config_data = {
            "bids_dir": self.bids_dir_var.get(),
            "fmriprep_container_dir": self.fmriprep_container_dir_var.get(),
            # Add the rest of your variables here
        }
        config_file_path = os.path.join(self.project_dir, f"{self.project_name}_config.json")
        with open(config_file_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        self.destroy()  # Close the dialog

def ask_for_config_and_save(self, project_name, project_dir):
    # Open the configuration dialog
    ConfigDialog(self, project_dir, project_name)
    
    # Save the configuration to a JSON file within the project's director
    messagebox.showinfo("Success", "Configuration saved successfully.")