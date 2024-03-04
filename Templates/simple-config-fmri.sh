#!/bin/bash

#$ -N sub-SUBJECT_xcp-d
#$ -pe smp 25
#$ -q PINC,VOSSHBC,UI
#$ -m bea
#$ -M zjgilliam@uiowa.edu

OMP_NUM_THREADS=10

singularity run --cleanenv \
-B /Users/USER/work:/work \
/Volumes/vosslabhpc/Projects/BETTER_IIB/3-Experiment/2-Data/BIDS/derivatives/code/derivatives/fmriprep_v23.2.0 \
InputDir \
DerivDir \
participant --participant-label SUBJECT \
--dummy-scans 5 \
--output-spaces MNI152NLin6Asym:res-2 MNI152NLin2009cAsym:res-native \
--resource-monitor \
--output-layout bids \
-fs-license-file {{Directory of the license file in shared server}} \