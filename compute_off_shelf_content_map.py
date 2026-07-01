import xarray as xr
import numpy as np

import os
import joblib
from scripts.preprocessing import read_region_input_files, crop_region

from tqdm import tqdm

from omegaconf import OmegaConf

from dask.distributed import Client


if __name__ == '__main__':
    print('### Off-shelf content map computation ###')

    client = Client()
    print(client.dashboard_link)
    # Read coordinate list for boxes
    print('Reading regions')
    regions = read_region_input_files('regions.input')
    print(f'Found regions: {regions.keys()}')

    if not os.path.exists('outputs/off_shelf_content_map/'):
        print('off_shelf_content_map folder is missing. Creating it.')
        os.makedirs('outputs/off_shelf_content_map/')

    # Read global configurations (number of clusters etc)
    cfg = OmegaConf.load('glob_config.yaml')
    print(cfg)

    boxes = [box for boxes in regions.values() for box in boxes] 
   # bathy = xr.open_dataarray(cfg.bathy_path)

    for i, box in enumerate(boxes):
        i += 1

        if not os.path.exists(f'outputs/off_shelf_content_map/box_{i}.nc'):
            print(f'Processing box {i}...')

            chl_path = os.path.join(cfg.data_path, 'chl', f'box_{i}.nc')
            eudepth_path = os.path.join(cfg.data_path, 'eudepth', f'box_{i}.nc')
            bathy = xr.open_dataarray(os.path.join(cfg.data_path, 'bathymetry', f'box_{i}.nc'))


            lons, lats = slice(box[0], box[1]), slice(box[2], box[3])
            off_shelf_mask = bathy.sel(longitude=lons, latitude=lats) < cfg.ref_depth

            chl = xr.open_dataarray(chl_path) * off_shelf_mask
            eudepth = xr.open_dataarray(eudepth_path) * off_shelf_mask

            # chl = crop_region(cfg.chl_path, box) * off_shelf_mask
            # eudepth = crop_region(cfg.eudepth_path, box) * off_shelf_mask

            biomass_content = chl * eudepth * (4000)**2 * 1e-15


            biomass_content.to_netcdf(f'outputs/off_shelf_content_map/box_{i}.nc')
        else:
            print(f'Box {i} already processed. Skipping...')

    client.close()
