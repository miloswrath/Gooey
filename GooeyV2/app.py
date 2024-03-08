import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import json
import os

project_name = ""
project_dir = ""
config_data = {}

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frames = {}
        self.title("Project Management")
        self.geometry("800x600")
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        for F in (HomePage, ProjectPage, FmriPrepPage, XcpdPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

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
            "xcp-d Subject(s)": tk.StringVar(),
            "xcp-d Session": tk.StringVar(),
            "fmriprep Subject(s)": tk.StringVar(),
            "fmriprep Session": tk.StringVar(),
            "fmriprep Dummy Scans": tk.StringVar(),

        }

        self.show_frame("HomePage")


    def setup_input_fields(self):
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y")

        row = 0
        for name, var in self.variables.items():

            ttk.Label(left_frame, text=name.replace('_', ' ').title() + ":").grid(row=row, column=0, sticky=tk.W)
            ttk.Entry(left_frame, textvariable=var).grid(row=row, column=1, sticky=tk.EW)
            # Bind the variable to update the display whenever its value changes
            var.trace_add("write", lambda name, index, mode, var=var: self.update_display(var=var))
            row += 1

    def setup_display(self):
        self.display = scrolledtext.ScrolledText(self, state='disabled')
        self.display.pack(side="right", fill="both", expand=True)

    def save_config(self):
        config_data = {name: var.get() for name, var in self.variables.items()}
        with open("config.json", "w") as file:
            json.dump(config_data, file, indent=4)
        messagebox.showinfo("Info", "Configuration saved.")

    def create_new_project(self):
            global project_name, project_dir, config_data  # Add this line
            project_name = simpledialog.askstring("Project Name", "Enter the name of the new project:")
            if project_name:
                project_dir = os.path.join(os.getcwd(), project_name)
                try:
                    os.makedirs(project_dir)
                    config_file = os.path.join(project_dir, "config.json")
                    with open(config_file, "w") as f:
                        json.dump(config_data, f)
                    messagebox.showinfo("Success", f"Project '{project_name}' created successfully.")
                    #cd into the new project directory
                    os.chdir(project_dir)
                    # Now ask for configurations and save them
                    self.ask_for_config_and_save(project_name, project_dir)
                    #show the project page for this project
                    self.show_frame(ProjectPage)

                except FileExistsError:
                    messagebox.showerror("Error", "Project already exists.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create project: {str(e)}")

    def setup_fmriprep_display(self):

        # Extract variables from self.variables
        user_email = self.variables["User Email"].get()
        fmriprep_container_dir = self.variables["fmriprep Container Directory"].get()
        bids_dir = self.variables["BIDS Directory"].get()
        fmriprep_out_dir = self.variables["fmriprep Output Directory"].get()
        fmriprep_error_out_dir = self.variables["fmriprep Error Output Directory"].get()
        fmriprep_freesurfer_license_dir = self.variables["fmriprep Freesurfer License Directory"].get()
        fmriprep_job_file_out_dir = self.variables["fmriprep Job File Output Directory"].get()
        fmriprep_dummy_scans = self.variables["fmriprep Dummy Scans"].get()
        
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
        --dummy-scans {fmriprep_dummy_scans} \\
        -f 0.5 \\
        --license /{fmriprep_freesurfer_license_dir} \\
        --atlases 4S456Parcels
        #path: {fmriprep_job_file_out_dir}
        """

        
        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, "fmriscript\n\n")
        self.display.insert(tk.END, fmriscript_template)
        self.display.config(state='disabled')
    
    def setup_xcpd_display(self):
        user_email = self.variables["User Email"].get()
        fmriprep_out_dir = self.variables["fmriprep Output Directory"].get()
        xcpd_container_dir = self.variables["xcp-d Container Directory"].get()
        xcpd_error_out_dir = self.variables["xcp-d Error Output Directory"].get()
        xcpd_out_dir = self.variables["xcp-d Output Directory"].get()
        xcpd_job_file_out_dir = self.variables["xcp-d Job File Output Directory"].get()

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
        
        self.display.config(state='normal')
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, "\n\nxcpdscript\n\n")
        self.display.insert(tk.END, xcpdscript_template)
        self.display.config(state='disabled')

    def setup_fmri_input_fields(self, controller):
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y")

        row = 0
        # Set up subject inputs, should be a comma separated list
        ttk.Label(left_frame, text="Subject(s):").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(left_frame, textvariable=self.controller.variables["fmriprep Subject(s)"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1

        # Set up session inputs, should be one string
        ttk.Label(left_frame, text="Session:").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(left_frame, textvariable=self.controller.variables["fmriprep Session"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1

        # Set up dummy scans input
        ttk.Label(left_frame, text="Dummy Scans:").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(left_frame, textvariable=self.controller.variables["fmriprep Dummy Scans"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1
    ...

    def setup_xcpd_input_fields(self, controller):
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y")

        row = 0
        # Set up subject inputs, should be a comma separated list
        ttk.Label(left_frame, text="Subject(s):").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(left_frame, textvariable=self.controller.variables["xcp-d Subject(s)"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1

        # Set up session inputs, should be one string
        ttk.Label(left_frame, text="Session:").grid(row=row, column=0, sticky=tk.W)
        ttk.Entry(left_frame, textvariable=self.controller.variables["xcp-d Session"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1

    
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


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        self.frames[page_name].tkraise()



class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Home Page").pack(pady=10)

        # Widget for add project button
        ttk.Button(self, text="Create New Project", command=controller.create_new_project).pack(pady=10)

        

class ProjectPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Project Page").pack(pady=10)

        # Add widgets to fMRIprep and XCP-d configuration pages
        ttk.Button(self, text="fMRIprep Configuration", command=lambda: controller.show_frame(FmriPrepPage)).pack(pady=10)
        ttk.Button(self, text="XCP-d Configuration", command=lambda: controller.show_frame(XcpdPage)).pack(pady=10)


        

class FmriPrepPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="fmriprep Configuration").pack(pady=10)
        
        controller.setup_fmri_input_fields(controller)
        controller.setup_fmriprep_display()
        controller.load_config()

        #add save config widgets 
        ttk.Button(self, text="Save Configuration", command=controller.save_config).pack(pady=10)


class XcpdPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="xcpd Configuration").pack(pady=10)

       
        controller.setup_xcpd_input_fields(controller)
        controller.setup_xcpd_display()
        controller.load_config()
        #add save config widgets
        ttk.Button(self, text="Save Configuration", command=controller.save_config).pack(pady=10)


if __name__ == "__main__":
    app = Application()
    app.mainloop()