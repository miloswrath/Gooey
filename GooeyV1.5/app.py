import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuration")
        self.geometry("600x400")
        

        self.variables = {
            "User Email": tk.StringVar(), 
            "BIDS Directory": tk.StringVar(),
            "fmriprep Container Directory": tk.StringVar(),
            "fmriprep Job File Output Directory": tk.StringVar(),
            "fmriprep Output Directory": tk.StringVar(),
            "fmriprep Error Output Directory": tk.StringVar(),
            "fmriprep Freesurfer License Directory": tk.StringVar(),
            "xcp-d Container Directory": tk.StringVar(),
            "xcp-d Job File Output Directory": tk.StringVar(),
            "xcp-d Output Directory": tk.StringVar(),
            "xcp-d Error Output Directory": tk.StringVar(),
        }

        self.setup_input_fields()  # call to setup input fields
        self.setup_display()  # call to setup display
        self.load_config()

    def setup_input_fields(self):
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y")

        row = 0
        for name, var in self.variables.items():

            ttk.Label(left_frame, text=name.replace('_', ' ').title() + ":").grid(row=row, column=0, sticky=tk.W)
            ttk.Entry(left_frame, textvariable=var).grid(row=row, column=1, sticky=tk.EW)
            # Bind the variable to update the display whenever its value changes
            var.trace_add("write", lambda name, index, mode, var=var: self.update_display())
            row += 1

        # Save button
        ttk.Button(left_frame, text="Save Configuration", command=self.save_config).grid(row=row, column=0, columnspan=2, pady=10)
    def setup_display(self):
        self.display = scrolledtext.ScrolledText(self, state='disabled')
        self.display.pack(side="right", fill="both", expand=True)

    def save_config(self):
        config_data = {name: var.get() for name, var in self.variables.items()}
        with open("config.json", "w") as file:
            json.dump(config_data, file, indent=4)
        messagebox.showinfo("Info", "Configuration saved.")

    def update_display(self):
        # Extract variables from self.variables
        user_email = self.variables["User Email"].get()
        fmriprep_container_dir = self.variables["fmriprep Container Directory"].get()
        bids_dir = self.variables["BIDS Directory"].get()
        fmriprep_out_dir = self.variables["fmriprep Output Directory"].get()
        fmriprep_error_out_dir = self.variables["fmriprep Error Output Directory"].get()
        fmriprep_freesurfer_license_dir = self.variables["fmriprep Freesurfer License Directory"].get()
        fmriprep_job_file_out_dir = self.variables["fmriprep Job File Output Directory"].get()
        xcpd_container_dir = self.variables["xcp-d Container Directory"].get()
        xcpd_error_out_dir = self.variables["xcp-d Error Output Directory"].get()
        xcpd_out_dir = self.variables["xcp-d Output Directory"].get()
        xcpd_job_file_out_dir = self.variables["xcp-d Job File Output Directory"].get()
        
        # Create the fmriscript
        fmriscript_template = f"""#!/bin/bash
        #$ -pe smp 56
        #$ -q UI
        #$ -m bea
        #$ -M {user_email}
        #$ -j y
        #$ -o {fmriprep_out_dir}
        #$ -e {fmriprep_error_out_dir}a
        OMP_NUM_THREADS=10
        singularity run --cleanenv -H $HOME/singularity_home -B /Shared/vosslabhpc:/mnt \\
        /{fmriprep_container_dir} \\
        /{bids_dir} \\
        /{fmriprep_out_dir} \\
        participant --participant_label SUBJECT WILL GO HERE \\
        --dummy-scans 5 \\
        -f 0.5 \\
        --license /{fmriprep_freesurfer_license_dir} \\
        --atlases 4S456Parcels
        #path: {fmriprep_job_file_out_dir}
        """
        # Create the xcpdscript
        xcpdscript_template = f"""#!/bin/bash
        #$ -pe smp 56
        #$ -q UI
        #$ -m bea
        #$ -M {user_email}
        #$ -j y
        #$ -e {xcpd_error_out_dir}
        #$ -o {xcpd_out_dir}

        singularity run -B /Users/bmadero/xcpEngine/utils:/xcpEngine/utils \\
        -H /Users/bmadero/singularity_home \\
        /{xcpd_container_dir} \\
        /{fmriprep_out_dir} \\
        -d /Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/code/xcp/job_scripts/day1pre/fc-acompcor.dsn \\
        --participant_label SUBJECT WILL GO HERE \\
        -o {xcpd_out_dir} \\
        -t 2 -r /Shared/vosslabhpc/Projects/BikeExtend/3-Experiment/2-Data/BIDS/derivatives/
        #path: {xcpd_job_file_out_dir}
        """
        # Display the scripts in the display area
        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, "fmriscript\n\n")
        self.display.insert(tk.END, fmriscript_template)
        self.display.insert(tk.END, "\n\nxcpdscript\n\n")
        self.display.insert(tk.END, xcpdscript_template)
        self.display.config(state='disabled')

    
    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                file_content = file.read()
                if file_content:
                    config_data = json.loads(file_content)
                    if config_data:
                        for name, value in config_data.items():
                            if name in self.variables:
                                self.variables[name].set(value)


if __name__ == "__main__":
    app = Application()
    app.mainloop()