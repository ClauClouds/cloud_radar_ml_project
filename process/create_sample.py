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
from figures.doppler_spectra import plot_single_sample, plot_distribution_spectra_values
from utils.func import normalize_spec, extract_day_hour, construct_sample_string, store_data_ncdf
from config import *


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

    # Select time and range gate for the plot, local path where to save files, and site name for the plot title and file name
    if site == "lampedusa":
        file_path = os.path.join(cr_lampedusa_path, cr_lampedusa_filename)
        save_path = os.path.join(cr_lampedusa_savefig_path, "doppler_spectra_sample.png")
        time_stamp = cr_lampedusa_filename.split(".")[0]
        cr_savefig_path = cr_lampedusa_savefig_path
        log_path = log_lampedusa_path
    elif site == "joyce":
        file_path = os.path.join(cr_joyce_path, cr_joyce_filename)
        save_path = os.path.join(cr_joyce_savefig_path, "doppler_spectra_sample.png")
        time_stamp = cr_joyce_filename.split(".")[0]
        cr_savefig_path = cr_joyce_savefig_path
        log_path = log_joyce_path

    # create output folder if it does not exist
    os.makedirs(cr_savefig_path, exist_ok=True)
    os.makedirs(os.path.join(cr_savefig_path, "samples"), exist_ok=True)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Cloud radar file not found: {file_path}. Set CLOUD_RADAR_DATA_DIR and CLOUD_RADAR_FILENAME before running."
        )

    # extract day and hour from time stamp
    yy = time_stamp.split("_")[0][2:4]
    mm = time_stamp.split("_")[0][4:6]
    dd = time_stamp.split("_")[0][6:8]
    hh = time_stamp.split("_")[1][0:2]

    # construct date string
    date = f"{yy}{mm}{dd}"
    print(f"Selected case: {date} date, {hh} hour")

    # read the file and identify all time and range indexes where Zg is not Nan.
    # it resamples to 10 seconds if resampling is on
    ds, time_range_indices = read_cloud_radar_data(file_path, log_path=log_path, resampling=resampling)   

    if plotting:

        # plot time height plot of radar reflectivity for the day
        Ze_time_height_day(ds, date, cr_savefig_path)

        # plot the mask of time and range indexes where Zg is not Nan.
        plot_mask_spectra_gates(ds, time_range_indices, date, cr_savefig_path)


    # read doppler vel for firther plotting
    v_doppler = ds['doppler'].values

    # loop on time range indices and extract the doppler spectra for each of them, storing it in spec_data array
    total_samples = len(time_range_indices[0])
    bar = Bar("Extracting samples", max=total_samples) if Bar is not None else None

    spec_data = np.full((total_samples, len(ds['doppler'])), np.nan)
    times = np.full(total_samples, np.nan)
    ranges = np.full(total_samples, np.nan)

    ind = 0
    for time_idx, range_idx in zip(*time_range_indices):

        # select ds for the given time and range index
        ds_sel = ds.isel(time=time_idx, range=range_idx)

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
    ncdf_path = store_data_ncdf(spec_data, spec_data_norm, times, ranges, ds, site, date, hh, cr_savefig_path)
    print(f"Saved extracted spectra data to {ncdf_path}")

    # loop on all time and range indexes where Zg is not Nan and plot the doppler spectra for each of them
    for ind, (time_idx, range_idx) in enumerate(zip(*time_range_indices)):

        # read time stamp and range gate value for current index
        time_stamp = str(ds['time'].values[time_idx])
        range_gate = ds['range'].values[range_idx]

        print(f"Plotting doppler spectra for time stamp {time_stamp} and range gate {range_gate} m")

        # define sample file name and path to save the plot
        save_path = construct_sample_string(time_stamp, range_gate, cr_savefig_path, site, date=date)

        # call plotting function to plot the doppler spectra for the current time stamp and range gate
        plot_single_sample(spec_data[ind, :], v_doppler, doppler_range, save_path)


if __name__ == "__main__":
    main()