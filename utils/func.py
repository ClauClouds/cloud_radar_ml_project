
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