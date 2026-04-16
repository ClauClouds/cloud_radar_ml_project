"""
Code to generate cloud radar doppler spectra sample for deep learning processing
The code reads a cloud radar file for a given time stamp and plots the doppler spectra for a given range gate

how to run:
cd /Users/claudia/Github/cloud_radar_project
source /Users/claudia/Github/.env_base/bin/activate
python -m process.create_sample

"""


import pdb

from figures.vars_time_height import Ze_time_height_day, plot_mask_spectra_gates
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import os
from progress.bar import Bar

from readers.cloud_radar_lampedusa import read_cloud_radar_data, read_and_store_log_vars
from utils.data_info import cr_lampedusa_path, cr_lampedusa_filename, cr_savefig_path, log_lampedusa_path
from figures.doppler_spectra import plot_single_sample, plot_distribution_spectra_values
from utils.func import normalize_spec

def extract_sample(ds):
    """
    Extracts the doppler spectra for a given time index and range index from a cloud radar dataset.

    Parameters:
    ds (xarray.Dataset): Cloud radar dataset for selected time and range index.

    Returns:
    xarray.Dataset: The selected doppler spectra data as an xarray Dataset.
    """
    spectra = ds['SPCco'].values
    noise = np.repeat(ds['HSDco'].values, len(ds['doppler'])) 

    # define a new var as spec_plot that is spectra if spectra is larger than noise, else is noise
    spec_no_noise = spectra - noise  
    spec_plot = np.where(spec_no_noise > 0, spec_no_noise, 0)

    return spec_plot

def main():

    # Select time and range gate for the plot
    file_path = os.path.join(cr_lampedusa_path, cr_lampedusa_filename)
    time_stamp = "2024-01-05 14:00:00"
    range_gate = 10
    save_path = os.path.join(cr_savefig_path, "doppler_spectra_sample.png")
    plotting = True

    os.makedirs(cr_savefig_path, exist_ok=True)
    os.makedirs(os.path.join(cr_savefig_path, "samples"), exist_ok=True)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Cloud radar file not found: {file_path}. Set CLOUD_RADAR_DATA_DIR and CLOUD_RADAR_FILENAME before running."
        )

    # extract day and hour from time stamp
    yy = time_stamp.split(" ")[0].split("-")[0]
    mm = time_stamp.split(" ")[0].split("-")[1]
    dd = time_stamp.split(" ")[0].split("-")[2]
    hh = time_stamp.split(" ")[1].split(":")[0]

    # construct date string
    date = f"{yy}{mm}{dd}"
    print(f"Selected case: {date} date, {hh} hour")

    # read the file
    ds = read_cloud_radar_data(file_path)   

    # Select the data for the given time stamp and range gate
    doppler = ds['doppler'].values

    # sorting all dataset variables according to doppler values, to have the doppler spectra ordered by doppler velocity
    sorted_indices = np.argsort(doppler)
    doppler = doppler[sorted_indices]
    ds_sorted = ds.isel(doppler=sorted_indices)


    # read and stor log var file if it does not exist
    if not os.path.exists(log_lampedusa_path):
        read_and_store_log_vars(ds)

    # identify all time and range indexes where Zg is not Nan.
    time_range_indices = np.where(~np.isnan(ds['Zg'].values))

    if plotting:

        # plot time height plot of radar reflectivity for the day
        Ze_time_height_day(ds, "20240105", cr_savefig_path)

        # plot the mask of time and range indexes where Zg is not Nan.
        plot_mask_spectra_gates(ds, time_range_indices, "20240105", cr_savefig_path)


    # read doppler vel for firther plotting
    v_doppler = ds_sorted['doppler'].values

    # loop on time range indices and extract the doppler spectra for each of them, storing it in spec_data array
    total_samples = len(time_range_indices[0])
    bar = Bar("Extracting samples", max=total_samples) if Bar is not None else None

    spec_data = np.full((total_samples, len(ds['doppler'])), np.nan)
    times = np.full(total_samples, np.nan)
    ranges = np.full(total_samples, np.nan)

    ind = 0
    for time_idx, range_idx in zip(*time_range_indices):

        # select ds for the given time and range index
        ds_sel = ds_sorted.isel(time=time_idx, range=range_idx)

        # store time and range values for the current index
        times[ind] = ds_sel['time'].values
        ranges[ind] = ds_sel['range'].values

        # extract sample
        spec_data[ind, :] = extract_sample(ds_sel)
        ind += 1

        if bar is not None:
            bar.next()

    if bar is not None:
        bar.finish()

    # normalize spec_data by its max value to have values between 0 and 1, to better visualize the distribution of the spectra values and set a threshold for plotting the samples
    spec_data_norm = normalize_spec(spec_data)


    # store data in an ncdf file for further use
    ds_spec = xr.Dataset(
        data_vars={
            "spec_data": (("times", "doppler"), spec_data),
            "spec_data_norm": (("times", "doppler"), spec_data_norm),
        },
        coords={
            "times": times,
            "doppler": ds_sorted['doppler'].values,
            "ranges": ranges
        }
    )   
    ds_spec.to_netcdf(os.path.join(cr_savefig_path, "spec_data.nc"))
    print(f"Saved extracted spectra data to {os.path.join(cr_savefig_path, 'spec_data.nc')}")


    # loop on all time and range indexes where Zg is not Nan and plot the doppler spectra for each of them
    for ind, (time_idx, range_idx) in enumerate(zip(*time_range_indices)):

        # read time stamp and range gate value for current index
        time_stamp = str(ds_sorted['time'].values[time_idx])
        range_gate = ds_sorted['range'].values[range_idx]
        print(f"Plotting doppler spectra for time stamp {time_stamp} and range gate {range_gate} m")

        # approximate range gate to avoid decimals values
        range_gate = int(range_gate)

        # write time stamp as yymmdd_hhmmss
        time_stamp = time_stamp.replace(" ", "_").replace(":", "").replace("-", "")[:-3]

        # build string 
        str_sample = f"{date}_{time_stamp}_range_{range_gate}"
        save_path = os.path.join(cr_savefig_path, "samples", f"{str_sample}.png")

        # call plotting function to plot the doppler spectra for the current time stamp and range gate
        plot_single_sample(spec_data_norm[ind, :], v_doppler, save_path)


if __name__ == "__main__":
    main()