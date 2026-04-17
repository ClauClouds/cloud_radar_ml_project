"""
Define configuration variables for the project, such as file paths and parameters for data processing and plotting. 
This file centralizes all the configuration settings, making it easier to manage and update them in one place.
 It includes paths for input data, output directories, and any other parameters that may be needed across different modules of the project.

 To check your case studies and identify which range gates contain radar data
 For JOYCE: 
 https://atmos.meteo.uni-koeln.de/~hatpro/dataBrowser/dataBrowser2.html?site=JOYCE&date=-1&UpperLeft=Joyrad35_CN-Measurements&UpperRight=Ceilo_ct25k_Backscatter


"""


import os

"""keywords"""
plotting = True # keyword to turn on/off plotting functions in create_sample.py
resampling = True # keyword to turn on/off resampling of the data to 10 seconds in create_sample.py, to reduce the number of samples and make the processing faster.
# It resamples only if the time resolution of the dataset is below 10 seconds.
site = "joyce" # keyword to select the site to process in create_sample.py. It can be "lampedusa" or "joyce". 

# specifics for plots
doppler_range = (-10, 10) # range of doppler velocities to plot in the doppler spectra plots, in m/s




"""Centralized path configuration for cloud radar processing."""
DEFAULT_DATA_DIR = "/Users/claudia/Documents/Data/cloud_radar_Lampedusa"
DEFAULT_OUTPUT_DIR = "/Users/claudia/Documents/Data/cloud_radar_Lampedusa/plots"
DEFAULT_FILENAME = "20240105_1400.znc"


cr_lampedusa_path = os.getenv("CLOUD_RADAR_DATA_DIR", DEFAULT_DATA_DIR)
cr_lampedusa_filename = os.getenv("CLOUD_RADAR_FILENAME", DEFAULT_FILENAME)
cr_lampedusa_savefig_path = os.getenv("CLOUD_RADAR_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
log_lampedusa_path = os.path.join(cr_lampedusa_savefig_path, "ds_variables.log")

# add path for JOYCE dataset
JOYCE_DATA_DIR = "/Users/claudia/Documents/Data/cloud_radar_Joyce"
JOYCE_FILENAME = "20250829_1500.znc"
JOYCE_OUTPUT_DIR = "/Users/claudia/Documents/Data/cloud_radar_Joyce/plots"

cr_joyce_path = os.getenv("JOYCE_CLOUD_RADAR_DATA_DIR", JOYCE_DATA_DIR)
cr_joyce_filename = os.getenv("JOYCE_CLOUD_RADAR_FILENAME", JOYCE_FILENAME)
cr_joyce_savefig_path = os.getenv("JOYCE_CLOUD_RADAR_OUTPUT_DIR", JOYCE_OUTPUT_DIR)
log_joyce_path = os.path.join(cr_joyce_savefig_path, "ds_variables.log")
