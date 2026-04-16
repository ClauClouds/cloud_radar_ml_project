
import os
import pdb

import numpy as np
import matplotlib.pyplot as plt

def calc_ymax(spec):

    # remove 0 from spec_data and replace them with nan
    spec[spec == 0] = np.nan

    # drop nan values from spec_data if present
    spec = spec[~np.isnan(spec)]

    return np.nanmax(spec)


def normalize_spec(spec):

    ymax = calc_ymax(spec)

    # find max value of spec_data and normalize it to 1
    max_val = np.nanmax(spec)

    print(f"Max value of spec_data: {max_val}")

    # normalize spectra data by max value to have values between 0 and 1, to better visualize the distribution of the spectra values and set a threshold for plotting the samples
    spec_data_norm = spec/max_val 

    return spec_data_norm



def extract_day_hour(time_stamp):
    """
    Extracts the day and hour from a time stamp in the format "yyyy-mm-dd hh:mm:ss".

    Parameters:
    time_stamp (str): Time stamp in the format "yyyy-mm-dd hh:mm:ss".

    Returns:
    tuple: A tuple containing the year, month, day, hour, minute, and second as strings.
    """
    time_string = str(time_stamp).strip().replace("T", " ")
    date_part, time_part = time_string.split(" ", 1)
    time_part = time_part.split(".")[0]

    yy, mm, dd = date_part.split("-")
    hh, MM, ss = time_part.split(":")

    return yy, mm, dd, hh, MM, ss




def construct_sample_string(time_stamp, range_gate, cr_savefig_path, date=None):
    """
    costructs a string to save the plot of the doppler spectra for
      a given time stamp and range gate from a cloud radar file.
    Parameters:
    time_stamp (str): Time stamp in the format "yyyy-mm-dd hh:mm:ss".
    range_gate (float): Range gate value in meters.
    cr_savefig_path (str): Path to save the plot.
    date (str, optional): Date string in the format "yyyymmdd". If None,
      the date will be extracted from the time stamp.
    Returns:
    str: A string to save the plot of the doppler
      spectra for the given time stamp and range gate.

    """
    print(time_stamp, range_gate)
    range_string = int(range_gate)

    # extract day and hour from time stamp
    yy, mm, dd, hh, MM, ss = extract_day_hour(time_stamp)
    
    # write time stamp as "yymmdd_hhmmss"
    time_string = yy+mm+dd+'_'+hh+MM+ss

    # build string 
    str_sample = f"{time_string}_range_{range_string}"
    save_path = os.path.join(cr_savefig_path, "samples", f"{str_sample}.png")
    return save_path