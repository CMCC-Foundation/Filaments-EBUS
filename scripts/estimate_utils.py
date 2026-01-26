import os
import numpy as np
import xarray as xr

def compute_maxmins_pairs(timeseries, weighted = False,  pct_avails = None):
        ts = timeseries.values

        # 0.0 is only for cloud coverage
        zero_mask = ts > 0

        ts = ts[zero_mask]

        if weighted:
            pct = pct_avails[zero_mask]
            ts = ts / pct

        maxmins = []

        for i in range(1, len(ts) - 1):
            max_mask = (ts[i] > ts[i-1]) & (ts[i] > ts[i+1])
            if max_mask: 
                #print(f'found max at index {i}. looking for subsequent min')
                for j in range(i, len(ts) - 1):
                    min_mask = (ts[j] < ts[j-1]) & (ts[j] < ts[j+1])
                    if min_mask:
                        #print(f'found min at index {j}. saving')
                        maxmins.append([i, j])
                        break

        maxmins = np.array(maxmins)

        times = timeseries.time[zero_mask][maxmins[:,0]]

        maxs = xr.DataArray(timeseries[zero_mask][maxmins[:,0]],
                        coords = {'time' : times})
        mins = xr.DataArray(timeseries[zero_mask][maxmins[:,1]],
                        coords = {'time' : times})

        return maxs, mins


def compute_transport(timeseries, period = 'year', weighted = False, pct_avails = None):

    maxs, mins = compute_maxmins_pairs(timeseries, weighted = weighted, pct_avails = pct_avails)

    return (maxs - mins).groupby(f'time.{period}').sum()

def load_carbon_data(path):
    return  xr.open_dataarray(path) * 50

def compute_carbon_per_region(group, path, weighted = False, pct_avails = None):
    boxes = []
    for i, box in enumerate(group):
        box_timeseries = load_carbon_data(os.path.join(path, f'box_{box}.nc'))
        if weighted:
            box_timeseries = box_timeseries / pct_avails[i]
        box_timeseries.name = f'box_{box}'
        boxes.append(box_timeseries)
    time_series = xr.merge(boxes)
    time_series = sum([time_series[f'box_{i}'] for i in group]) # (carbon export)
    return time_series

def circular_rolling_average(data, window_size):
    """
    Calculates the circular rolling average of a 1D NumPy array.

    Args:
        data (np.ndarray): The input 1D NumPy array.
        window_size (int): The size of the rolling window.

    Returns:
        np.ndarray: The array containing the circular rolling averages.
    """
    if window_size <= 0:
        raise ValueError("Window size must be a positive integer.")
    if window_size > len(data):
        raise ValueError("Window size cannot be greater than the data length.")

    # Pad the data circularly
    padded_data = np.concatenate((data[-window_size:], data, data[:window_size]))

    # Create the weights for the moving average (all ones for simple average)
    weights = np.ones(window_size) / window_size

    # Convolve the padded data with the weights
    # 'valid' mode ensures only full overlaps are considered,
    # effectively returning the rolling average for the original data length
    circular_avg = np.convolve(padded_data, weights, mode='same')

    return circular_avg[window_size:-(window_size)]
