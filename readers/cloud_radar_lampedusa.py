"""
Routines to read the cloud radar data from Lampedusa, in format .znc, which is a NetCDF format. 
The data is read using xarray and returned as an xarray Dataset.

"""
import pdb
import pandas as pd

from utils.data_info import cr_lampedusa_path
import xarray as xr
import os

from utils.data_info import log_lampedusa_path

def read_cloud_radar_data(file_path):
    """
    Reads the cloud radar data from a given file path and returns it as an xarray Dataset.

    Parameters:
    file_path (str): Path to the cloud radar file (NetCDF format).

    Returns:
    xarray.Dataset: The cloud radar data as an xarray Dataset.
    """
    
    # Read the cloud radar data using xarray
    ds = xr.open_dataset(file_path)

    # convert time from seconds since since 01.01.1970 00:00 UTC to datetime format
    ds["time"] = pd.to_datetime(ds["time"].values, unit="s")

    return ds


def read_and_store_log_vars(ds):
    log_path = log_lampedusa_path

    with open(log_path, "w") as f:
        print("Dataset attributes:", file=f)
        for key, value in ds.attrs.items():
            print(f"  {key}: {value}", file=f)

        for name, da in ds.data_vars.items():
            print(f"\nVariable: {name}", file=f)
            print(f"  dims: {da.dims}", file=f)
            print(f"  shape: {da.shape}", file=f)
            print("  attrs:", file=f)
            for key, value in da.attrs.items():
                print(f"    {key}: {value}", file=f)
    # close file
    f.close()
    
    print(f"Wrote log to {log_path}")

    return None
