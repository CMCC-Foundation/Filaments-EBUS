import xarray as xr
import numpy as np
from dask.distributed import Client
from scripts.preprocessing import read_region_input_files
import os
from omegaconf import OmegaConf

if __name__ == '__main__':
    client = Client()
    print(client.dashboard_link)

    data = xr.merge([np.isnan(xr.open_zarr('/data01/benassi/export-biomass/data/processed/chl_2003-2023.zarr', chunks = 'auto')),
                    np.isnan(xr.open_zarr('/data01/benassi/export-biomass/data/processed/sst_2003-2023.zarr', chunks = 'auto')),
                    np.isnan(xr.open_zarr('/data01/benassi/export-biomass/data/processed/eudepth_2003-2023.zarr', chunks = 'auto'))])

    # Read coordinate list for boxes
    print('Reading regions')
    regions = read_region_input_files('regions.input')

    if not os.path.exists('outputs/data_availability/'):
        print('data_availability folder is missing. Creating it.')
        os.makedirs('outputs/data_availability/')

        # Read global configurations (number of clusters etc)
        cfg = OmegaConf.load('../glob_config.yaml')

        boxes = [box for boxes in regions.values() for box in boxes] 

        for i, box in enumerate(boxes):
            
            lons, lats = slice(box[0], box[1]), slice(box[2], box[3])
            data.sel(longitude = lons, latitude = lats).to_netcdf(f'outputs/data_availability/box_{i + 1}.nc')

        client.close()