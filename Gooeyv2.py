import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
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

    def create_new_project(self):
            project_name = simpledialog.askstring("Project Name", "Enter the name of the new project:")
            if project_name:
                project_dir = os.path.join(os.getcwd(), project_name)
                try:
                    os.makedirs(project_dir)
                    messagebox.showinfo("Success", f"Project '{project_name}' created successfully.")
                    # Now ask for configurations and save them
                    self.ask_for_config_and_save(project_name, project_dir)
                except FileExistsError:
                    messagebox.showerror("Error", "Project already exists.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create project: {str(e)}")

    def ask_for_config_and_save(self, project_name, project_dir):
        # Here you should implement the logic to ask the user for configuration details
        
        # For simplicity, we'll just simulate this with a placeholder dictionary
        config_data = {
            "example_setting": "value",
            # Add more settings here based on user input
        }
    
    # Save the configuration to a JSON file within the project's directory
    config_file_path = os.path.join(project_dir, f"{project_name}_config.json")
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
        messagebox.showinfo("Success", "Configuration saved successfully.")


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
        # Add your fmriprep configuration widgets here

class XcpdPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="xcpd Configuration").pack(pady=10)
        # Add your xcpd configuration widgets here

if __name__ == "__main__":
    app = Application()
    app.mainloop()
