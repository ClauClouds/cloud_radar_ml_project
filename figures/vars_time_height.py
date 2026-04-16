"""
code to generatr time height plot for radar reflectivity and other variables for a day of cloud radar data.
 The code reads a cloud radar file for a given day and plots the radar reflectivity as a function of time and height.

"""
import pdb

import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.dates as mdates
import numpy as np
import os
import matplotlib.colors as mcolors

def Ze_time_height_day(ds, date, save_path=None):
    """
    Plots the radar reflectivity as a function of time and height for a given day from a cloud radar file.

    Parameters:
    ds (xarray.Dataset): The cloud radar data as an xarray Dataset.
    date (str): Date to select the data (format: 'YYYY-MM-DD').

    save_path (str, optional): Path to save the plot. If None, the plot will be displayed.

    Returns:
    None
    """
    
    # Select the radar reflectivity variable
    Ze = ds['Zg']
    
    # Plot the radar reflectivity as a function of time and height
    fig, ax = plt.subplots(figsize=(12, 6))

    pcm = ax.pcolormesh(Ze['time'], Ze['range'], Ze.T, shading='auto')
    fig.colorbar(pcm, ax=ax, label='Radar Reflectivity [dBZ]')  
    ax.set_title('Radar Reflectivity (Ze) Time-Height Plot')

    # format time on x axis as hh:mm
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    ax.set_xlabel('Time')
    ax.set_ylabel('Height [m]')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Save or display the plot
    if save_path:
        fig.savefig(save_path+f"{date}_Ze_time_height.png")
        print(f'Plot saved to {save_path}')
    else:
        plt.show()
    plt.close(fig)
    return None



def plot_mask_spectra_gates(ds,time_range_indices, date, save_path=None):
    """
    Plots the range gates where Doppler spectra should be plotted
      for a given cloud radar file.
      Parameters:
      ds (xarray.Dataset): The cloud radar data as an xarray Dataset.
      time_range_indices (tuple): Tuple of arrays containing the time and range indices where Doppler spectra should be plotted.
      date (str): Date to select the data (format: 'YYYY-MM-DD').
      save_path (str, optional): Path to save the plot. If None, the plot will be displayed.
      Returns:  
      None
    """

 
    # Select the radar reflectivity variable
    Ze = ds['Zg']

    # select Ze values to plot
    Ze_masked = np.full_like(Ze.values, 0)
    Ze_masked[time_range_indices] = 1
    
    # Plot the radar reflectivity as a function of time and height
    fig, ax = plt.subplots(figsize=(12, 6))

    # define a discrete colorbar with 2 colors (grey and orange) 
    cmap = mcolors.ListedColormap(["grey", "orange"])
    norm = mcolors.BoundaryNorm(boundaries=[0, 0.5, 1.5], ncolors=cmap.N)

    pcm = ax.pcolormesh(Ze['time'], Ze['range'], Ze_masked.T, shading='auto', cmap=cmap, norm=norm)

    cbar = plt.colorbar(pcm, ax=ax, ticks=[0.25, 1.0])
    cbar.ax.set_yticklabels(['No Spectra', 'Plot Spectra']) 

    # set cbar colors
    cbar.cmap.set_under('lightgrey')
    cbar.cmap.set_over('orange')
    ax.set_title('Mask of Time and Range Gates for Doppler Spectra Plotting')

    # format time on x axis as hh:mm
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    ax.set_xlabel('Time')
    ax.set_ylabel('Height [m]')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    
    # Save or display the plot
    if save_path:
        fig.savefig(os.path.join(save_path, f"{date}_mask.png"))
        print(f'Plot saved to {save_path}')
    else:
        plt.show()
    plt.close(fig)
    return None