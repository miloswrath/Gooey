# Importing necessary libraries
import tkinter as tk
from tkinter import scrolledtext, ttk

# Function to update the shell script display based on user inputs and selections
def update_shell_script(*args):
    # Collecting user inputs with updated variable names
    bids_dir = bids_dir_var.get()
    fmriprep_container_dir = fmriprep_container_dir_var.get()
    fmriprep_job_file_out_dir = fmriprep_job_file_out_dir_var.get()
    fmriprep_out_dir = fmriprep_out_dir_var.get()
    fmriprep_error_out_dir = fmriprep_error_out_dir_var.get()
    fmriprep_freesurfer_license_dir = fmriprep_freesurfer_license_dir_var.get()
    xcpd_container_dir = xcpd_container_dir_var.get()
    xcpd_job_file_out_dir = xcpd_job_file_out_dir_var.get()
    xcpd_out_dir = xcpd_out_dir_var.get()
    xcpd_error_out_dir = xcpd_error_out_dir_var.get()
    user_email = user_email_var.get()

    # Building the shell script sample dynamically
    # The string content is not updated here as per instruction
    shell_script = f"""
    #fmriscript
    #!/bin/bash
    #$ -pe smp 56
    #$ -q UI
    #$ -m bea
    #$ -M {user_email}
    #$ -j y
    #$ -o {fmriprep_out_dir}
    #$ -e {fmriprep_error_out_dir}
    OMP_NUM_THREADS=10
    singularity run --cleanenv -H ${{HOME}}/singularity_home -B /Shared/vosslabhpc:/mnt \\
    /{fmriprep_container_dir} \\
    /{bids_dir} \\
    /{fmriprep_out_dir} \\
    participant --participant_label SUBJECT WILL GO HERE \\
    --dummy-scans 5 \\
    -f 0.5 \\
    --license /{fmriprep_freesurfer_license_dir} \\
    --atlases 4S456Parcels
    #path: {fmriprep_job_file_out_dir}

    #xcpdscript
    #!/bin/bash
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
    # Updating the shell script display
    shell_script_display.config(state=tk.NORMAL)
    shell_script_display.delete(1.0, tk.END)
    shell_script_display.insert(tk.INSERT, shell_script)
    shell_script_display.config(state=tk.DISABLED)


# Creating the main window
root = tk.Tk()
root.title("fMRI Preprocessing GUI")

# Defining user input variables with updated names
bids_dir_var = tk.StringVar()
fmriprep_container_dir_var = tk.StringVar()
fmriprep_job_file_out_dir_var = tk.StringVar()
fmriprep_out_dir_var = tk.StringVar()
fmriprep_error_out_dir_var = tk.StringVar()
fmriprep_freesurfer_license_dir_var = tk.StringVar()
xcpd_container_dir_var = tk.StringVar()
xcpd_job_file_out_dir_var = tk.StringVar()
xcpd_out_dir_var = tk.StringVar()
xcpd_error_out_dir_var = tk.StringVar()
user_email_var = tk.StringVar()
subject_ids_var = tk.StringVar()  # Ensure this variable is defined as it's used in the function

# Function to bind variable changes to the update function
def bind_variable_updates():
    variables = [
        bids_dir_var, fmriprep_container_dir_var, fmriprep_job_file_out_dir_var,
        fmriprep_out_dir_var, fmriprep_error_out_dir_var, fmriprep_freesurfer_license_dir_var,
        xcpd_container_dir_var, xcpd_job_file_out_dir_var, xcpd_out_dir_var,
        xcpd_error_out_dir_var, user_email_var, subject_ids_var
    ]
    for var in variables:
        var.trace_add("write", update_shell_script)


# Binding variable changes to the update function
bind_variable_updates()



# Creating the layout
left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

right_frame = ttk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Starting row for the grid layout
row_index = 0

# Widget for BIDS Directory
ttk.Label(left_frame, text="BIDS Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=bids_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for fmriprep Container Directory
ttk.Label(left_frame, text="fmriprep Container Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=fmriprep_container_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for fmriprep Job File Output Directory
ttk.Label(left_frame, text="fmriprep Job File Output Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=fmriprep_job_file_out_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for fmriprep Output Directory
ttk.Label(left_frame, text="fmriprep Output Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=fmriprep_out_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for fmriprep Error Output Directory
ttk.Label(left_frame, text="fmriprep Error Output Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=fmriprep_error_out_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for fmriprep Freesurfer License Directory
ttk.Label(left_frame, text="fmriprep Freesurfer License Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=fmriprep_freesurfer_license_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for xcp-d Container Directory
ttk.Label(left_frame, text="xcp-d Container Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=xcpd_container_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for xcp-d Job File Output Directory
ttk.Label(left_frame, text="xcp-d Job File Output Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=xcpd_job_file_out_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for xcp-d Output Directory
ttk.Label(left_frame, text="xcp-d Output Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=xcpd_out_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for xcp-d Error Output Directory
ttk.Label(left_frame, text="xcp-d Error Output Directory:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=xcpd_error_out_dir_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for User Email
ttk.Label(left_frame, text="User Email for HPC:").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=user_email_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)
row_index += 1

# Widget for Subject IDs
ttk.Label(left_frame, text="Subject IDs (comma-separated):").grid(row=row_index, column=0, sticky=tk.W, padx=5, pady=2)
ttk.Entry(left_frame, textvariable=subject_ids_var).grid(row=row_index, column=1, sticky=tk.EW, padx=5, pady=2)

# Right frame widget (shell script display)
shell_script_display = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, state=tk.DISABLED)
shell_script_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Initial update of the shell script display
update_shell_script()

# Start the GUI event loop
root.mainloop()
