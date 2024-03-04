import pandas as pd
import os
import sys
import re

# Setting up Directories
bidsDir = {}
xcpdDir = {}

# Function to replace placeholders in the template
def replace_placeholders(template, subject):
    # Here we will replace placeholders in the template string with actual values
    # For simplicity, only SUBJECT and SESSION are shown, but will expand with Bryan
    return template.replace("SUBJECT", subject)

# Read in the csv file
df = pd.read_csv(sys.argv[1])

# Iterate over each row to create job files
for index, row in df.iterrows():
    subject = row['subject']
    session = row['session']
    optFlags = row['optional flags']
    file_path = row['job_file']
    submitted = row['submitted']

    # Directory naming convention (adjust for correct convention after meeting w/ Bryan)
    output_dir = f"sub-{subject}-{session}"
    full_output_path = os.path.join("fmriprep_v23.2.0", output_dir)
    os.makedirs(full_output_path, exist_ok=True)

    #If a subject has already been processed, skip it and move to the next one
    if df['job_file'] == "submitted":
        print(f"Subject {subject} has already been processed. Skipping...")
        continue

    # Create the job file for each row, replacing placeholders with actual values
    job_file = f"sub-{subject}-{session}.job"
    with open(job_file, "w") as f:
        f.write(f"""#!/bin/bash
            #$ -pe smp 56
            #$ -q UI
            #$ -m bea
            #$ -M zjgilliam@uiowa.edu
            #$ -j y
            #$ -o /Shared/vosslabhpc/Projects/BETTER_B2/3-Experiment/2-Data/BIDS/derivatives/code/xcp-d/out
            #$ -e /Shared/vosslabhpc/Projects/BETTER_B2/3-Experiment/2-Data/BIDS/derivatives/code/xcp-d/err
            OMP_NUM_THREADS=10
            singularity run --cleanenv -H ${{HOME}}/singularity_home -B /Shared/vosslabhpc:/mnt \
            /Shared/vosslabhpc/UniversalSoftware/SingularityContainers/xcp_d_v0.6.1.sif \
            /mnt/Projects/BETTER_B2/3-Experiment/2-Data/BIDS/derivatives/fmriprep_v23.2.0 \
            /mnt/Projects/BETTER_B2/3-Experiment/2-Data/BIDS/derivatives/xcp_d_v0.6.1 \
            participant --participant_label {subject} \
            --dummy-scans 5 \
            -f 0.5 \
            --atlases 4S456Parcels
            """).format(subject)

    # Store an array of each job file
    job_files_array = []
    job_files_array.append(job_file)




#if error move to nenxt job file and log error in a file - if more than one error log all in the same file
error_log_file = "error_log-.txt"

for job_file in job_files_array:
    try:
        os.system(f"qsub {job_file}")
        print(f"Submitted {job_file} to the cluster")
        # If successful, mark the job file as submitted in the csv
        df['submitted'] = "TRUE"
    except Exception as e:
        with open(error_log_file, "a") as f:
            f.write(f"Error submitting {job_file}: {str(e)}\n")

        continue

    print(f"Submitted {job_file} to the cluster")





