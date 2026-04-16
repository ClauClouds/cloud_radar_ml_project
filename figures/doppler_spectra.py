

import pdb

import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.dates as mdates
import numpy as np
import os
import matplotlib.colors as mcolors


def plot_single_sample(spec, doppler, save_path=None):
    """
    Plots the doppler spectra for a given time stamp and range gate from a cloud radar file.

    Parameters:
    ds (xarray.Dataset): Cloud radar dataset for the selected time and range gate   .
    save_path (str, optional): Path to save the plot. If None, the plot will be displayed.

    Returns:
    None
    """

    #spec_plot = np.where(spectra.values > noise.values, spectra.values, noise.values)
        # Plot the doppler spectra

    fig, ax = plt.subplots(figsize=(10, 6))

    # plot spectra minus noise
    ax.plot(doppler,spec, color='black')

    # find max value of spec to set y axis limit
    max_spec = np.nanmax(spec)
    ax.set_ylim(0, max_spec*1.1)
    ax.set_xlim(doppler.min(), doppler.max())

    # make axis and labels invisible
    ax.axis('off')

    # be sure the only thing visible is the line plot of the spectra
    ax.set_frame_on(False)

    # Save or display the plot
    if save_path:
        fig.savefig(save_path)
        print(f'Plot saved to {save_path}')
    else:
        plt.show()
    plt.close(fig)
    return None


   
def plot_distribution_spectra_values(spec_data, cr_savefig_path):
    
    """Plots the distribution of the doppler spectra values for all time and range indexes where Zg is not Nan.
    Parameters:
    spec_data (numpy array): Array containing the doppler spectra values for all time and range indexes where Zg is not Nan.
    cr_savefig_path (str): Path to save the plot.
    Returns:
    None
    """
    print(np.nanmax(spec_data), np.nanmin(spec_data))
    # remove 0 from spec_data and replace them with nan
    spec_data[spec_data == 0] = np.nan

    # drop nan values from spec_data if present
    spec_data = spec_data[~np.isnan(spec_data)]

    # plot normalized distribution of spec_data values
    plt.figure(figsize=(8, 6))
    plt.hist(spec_data.flatten(), bins=50, color='blue', alpha=0.7, density=True)
    plt.title('Distribution of Spectra Values')
    plt.xlabel('Normalized Spectra Value')
    plt.ylabel('Frequency')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(cr_savefig_path, "spec_data_distribution.png"))
    plt.close()

    # identify bin value corresponding to max distribution value to set y axis limit of the sample plot
    counts, bins = np.histogram(spec_data.flatten(), bins=50)
    max_count = np.max(counts)

    # bin value corresponding to max distribution value
    max_bin = bins[np.argmax(counts)]
    print(f"Max distribution value: {max_count} at bin value: {max_bin}")

    return max_bin
