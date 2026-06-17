import xarray as xr
import numpy as np

import os
import joblib
from scripts.preprocessing import read_region_input_files, crop_region

from tqdm import tqdm

from omegaconf import OmegaConf

from dask.distributed import Client



"""
Computes the daily time series of shelf content for each box (n_time,).
"""
if __name__ == '__main__':
    print('### Shelf content timeseries computation ###')

    client = Client()
    print(client.dashboard_link)
    # Read coordinate list for boxes
    print('Reading regions')
    regions = read_region_input_files('regions.input')

    if not os.path.exists('outputs/shelf_content_timeseries/'):
        print('shelf_content_timeseries folder is missing. Creating it.')
        os.makedirs('outputs/shelf_content_timeseries/')

    # Read global configurations (number of clusters etc)
    cfg = OmegaConf.load('../glob_config.yaml')
    print(cfg)

    boxes = [box for boxes in regions.values() for box in boxes] 

    for i, box in enumerate(boxes):
        i += 1
        if not os.path.exists(f'outputs/shelf_content_timeseries/box_{i}.nc'):
            print(f'Processing box {i}')
            content = xr.open_dataarray(f'outputs/shelf_content_map/box_{i}.nc').chunk({'time' : 1})

            time_series = content.sum(dim=['longitude', 'latitude'])

            time_series.to_netcdf(f'outputs/shelf_content_timeseries/box_{i}.nc')
        else:
            print(f'Box {i} already processed. Skipping.')

    client.close()
