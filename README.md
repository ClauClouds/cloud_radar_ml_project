# cloud_radar_ml_project

Python utilities for reading cloud radar observations, extracting Doppler spectra samples, and preparing data products for machine learning workflows.

Python 3.9+ is supported.

## What this repository contains

- `readers/`: dataset loading and metadata logging.
- `process/`: sample extraction workflows and code to upload on s3 data bucket once samples are created
- `figures/`: plotting helpers for spectra and time-height diagnostics.
- `utils/`: configuration and normalization utilities.
-  config.py: configuration file to setup your run (to be edited for running what you want)

## Quick start

1. Create and activate a virtual environment.
2. Install the project in editable mode:

```bash
pip install -e .
```

3. Point the project to your radar data:

```bash
export CLOUD_RADAR_DATA_DIR="/path/to/cloud_radar_data"
export CLOUD_RADAR_OUTPUT_DIR="/path/to/output_directory"
export CLOUD_RADAR_FILENAME="20240105_1400.znc"
```

4. Run the sample extraction workflow:

```bash
python -m process.create_sample
```

or with the helper script:

```bash
./run_create_sample.sh
```

or, after installation:

```bash
cloud-radar-create-sample
```

## Expected data layout

The code expects `CLOUD_RADAR_DATA_DIR` to contain the file specified by `CLOUD_RADAR_FILENAME`.

Outputs are written to `CLOUD_RADAR_OUTPUT_DIR`, including:

- `spec_data.nc`
- `ds_variables.log`
- generated diagnostic figures
- `samples/` containing per-gate spectra plots

## Notes

- The default paths in [config.py] are currently set for the local Lampedusa dataset on this machine.
- Environment variables can still override those defaults when needed.
- Raw data is ignored by git through `.gitignore`.
- The project metadata is configured in `pyproject.toml`, so this folder is ready to initialize as a git repository and publish to GitHub.


## command to run .sh 
./run_create_sample.sh

## for uploading on s3 bucket where to then run Deep learning model
python3 -m process.upload_to_bucket.py

## link where to find project info a dataset
https://drive.google.com/drive/folders/1IyUB4aFUO9S4XaHOwwazp17tPlLD6aNp?usp=share_link
