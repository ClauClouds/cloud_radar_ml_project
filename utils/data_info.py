"""Centralized path configuration for cloud radar processing."""

import os


DEFAULT_DATA_DIR = "/Users/claudia/Documents/Data/cloud_radar_Lampedusa"
DEFAULT_OUTPUT_DIR = "/Users/claudia/Documents/Data/cloud_radar_Lampedusa/plots"
DEFAULT_FILENAME = "20240105_1400.znc"


cr_lampedusa_path = os.getenv("CLOUD_RADAR_DATA_DIR", DEFAULT_DATA_DIR)
cr_lampedusa_filename = os.getenv("CLOUD_RADAR_FILENAME", DEFAULT_FILENAME)
cr_savefig_path = os.getenv("CLOUD_RADAR_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
log_lampedusa_path = os.path.join(cr_savefig_path, "ds_variables.log")