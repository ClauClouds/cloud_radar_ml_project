"""
Routines to read the cloud radar data from Lampedusa, in format .znc, which is a NetCDF format. 
The data is read using xarray and returned as an xarray Dataset.

"""
import pdb
import pandas as pd
import numpy as np
import xarray as xr
import os


def read_cloud_radar_data(file_path, log_path, resampling=False):
    """
    Reads the cloud radar data from a given file path and returns it as an xarray Dataset.

    Parameters:
    file_path (str): Path to the cloud radar file (NetCDF format).
    log_path (str): Path to the log file where dataset variables will be stored.
    resampling (bool): Whether to resample the data to 10 seconds intervals. Default is False.
    
    Returns:
    xarray.Dataset: The cloud radar data as an xarray Dataset.
    """
    
    # Read the cloud radar data using xarray
    ds = xr.open_dataset(file_path)

    # Convert integer epoch seconds to datetimes before any time-based operations.
    if not np.issubdtype(ds["time"].dtype, np.datetime64):
        ds["time"] = pd.to_datetime(ds["time"].values, unit="s")

    if resampling:

        # read the time resolution of the dataset from ds
        time_res = ds['time'].diff('time').values[0]

        # print time resolution in seconds
        time_res_seconds = np.timedelta64(time_res, 's').astype(int)

        print(f"Time resolution of the dataset: {time_res_seconds} seconds")

        # if time res is below 10 seconds, resample the data to 10 seconds 
        # to reduce the number of samples and make the processing faster, 
        # by taking the mean of the values in each 10 seconds interval
        if time_res_seconds < 10:
            ds = ds.resample(time='10s').mean(skipna=True)
            print(f"Resampled the dataset to 10 seconds resolution")
            print("######################################################")

    # Select the data for the given time stamp and range gate
    doppler = ds['doppler'].values

    # sorting all dataset variables according to doppler values, to have the doppler spectra ordered by doppler velocity
    sorted_indices = np.argsort(doppler)
    doppler = doppler[sorted_indices]
    ds_sorted = ds.isel(doppler=sorted_indices)

    # read and stor log var file if it does not exist
    if not os.path.exists(log_path):
        read_and_store_log_vars(ds_sorted, log_path)

    # identify all time and range indexes where Zg is not Nan.
    time_range_indices = np.where(~np.isnan(ds_sorted['Zg'].values))


    return ds_sorted, time_range_indices


def read_and_store_log_vars(ds, log_path):
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
