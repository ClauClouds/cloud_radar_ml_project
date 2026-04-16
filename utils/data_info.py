"""Centralized path configuration for cloud radar processing."""

from pathlib import Path
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"


cr_lampedusa_path = os.getenv("CLOUD_RADAR_DATA_DIR", str(DEFAULT_DATA_DIR))
cr_lampedusa_filename = os.getenv("CLOUD_RADAR_FILENAME", "20240105_1400.znc")
cr_savefig_path = os.getenv("CLOUD_RADAR_OUTPUT_DIR", str(DEFAULT_OUTPUT_DIR))
log_lampedusa_path = os.path.join(cr_savefig_path, "ds_variables.log")