import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox, scrolledtext
import pandas as pd
import os
import json

project_name = ""
project_dir = ""
config_data = {}


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Project Management")
        self.geometry("800x600")
        
        # Add a button on the home page to create a new project
        self.create_project_button = tk.Button(self, text="Create New Project", command=self.create_new_project)
        self.create_project_button.pack(pady=20)
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
        

        # Initialize container for pages
        self.container = ttk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (HomePage, FmriPrepPage, XcpdPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")
    
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


    def create_new_project(self):
            project_name = simpledialog.askstring("Project Name", "Enter the name of the new project:")
            if project_name:
                project_dir = os.path.join(os.getcwd(), project_name)
                try:
                    os.makedirs(project_dir)
                    config_file = os.path.join(project_dir, "config.json")
                    with open(config_file, "w") as f:
                        json.dump(config_data, f)
                    messagebox.showinfo("Success", f"Project '{project_name}' created successfully.")
                    # Now ask for configurations and save them
                    self.ask_for_config_and_save(project_name, project_dir)
                except FileExistsError:
                    messagebox.showerror("Error", "Project already exists.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create project: {str(e)}")



    def setup_fmriprep_input_fields(self):
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y")

        row = 0
        for name, var in self.variables.items():
            #if variable does not start with "xcpd" then skip
            if not name.startswith("xcpd"):  
                ttk.Label(left_frame, text=name.replace('_', ' ').title() + ":").grid(row=row, column=0, sticky=tk.W)
                ttk.Entry(left_frame, textvariable=var).grid(row=row, column=1, sticky=tk.EW)
                # Bind the variable to update the display whenever its value changes
                var.trace_add("write", lambda name, index, mode, var=var: self.update_display())
                row += 1
            else:
                row+=1

    def setup_display(self):
        self.display = scrolledtext.ScrolledText(self, state='disabled')
        self.display.pack(side="right", fill="both", expand=True)

    

    def setup_xcpd_input_fields(self):
        left_frame = ttk.Frame(self)
        left_frame.pack(side="left", fill="y")

        row = 0
        for name, var in self.variables.items():
            #if variable does not start with "fmriprep" then skip
            if not name.startswith("fmriprep"):  
                ttk.Label(left_frame, text=name.replace('_', ' ').title() + ":").grid(row=row, column=0, sticky=tk.W)
                ttk.Entry(left_frame, textvariable=var).grid(row=row, column=1, sticky=tk.EW)
                # Bind the variable to update the display whenever its value changes
                var.trace_add("write", lambda name, index, mode, var=var: self.update_display())
                row += 1
            else:
                row+=1




    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_class):
        '''Get an instance of a page given its class'''
        return self.frames[page_class.__name__]

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Home Page").pack(pady=10)

        # Example of switching pages
        ttk.Button(self, text="Go to fmriprep",
                   command=lambda: controller.show_frame("FmriPrepPage")).pack()
        ttk.Button(self, text="Go to xcpd",
                   command=lambda: controller.show_frame("XcpdPage")).pack()

class FmriPrepPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="fmriprep Configuration").pack(pady=10)
        
        # Add widgets
        controller.setup_fmriprep_input_fields()
        controller.setup_display()
        controller.load_config()

class XcpdPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="xcpd Configuration").pack(pady=10)

        # Add widgets
        controller.setup_xcpd_input_fields()
        controller.setup_display()
        controller.load_config()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
