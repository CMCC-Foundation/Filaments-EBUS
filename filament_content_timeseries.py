import xarray as xr
import numpy as np

import os
import joblib
from scripts.preprocessing import read_region_input_files, crop_region

from tqdm import tqdm

from omegaconf import OmegaConf

from dask.distributed import Client


if __name__ == '__main__':
    print('### Filament content timeseries computation ###')
    client = Client()
    # Read coordinate list for boxes
    print('Reading regions')
    regions = read_region_input_files('regions.input')

    if not os.path.exists('outputs/filament_content_timeseries/'):
        print('filament_content_timeseries folder is missing. Creating it.')
        os.makedirs('outputs/filament_content_timeseries/')

    # Read global configurations (number of clusters etc)
    cfg = OmegaConf.load('../glob_config.yaml')
    print(cfg)

    boxes = [box for boxes in regions.values() for box in boxes] 

    for i, box in enumerate(boxes):
        i += 1
        if not os.path.exists(f'outputs/filament_content_timeseries/box_{i}.nc'):
            print(f'Processing box {i}...')

            masks = xr.open_dataarray(f'outputs/filament_masks/box_{i}.nc').chunk({'time' : 1})

            chl = crop_region(cfg.chl_path, box) * masks
            eudepth = crop_region(cfg.eudepth_path, box) * masks

            biomass_content = chl * eudepth 
            time_series = biomass_content.sum(dim=['longitude', 'latitude']) * (4000)**2 * 1e-15

            time_series.to_netcdf(f'outputs/filament_content_timeseries/box_{i}.nc')
        else:
            print(f'Box {i} already processed. Skipping...')

    client.close()
